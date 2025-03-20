/// <reference types="react" />

import * as glMatrix from 'gl-matrix';
import React, {
  // DO NOT require MouseEvent
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useContext
} from 'react';
import { throttle } from '../utils';
import {$StateContext} from '../context';
import { useCanvasSnapshot } from '../canvasSnapshot';
import {
  CameraParams,
  CameraState,
  createCameraParams,
  createCameraState,
  dolly,
  adjustFov,
  orbit,
  pan,
  roll,
  zoom,
  DraggingState
} from './camera3d'

import isEqual from 'lodash-es/isEqual';

import {ellipsoidAxesSpec} from './components/ring'
import { ComponentConfig, cuboidSpec, ellipsoidSpec, lineBeamsSpec, pointCloudSpec, buildPickingData, buildRenderData } from './components';
import { unpackID } from './picking';
import { LIGHTING } from './shaders';
import { BufferInfo, GeometryResources, GeometryResource, PrimitiveSpec, RenderObject, PipelineCacheEntry, DynamicBuffers, RenderObjectCache, ComponentOffset } from './types';

/**
 * Aligns a size or offset to 16 bytes, which is a common requirement for WebGPU buffers.
 * @param value The value to align
 * @returns The value aligned to the next 16-byte boundary
 */
function align16(value: number): number {
  return Math.ceil(value / 16) * 16;
}

export interface SceneInnerProps {
  /** Array of 3D components to render in the scene */
  components: ComponentConfig[];

  /** Width of the container in pixels */
  containerWidth: number;

  /** Height of the container in pixels */
  containerHeight: number;

  /** Optional CSS styles to apply to the canvas */
  style?: React.CSSProperties;

  /** Optional controlled camera state. If provided, the component becomes controlled */
  camera?: CameraParams;

  /** Default camera configuration used when uncontrolled */
  defaultCamera?: CameraParams;

  /** Callback fired when camera parameters change */
  onCameraChange?: (camera: CameraParams) => void;

  /** Callback fired after each frame render with the render time in milliseconds */
  onFrameRendered?: (renderTime: number) => void;

  /** Callback to fire when scene is initially ready */
  onReady: () => void;
}

function initGeometryResources(device: GPUDevice, resources: GeometryResources) {
  // Create geometry for each primitive type
  for (const [primitiveName, spec] of Object.entries(primitiveRegistry)) {
    const typedName = primitiveName as keyof GeometryResources;
    if (!resources[typedName]) {
      resources[typedName] = spec.createGeometryResource(device);
    }
  }
}

const primitiveRegistry: Record<ComponentConfig['type'], PrimitiveSpec<any>> = {
  PointCloud: pointCloudSpec,
  Ellipsoid: ellipsoidSpec,
  EllipsoidAxes: ellipsoidAxesSpec,
  Cuboid: cuboidSpec,
  LineBeams: lineBeamsSpec
};


function ensurePickingData(device: GPUDevice, components: ComponentConfig[], ro: RenderObject) {
  if (!ro.pickingDataStale) return;
  // We'll work directly with the cached picking data to avoid an extra allocation and copy
  const pickingData = ro.cachedPickingData;

  // Partition the sortedIndices array if it exists, otherwise create sequential indices
  // Use the cached partitions if available to reduce allocations
  const componentPartitions = ro.cachedPartitions ||
  createSequentialIndices(ro.componentOffsets, undefined);
  ro.cachedPartitions = ro.cachedPartitions || componentPartitions;

  // Store the partitions for future reuse
  ro.cachedPartitions = componentPartitions;

  // For each component, use the partitioned indices to build picking data
  let dataOffset = 0;
  for (let i = 0; i < ro.componentOffsets.length; i++) {
    const offset = ro.componentOffsets[i];
    const component = components[offset.componentIdx];
    const count = offset.count;
    const floatsPerInstance = ro.spec.floatsPerPicking;
    const componentFloats = count * floatsPerInstance;

    // Get the pre-partitioned indices for this component
    const componentIndices = componentPartitions[i];

    // Create a view into the picking data array for this component
    const componentView = new Float32Array(
      pickingData.buffer,
      pickingData.byteOffset + dataOffset * Float32Array.BYTES_PER_ELEMENT,
      componentFloats
    );

    // Build picking data for this component
    const baseID = offset.start;
    buildPickingData(component, ro.spec, componentView, baseID, componentIndices);

    dataOffset += componentFloats;
  }

  // Write picking data to GPU
  const pickingInfo = ro.pickingVertexBuffers[1] as BufferInfo;
  device.queue.writeBuffer(
    pickingInfo.buffer,
    pickingInfo.offset,
    pickingData.buffer,
    pickingData.byteOffset,
    pickingData.byteLength
  );

  ro.pickingDataStale = false;
}

function computeUniforms(containerWidth: number, containerHeight: number, camState: CameraState): {
  aspect: number,
  view: glMatrix.mat4,
  proj: glMatrix.mat4,
  mvp: glMatrix.mat4,
  forward: glMatrix.vec3,
  right: glMatrix.vec3,
  camUp: glMatrix.vec3,
  lightDir: glMatrix.vec3
} {
    const aspect = containerWidth / containerHeight;
    const view = glMatrix.mat4.lookAt(
      glMatrix.mat4.create(),
      camState.position,
      camState.target,
      camState.up
    );

    const proj = glMatrix.mat4.perspective(
      glMatrix.mat4.create(),
      glMatrix.glMatrix.toRadian(camState.fov),
      aspect,
      camState.near,
      camState.far
    );

    const mvp = glMatrix.mat4.multiply(
      glMatrix.mat4.create(),
      proj,
      view
    );

    // Compute camera vectors for lighting
    const forward = glMatrix.vec3.sub(glMatrix.vec3.create(), camState.target, camState.position);
    const right = glMatrix.vec3.cross(glMatrix.vec3.create(), forward, camState.up);
    glMatrix.vec3.normalize(right, right);

    const camUp = glMatrix.vec3.cross(glMatrix.vec3.create(), right, forward);
    glMatrix.vec3.normalize(camUp, camUp);
    glMatrix.vec3.normalize(forward, forward);

    // Compute light direction in camera space
    const lightDir = glMatrix.vec3.create();
    glMatrix.vec3.scaleAndAdd(lightDir, lightDir, right, LIGHTING.DIRECTION.RIGHT);
    glMatrix.vec3.scaleAndAdd(lightDir, lightDir, camUp, LIGHTING.DIRECTION.UP);
    glMatrix.vec3.scaleAndAdd(lightDir, lightDir, forward, LIGHTING.DIRECTION.FORWARD);
    glMatrix.vec3.normalize(lightDir, lightDir);

    return {aspect, view, proj, mvp, forward, right, camUp, lightDir}
}

function renderPass({
  device,
  context,
  depthTexture,
  renderObjects,
  uniformBindGroup,
  onRenderComplete
}: {
  device: GPUDevice;
  context: GPUCanvasContext;
  depthTexture: GPUTexture | null;
  renderObjects: RenderObject[];
  uniformBindGroup: GPUBindGroup;
  onRenderComplete: () => void;
}) {

  function isValidRenderObject(ro: RenderObject): ro is Required<Pick<RenderObject, 'pipeline' | 'vertexBuffers' | 'instanceCount'>> & {
  vertexBuffers: [GPUBuffer, BufferInfo];
} & RenderObject {
  return (
    ro.pipeline !== undefined &&
    Array.isArray(ro.vertexBuffers) &&
    ro.vertexBuffers.length === 2 &&
    ro.vertexBuffers[0] !== undefined &&
    ro.vertexBuffers[1] !== undefined &&
    'buffer' in ro.vertexBuffers[1] &&
    'offset' in ro.vertexBuffers[1] &&
    (ro.indexBuffer !== undefined || ro.vertexCount !== undefined) &&
    typeof ro.instanceCount === 'number' &&
    ro.instanceCount > 0
  );
}

  // Begin render pass
  const cmd = device.createCommandEncoder();
  const pass = cmd.beginRenderPass({
    colorAttachments: [{
      view: context.getCurrentTexture().createView(),
      clearValue: { r: 0, g: 0, b: 0, a: 1 },
      loadOp: 'clear',
      storeOp: 'store'
    }],
    depthStencilAttachment: depthTexture ? {
      view: depthTexture.createView(),
      depthClearValue: 1.0,
      depthLoadOp: 'clear',
      depthStoreOp: 'store'
    } : undefined
  });

  // Draw each object
  for(const ro of renderObjects) {
    if (!isValidRenderObject(ro)) {
      continue;
    }

    pass.setPipeline(ro.pipeline);
    pass.setBindGroup(0, uniformBindGroup);
    pass.setVertexBuffer(0, ro.vertexBuffers[0]);
    const instanceInfo = ro.vertexBuffers[1];
    pass.setVertexBuffer(1, instanceInfo.buffer, instanceInfo.offset);
    if(ro.indexBuffer) {
      pass.setIndexBuffer(ro.indexBuffer, 'uint16');
      pass.drawIndexed(ro.indexCount ?? 0, ro.instanceCount ?? 1);
    } else {
      pass.draw(ro.vertexCount ?? 0, ro.instanceCount ?? 1);
    }
  }

  pass.end();
  device.queue.submit([cmd.finish()]);
  device.queue.onSubmittedWorkDone().then(onRenderComplete)


}

function computeUniformData(containerWidth: number, containerHeight: number, camState: CameraState): Float32Array {
  const {mvp, right, camUp, lightDir} = computeUniforms(containerWidth, containerHeight, camState)
  return new Float32Array([
    ...Array.from(mvp),
    right[0], right[1], right[2], 0,  // pad to vec4
    camUp[0], camUp[1], camUp[2], 0,  // pad to vec4
    lightDir[0], lightDir[1], lightDir[2], 0,  // pad to vec4
    camState.position[0], camState.position[1], camState.position[2], 0  // Add camera position
  ]);
}

// Helper to check if camera has moved significantly
function hasCameraMoved(current: glMatrix.vec3, last: glMatrix.vec3 | undefined): boolean {
  if (!last) return true;
  const dx = current[0] - last[0];
  const dy = current[1] - last[1];
  const dz = current[2] - last[2];
  return (dx*dx + dy*dy + dz*dz) > 0.0001;
}

/**
 * Sorts indices by distance (furthest to closest) for correct alpha blending
 */
function sortIndicesByDistance(
  indices: Uint32Array,
  distances: Float32Array,
  count: number
): void {
  // Create a temporary array of index/distance pairs for sorting
  const pairs = new Array(count);
  for (let i = 0; i < count; i++) {
    pairs[i] = { index: indices[i], distance: distances[i] };
  }

  // Sort by distance (furthest to closest)
  pairs.sort((a, b) => {
    // If distances are equal, maintain relative order based on original indices
    const diff = b.distance - a.distance;
    return diff !== 0 ? diff : a.index - b.index;
  });

  // Copy sorted indices back to the original array
  for (let i = 0; i < count; i++) {
    indices[i] = pairs[i].index;
  }
}

/**
 * Partitions sorted indices by component
 */
function partitionSortedIndices(
  sortedIndices: Uint32Array,
  offsets: ComponentOffset[]
): Uint32Array[] {
  return partitionIndices(sortedIndices, offsets);
}

function updateInstanceSorting(
  ro: RenderObject,
  components: ComponentConfig[],
  cameraPos: glMatrix.vec3
): void {
  // Skip if no alpha components
  const hasAlphaComponents = ro.componentOffsets.some(offset =>
    componentHasAlpha(components[offset.componentIdx])
  );
  if (!hasAlphaComponents) return;

  // Get total instance count
  const totalCount = ro.componentOffsets.reduce((sum, offset) => sum + offset.count, 0);

  // Check if we need to reallocate arrays (only if count changed)
  const needsReallocation = !ro.sortedIndices || ro.sortedIndices.length !== totalCount ||
                           !ro.distances || ro.distances.length !== totalCount;

  // Ensure we have arrays of the right size
  if (needsReallocation) {
    ro.sortedIndices = new Uint32Array(totalCount);
    ro.distances = new Float32Array(totalCount);
    // Clear cached partitions since component counts changed
    ro.cachedPartitions = undefined;
  }

  // Calculate distances and initialize indices for each component
  let globalIdx = 0;
  for (const offset of ro.componentOffsets) {
    const component = components[offset.componentIdx];
    const spec = ro.spec;
    const centers = spec.getCenters(component);
    const instanceCount = offset.count;

    const elementCount = spec.getElementCount(component);

    const instancesPerElement = spec.instancesPerElement || 1;

    // For each element in this component
    for (let elemIdx = 0; elemIdx < elementCount; elemIdx++) {
      // Calculate distance to camera once per element
      const baseIdx = elemIdx * 3;
      const x = centers[baseIdx] - cameraPos[0];
      const y = centers[baseIdx + 1] - cameraPos[1];
      const z = centers[baseIdx + 2] - cameraPos[2];
      const distanceSq = x * x + y * y + z * z;

      // For each instance of this element
      for (let instOffset = 0; instOffset < instancesPerElement; instOffset++) {
        const instanceIdx = elemIdx * instancesPerElement + instOffset;
        if (instanceIdx >= instanceCount) break; // Safety check

        const idx = globalIdx + instanceIdx;

        // Store the global index
        ro.sortedIndices![idx] = offset.start + instanceIdx;

        // Use the same distance for all instances of the same element
        ro.distances![idx] = distanceSq;
      }
    }

    globalIdx += instanceCount;
  }

  // Sort indices by distance (furthest to closest for correct alpha blending)
  sortIndicesByDistance(ro.sortedIndices!, ro.distances!, totalCount);

  // Partition the sorted indices by component
  ro.cachedPartitions = partitionSortedIndices(ro.sortedIndices!, ro.componentOffsets);
}

/**
 * Efficiently partitions global sorted indices into component-specific arrays in a single pass,
 * reusing pre-allocated buffers when possible to reduce garbage collection pressure.
 *
 * @param sortedIndices Global sorted indices
 * @param offsets Component offsets (assumed sorted by start)
 * @param existingPartitions Optional pre-allocated array of Uint32Arrays to reuse
 * @returns An array of Uint32Arrays, one per component
 */
function updatePartitions(
  sortedIndices: Uint32Array,
  offsets: ComponentOffset[],
  existingPartitions?: Uint32Array[]
): Uint32Array[] {
  const result: Uint32Array[] = [];

  // Pre-allocate result arrays or reuse existing ones if sizes match
  for (let j = 0; j < offsets.length; j++) {
    const { count } = offsets[j];
    // If we already have a partition with the correct length, reuse it
    if (existingPartitions && existingPartitions[j] && existingPartitions[j].length === count) {
      result[j] = existingPartitions[j];
    } else {
      result[j] = new Uint32Array(count);
    }
  }

  // Maintain an index pointer for each component
  const writeIndices = new Uint32Array(offsets.length);

  // For each global index, find which component offset it belongs to
  for (let i = 0; i < sortedIndices.length; i++) {
    const globalIdx = sortedIndices[i];

    // Find the component this index belongs to
    // For a small number of components, a simple linear scan is efficient
    for (let j = 0; j < offsets.length; j++) {
      const { start, count } = offsets[j];
      if (globalIdx >= start && globalIdx < start + count) {
        // Store the relative index in the appropriate partition
        result[j][writeIndices[j]++] = globalIdx - start;
        break;
      }
    }
  }

  return result;
}

/**
 * Creates or reuses arrays of sequential indices for each component.
 * This is used when no sorting is needed.
 *
 * @param offsets Component offsets
 * @param existingPartitions Optional pre-allocated arrays to reuse
 * @returns An array of Uint32Arrays with sequential indices
 */
function createSequentialIndices(
  offsets: ComponentOffset[],
  existingPartitions?: Uint32Array[]
): Uint32Array[] {
  const result: Uint32Array[] = [];

  for (let j = 0; j < offsets.length; j++) {
    const { count } = offsets[j];

    // If we already have a partition with the correct length, reuse it
    if (existingPartitions && existingPartitions[j] && existingPartitions[j].length === count) {
      const indices = existingPartitions[j];
      // Fill with sequential indices
      for (let i = 0; i < count; i++) {
        indices[i] = i;
      }
      result[j] = indices;
    } else {
      // Create a new array with sequential indices
      const indices = new Uint32Array(count);
      for (let i = 0; i < count; i++) {
        indices[i] = i;
      }
      result[j] = indices;
    }
  }

  return result;
}

export function getGeometryResource(resources: GeometryResources, type: keyof GeometryResources): GeometryResource {
  const resource = resources[type];
  if (!resource) {
    throw new Error(`No geometry resource found for type ${type}`);
  }
  return resource;
}



export function SceneInner({
  components,
  containerWidth,
  containerHeight,
  style,
  camera: controlledCamera,
  defaultCamera,
  onCameraChange,
  onFrameRendered,
  onReady
}: SceneInnerProps) {
  const $state = useContext($StateContext);

  // We'll store references to the GPU + other stuff in a ref object
  const gpuRef = useRef<{
    device: GPUDevice;
    context: GPUCanvasContext;
    uniformBuffer: GPUBuffer;
    uniformBindGroup: GPUBindGroup;
    bindGroupLayout: GPUBindGroupLayout;
    depthTexture: GPUTexture | null;
    pickTexture: GPUTexture | null;
    pickDepthTexture: GPUTexture | null;
    readbackBuffer: GPUBuffer;
    lastCameraPosition?: glMatrix.vec3;

    renderObjects: RenderObject[];
    pipelineCache: Map<string, PipelineCacheEntry>;
    dynamicBuffers: DynamicBuffers | null;
    resources: GeometryResources;
    renderedComponents?: ComponentConfig[];
  } | null>(null);

  const [internalCamera, setInternalCamera] = useState<CameraState>(() => {
      return createCameraState(defaultCamera);
  });

  // Use the appropriate camera state based on whether we're controlled or not
  const activeCameraRef = useRef<CameraState | null>(null);
  useMemo(() => {
    let nextCamera: CameraState;
    if (controlledCamera) {
      nextCamera = createCameraState(controlledCamera);
    } else {
      nextCamera = internalCamera;
    }
    activeCameraRef.current = nextCamera;
    return nextCamera;
  }, [controlledCamera, internalCamera]);

  const handleCameraUpdate = useCallback((updateFn: (camera: CameraState) => CameraState) => {
    const newCameraState = updateFn(activeCameraRef.current!);

    if (controlledCamera) {
        onCameraChange?.(createCameraParams(newCameraState));
    } else {
        setInternalCamera(newCameraState);
        onCameraChange?.(createCameraParams(newCameraState));
    }
  }, [controlledCamera, onCameraChange]);

  // Create a render callback for the canvas snapshot system
  // This function is called during PDF export to render the 3D scene to a texture
  // that can be captured as a static image
  const renderToTexture = useCallback((targetTexture: GPUTexture, depthTexture: GPUTexture | null) => {
    if (!gpuRef.current) return;
    const { device, uniformBindGroup, renderObjects } = gpuRef.current;

    // Reuse the existing renderPass function with a temporary context
    // that redirects rendering to our snapshot texture
    const tempContext = {
      getCurrentTexture: () => targetTexture
    } as GPUCanvasContext;

    renderPass({
      device,
      context: tempContext,
      depthTexture: depthTexture || null,
      renderObjects,
      uniformBindGroup,
      onRenderComplete: () => {}
    });
  }, [containerWidth, containerHeight, activeCameraRef.current!]);


  const { canvasRef } = useCanvasSnapshot(
    gpuRef.current?.device,
    gpuRef.current?.context,
    renderToTexture
  );

  const [isReady, setIsReady] = useState(false);

  const pickingLockRef = useRef(false);

  const lastHoverState = useRef<{componentIdx: number, instanceIdx: number} | null>(null);

  const renderObjectCache = useRef<RenderObjectCache>({});

  /******************************************************
   * A) initWebGPU
   ******************************************************/
  const initWebGPU = useCallback(async()=>{
    if(!canvasRef.current) return;
    if(!navigator.gpu) {
      console.error("WebGPU not supported in this browser.");
      return;
    }
    try {
      const adapter = await navigator.gpu.requestAdapter();
      if(!adapter) throw new Error("No GPU adapter found");
      const device = await adapter.requestDevice().catch(err => {
        console.error("Failed to create WebGPU device:", err);
        throw err;
      });

      // Add error handling for uncaptured errors
      device.addEventListener('uncapturederror', ((event: Event) => {
        if (event instanceof GPUUncapturedErrorEvent) {
          console.error('Uncaptured WebGPU error:', event.error);
          // Log additional context about where the error occurred
          console.error('Error source:', event.error.message);
        }
      }) as EventListener);

      const context = canvasRef.current.getContext('webgpu') as GPUCanvasContext;
      const format = navigator.gpu.getPreferredCanvasFormat();
      context.configure({ device, format, alphaMode:'premultiplied' });

      // Create all the WebGPU resources
      const bindGroupLayout = device.createBindGroupLayout({
        entries: [{
          binding: 0,
          visibility: GPUShaderStage.VERTEX | GPUShaderStage.FRAGMENT,
          buffer: {type:'uniform'}
        }]
      });

      const uniformBufferSize=128;
      const uniformBuffer=device.createBuffer({
        size: uniformBufferSize,
        usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST
      });

      const uniformBindGroup = device.createBindGroup({
        layout: bindGroupLayout,
        entries: [{ binding:0, resource:{ buffer:uniformBuffer } }]
      });

      const readbackBuffer = device.createBuffer({
        size: 256,
        usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ,
        label: 'Picking readback buffer'
      });

      gpuRef.current = {
        device,
        context,
        uniformBuffer,
        uniformBindGroup,
        bindGroupLayout,
        depthTexture: null,
        pickTexture: null,
        pickDepthTexture: null,
        readbackBuffer,
        renderObjects: [],
        pipelineCache: new Map(),
        dynamicBuffers: null,
        resources: {
          PointCloud: null,
          Ellipsoid: null,
          EllipsoidAxes: null,
          Cuboid: null,
          LineBeams: null
        },
      };

      // Now initialize geometry resources
      initGeometryResources(device, gpuRef.current.resources);

      setIsReady(true);
    } catch(err){
      console.error("Error initializing WebGPU:", err);
    }
  },[]);

  /******************************************************
   * B) Depth & Pick textures
   ******************************************************/
  const createOrUpdateDepthTexture = useCallback(() => {
    if(!gpuRef.current || !canvasRef.current) return;
    const { device, depthTexture } = gpuRef.current;

    // Get the actual canvas size
        const canvas = canvasRef.current;
        const displayWidth = canvas.width;
        const displayHeight = canvas.height;

        if(depthTexture) depthTexture.destroy();
        const dt = device.createTexture({
            size: [displayWidth, displayHeight],
            format: 'depth24plus',
            usage: GPUTextureUsage.RENDER_ATTACHMENT
        });
        gpuRef.current.depthTexture = dt;
  }, []);

  const createOrUpdatePickTextures = useCallback(() => {
    if(!gpuRef.current || !canvasRef.current) return;
    const { device, pickTexture, pickDepthTexture } = gpuRef.current;

    // Get the actual canvas size
        const canvas = canvasRef.current;
        const displayWidth = canvas.width;
        const displayHeight = canvas.height;

        if(pickTexture) pickTexture.destroy();
        if(pickDepthTexture) pickDepthTexture.destroy();

        const colorTex = device.createTexture({
            size: [displayWidth, displayHeight],
            format: 'rgba8unorm',
            usage: GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.COPY_SRC
        });
        const depthTex = device.createTexture({
            size: [displayWidth, displayHeight],
            format: 'depth24plus',
            usage: GPUTextureUsage.RENDER_ATTACHMENT
        });
        gpuRef.current.pickTexture = colorTex;
        gpuRef.current.pickDepthTexture = depthTex;
  }, []);


  type ComponentType = ComponentConfig['type'];

  interface TypeInfo {
    offsets: number[];
    counts: number[];
    indices: number[];
    totalSize: number;
    totalCount: number;
    components: ComponentConfig[];
  }

  // Update the collectTypeData function signature
  function collectTypeData(components: ComponentConfig[]): Map<ComponentType, TypeInfo> {
    const typeArrays = new Map<ComponentType, TypeInfo>();

    // Single pass through components
    components.forEach((comp, idx) => {
      const spec = primitiveRegistry[comp.type];
      if (!spec) return;

      // Get the element count and instance count
      const elementCount = spec.getElementCount(comp);
      const instancesPerElement = spec.instancesPerElement || 1;
      const instanceCount = elementCount * instancesPerElement;

      if (instanceCount === 0) return;

      // Just allocate the array without building data
      const floatsPerInstance = spec.floatsPerInstance;
      const size = instanceCount * floatsPerInstance * 4; // 4 bytes per float

      let typeInfo = typeArrays.get(comp.type);
      if (!typeInfo) {
        typeInfo = {
          totalCount: 0,
          totalSize: 0,
          components: [],
          indices: [],
          offsets: [],
          counts: []
        };
        typeArrays.set(comp.type, typeInfo);
      }

      typeInfo.components.push(comp);
      typeInfo.indices.push(idx);
      typeInfo.offsets.push(typeInfo.totalSize);
      typeInfo.counts.push(instanceCount);
      typeInfo.totalCount += instanceCount;
      typeInfo.totalSize += size;
    });

    return typeArrays;
  }

  // Update buildRenderObjects to include caching
  function buildRenderObjects(components: ComponentConfig[]): RenderObject[] {
    if(!gpuRef.current) return [];
    const { device, bindGroupLayout, pipelineCache, resources } = gpuRef.current;

    // Clear out unused cache entries
    Object.keys(renderObjectCache.current).forEach(type => {
      if (!components.some(c => c.type === type)) {
        delete renderObjectCache.current[type];
      }
    });

    // Track global start index for all components
    let globalStartIndex = 0;

    // Collect render data using helper
    const typeArrays = collectTypeData(components);

    // Calculate total buffer sizes needed
    let totalRenderSize = 0;
    let totalPickingSize = 0;
    typeArrays.forEach((info: TypeInfo, type: ComponentType) => {
      const spec = primitiveRegistry[type];
      if (!spec) return;

      // Calculate total instance count for this type
      const totalInstanceCount = info.counts.reduce((sum, count) => sum + count, 0);

      // Calculate total size needed for all instances of this type
      const floatsPerInstance = spec.floatsPerInstance;
      const renderStride = Math.ceil(floatsPerInstance * 4);  // 4 bytes per float
      totalRenderSize += align16(totalInstanceCount * renderStride);
      totalPickingSize += align16(totalInstanceCount * spec.floatsPerPicking * 4);
    });

    // Create or recreate dynamic buffers if needed
    if (!gpuRef.current.dynamicBuffers ||
        gpuRef.current.dynamicBuffers.renderBuffer.size < totalRenderSize ||
        gpuRef.current.dynamicBuffers.pickingBuffer.size < totalPickingSize) {

      gpuRef.current.dynamicBuffers?.renderBuffer.destroy();
      gpuRef.current.dynamicBuffers?.pickingBuffer.destroy();

      const renderBuffer = device.createBuffer({
        size: totalRenderSize,
        usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
        mappedAtCreation: false
      });

      const pickingBuffer = device.createBuffer({
        size: totalPickingSize,
        usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
        mappedAtCreation: false
      });

      gpuRef.current.dynamicBuffers = {
        renderBuffer,
        pickingBuffer,
        renderOffset: 0,
        pickingOffset: 0
      };
    }
    const dynamicBuffers = gpuRef.current.dynamicBuffers!;

    // Reset buffer offsets
    dynamicBuffers.renderOffset = 0;
    dynamicBuffers.pickingOffset = 0;

    const validRenderObjects: RenderObject[] = [];

    // Create or update render objects and write buffer data
    typeArrays.forEach((info: TypeInfo, type: ComponentType) => {
      const spec = primitiveRegistry[type];
      if (!spec) return;

      try {
        // Ensure 4-byte alignment for all offsets
        const renderOffset = align16(dynamicBuffers.renderOffset);
        const pickingOffset = align16(dynamicBuffers.pickingOffset);

        // Calculate strides
        const renderInstanceFloats = spec.floatsPerInstance;
        const pickingInstanceFloats = spec.floatsPerPicking;
        const renderStride = renderInstanceFloats * 4;
        const pickingStride = pickingInstanceFloats * 4;

        // Get total instance count for this type
        const totalInstanceCount = info.totalCount;

        // Try to get existing render object
        let renderObject = renderObjectCache.current[type];
        const needNewRenderObject = !renderObject || renderObject.lastRenderCount !== totalInstanceCount;

        // Create or reuse render data arrays
        let renderData: Float32Array;
        let pickingData: Float32Array;

        if (needNewRenderObject) {
          renderData = new Float32Array(renderInstanceFloats * totalInstanceCount);
          pickingData = new Float32Array(pickingInstanceFloats * totalInstanceCount);
        } else {
          renderData = renderObject.cachedRenderData;
          pickingData = renderObject.cachedPickingData;
        }

        // Copy component data into combined render data array
        let renderDataOffset = 0;
        for (let i = 0; i < info.counts.length; i++) {
          const componentCount = info.counts[i];
          const componentFloats = componentCount * renderInstanceFloats;

          // Create a view into the combined array for this component
          const componentView = new Float32Array(
            renderData.buffer,
            renderData.byteOffset + renderDataOffset * Float32Array.BYTES_PER_ELEMENT,
            componentFloats
          );

          // Build render data directly into the view

          buildRenderData(info.components[i], spec, componentView);

          renderDataOffset += componentFloats;
        }

        // Write the combined render data to the GPU buffer
        device.queue.writeBuffer(
          dynamicBuffers.renderBuffer,
          renderOffset,
          renderData.buffer,
          renderData.byteOffset,
          renderData.byteLength
        );

        // Get or create pipeline
        const pipeline = spec.getRenderPipeline(device, bindGroupLayout, pipelineCache);
        if (!pipeline) return;

        // Get picking pipeline
        const pickingPipeline = spec.getPickingPipeline(device, bindGroupLayout, pipelineCache);
        if (!pickingPipeline) return;

        // Build component offsets for this type's components
        const typeComponentOffsets: ComponentOffset[] = [];
        let typeStartIndex = globalStartIndex;
        info.indices.forEach((componentIdx, i) => {
          const componentCount = info.counts[i];
          typeComponentOffsets.push({
            componentIdx,
            start: typeStartIndex,
            count: componentCount
          });
          typeStartIndex += componentCount;
        });
        globalStartIndex = typeStartIndex;

        // Create or update buffer info
        const bufferInfo = {
          buffer: dynamicBuffers.renderBuffer,
          offset: renderOffset,
          stride: renderStride
        };
        const pickingBufferInfo = {
          buffer: dynamicBuffers.pickingBuffer,
          offset: pickingOffset,
          stride: pickingStride
        };

        if (needNewRenderObject) {
          // Create new render object with all the required resources
          const geometryResource = getGeometryResource(resources, type);
          renderObject = {
            pipeline,
            pickingPipeline,
            vertexBuffers: [
              geometryResource.vb,
              bufferInfo
            ],
            indexBuffer: geometryResource.ib,
            indexCount: geometryResource.indexCount,
            instanceCount: totalInstanceCount,
            pickingVertexBuffers: [
              geometryResource.vb,
              pickingBufferInfo
            ],
            pickingIndexBuffer: geometryResource.ib,
            pickingIndexCount: geometryResource.indexCount,
            pickingVertexCount: geometryResource.vertexCount ?? 0,
            pickingInstanceCount: totalInstanceCount,
            pickingDataStale: true,
            componentIndex: info.indices[0],
            cachedRenderData: renderData,
            cachedPickingData: pickingData,
            lastRenderCount: totalInstanceCount,
            componentOffsets: typeComponentOffsets,
            spec: spec
          };
          renderObjectCache.current[type] = renderObject;
        } else {
          // Update existing render object with new buffer info and state
          renderObject.vertexBuffers[1] = bufferInfo;
          renderObject.pickingVertexBuffers[1] = pickingBufferInfo;
          renderObject.instanceCount = totalInstanceCount;
          renderObject.pickingInstanceCount = totalInstanceCount;
          renderObject.componentIndex = info.indices[0];
          renderObject.componentOffsets = typeComponentOffsets;
          renderObject.spec = spec;
          renderObject.pickingDataStale = true;
        }

        validRenderObjects.push(renderObject);

        // Update buffer offsets ensuring alignment
        dynamicBuffers.renderOffset = renderOffset + align16(renderData.byteLength);
        dynamicBuffers.pickingOffset = pickingOffset + align16(totalInstanceCount * spec.floatsPerPicking * 4);

      } catch (error) {
        console.error(`Error creating render object for type ${type}:`, error);
      }
    });

    return validRenderObjects;
  }

  /******************************************************
   * C) Render pass (single call, no loop)
   ******************************************************/


  const renderFrame = useCallback(function renderFrameInner(camState: CameraState, components?: ComponentConfig[]) {
    if(!gpuRef.current) return;

    const onRenderComplete = $state.beginUpdate("impl3d/renderFrame")

    components = components || gpuRef.current.renderedComponents;
    const componentsChanged = gpuRef.current.renderedComponents !== components;

    if (componentsChanged) {
      gpuRef.current.renderObjects = buildRenderObjects(components!);
      gpuRef.current.renderedComponents = components;
    }

    const {
      device, context, uniformBuffer, uniformBindGroup,
      renderObjects, depthTexture
    } = gpuRef.current;

    const cameraMoved = hasCameraMoved(camState.position, gpuRef.current.lastCameraPosition);
    gpuRef.current.lastCameraPosition = camState.position;

    // Update data for objects that need it
    renderObjects.forEach(ro => {
      const needsSorting = ro.componentOffsets.some(offset =>
        componentHasAlpha(components![offset.componentIdx])
      );

      const needsInitialBuild = !ro.lastRenderCount;
      const needsUpdate = needsSorting && (componentsChanged || cameraMoved);

      // Skip if no update needed
      if (!needsInitialBuild && !needsUpdate) return;

      // Update sorting if needed
      if (needsSorting) {
        updateInstanceSorting(ro, components!, camState.position);
      }

      ro.lastRenderCount = ro.componentOffsets.reduce((sum, offset) => sum + offset.count, 0);

      // We'll work directly with the cached render data to avoid an extra allocation and copy
      const renderData = ro.cachedRenderData;

      // Get indices to use for building render data
      let componentPartitions: Uint32Array[];
      if (needsSorting && ro.sortedIndices) {
        // Partition the sortedIndices array into component-specific arrays
        componentPartitions = updatePartitions(ro.sortedIndices, ro.componentOffsets, ro.cachedPartitions);
        // Store the partitions for future reuse
        ro.cachedPartitions = componentPartitions;
      } else {
        // Use sequential indices if no sorting needed
        componentPartitions = createSequentialIndices(ro.componentOffsets, ro.cachedPartitions);
        ro.cachedPartitions = componentPartitions;
      }

      // Build render data for each component
      let dataOffset = 0;
      for (let i = 0; i < ro.componentOffsets.length; i++) {
        const offset = ro.componentOffsets[i];
        const component = components![offset.componentIdx];
        const count = offset.count;
        const floatsPerInstance = ro.spec.floatsPerInstance;
        const componentFloats = count * floatsPerInstance;

        // Create a view into the render data array for this component
        const componentView = new Float32Array(
          renderData.buffer,
          renderData.byteOffset + dataOffset * Float32Array.BYTES_PER_ELEMENT,
          componentFloats
        );

        // Build render data for this component
        buildRenderData(component, ro.spec, componentView, componentPartitions[i]);

        dataOffset += componentFloats;
      }

      ro.pickingDataStale = true;

      // Write render data to GPU buffer
      const vertexInfo = ro.vertexBuffers[1] as BufferInfo;
      device.queue.writeBuffer(
        vertexInfo.buffer,
        vertexInfo.offset,
        renderData.buffer,
        renderData.byteOffset,
        renderData.byteLength
      );
    });

    const uniformData = computeUniformData(containerWidth, containerHeight, camState);
    device.queue.writeBuffer(uniformBuffer, 0, uniformData);

    renderPass({device, context, depthTexture, renderObjects, uniformBindGroup, onRenderComplete})

    onFrameRendered?.(performance.now());
  }, [containerWidth, containerHeight, onFrameRendered, components]);


  /******************************************************
   * D) Pick pass (on hover/click)
   ******************************************************/
  async function pickAtScreenXY(screenX: number, screenY: number, mode: 'hover'|'click') {
    if(!gpuRef.current || !canvasRef.current || pickingLockRef.current) return;
    const pickingId = Date.now();
    const currentPickingId = pickingId;
    pickingLockRef.current = true;

    try {
      const {
        device, pickTexture, pickDepthTexture, readbackBuffer,
        uniformBindGroup, renderObjects
      } = gpuRef.current;
      if(!pickTexture || !pickDepthTexture || !readbackBuffer) return;
      if (currentPickingId !== pickingId) return;

      // Ensure picking data is ready for all objects
      for (let i = 0; i < renderObjects.length; i++) {
        ensurePickingData(gpuRef.current.device, gpuRef.current.renderedComponents!, renderObjects[i]);
      }

      // Convert screen coordinates to device pixels
      const dpr = window.devicePixelRatio || 1;
      const pickX = Math.floor(screenX * dpr);
      const pickY = Math.floor(screenY * dpr);
      const displayWidth = Math.floor(containerWidth * dpr);
      const displayHeight = Math.floor(containerHeight * dpr);

      if(pickX < 0 || pickY < 0 || pickX >= displayWidth || pickY >= displayHeight) {
        if(mode === 'hover') handleHoverID(0);
        return;
      }

      const cmd = device.createCommandEncoder({label: 'Picking encoder'});
      const passDesc: GPURenderPassDescriptor = {
        colorAttachments:[{
          view: pickTexture.createView(),
          clearValue:{r:0,g:0,b:0,a:1},
          loadOp:'clear',
          storeOp:'store'
        }],
        depthStencilAttachment:{
          view: pickDepthTexture.createView(),
          depthClearValue:1.0,
          depthLoadOp:'clear',
          depthStoreOp:'store'
        }
      };
      const pass = cmd.beginRenderPass(passDesc);
      pass.setBindGroup(0, uniformBindGroup);

      for(const ro of renderObjects) {
        if (!ro.pickingPipeline || !ro.pickingVertexBuffers[0] || !ro.pickingVertexBuffers[1]) {
          continue;
        }

        pass.setPipeline(ro.pickingPipeline);
        pass.setBindGroup(0, uniformBindGroup);

        // Set geometry buffer
        pass.setVertexBuffer(0, ro.pickingVertexBuffers[0]);

        // Set instance buffer
        const instanceInfo = ro.pickingVertexBuffers[1] as BufferInfo;
        pass.setVertexBuffer(1, instanceInfo.buffer, instanceInfo.offset);

        // Draw with indices if we have them, otherwise use vertex count
        if(ro.pickingIndexBuffer) {
          pass.setIndexBuffer(ro.pickingIndexBuffer, 'uint16');
          pass.drawIndexed(ro.pickingIndexCount ?? 0, ro.instanceCount ?? 1);
        } else if (ro.pickingVertexCount) {
          pass.draw(ro.pickingVertexCount, ro.instanceCount ?? 1);
        }
      }

      pass.end();

      cmd.copyTextureToBuffer(
        {texture: pickTexture, origin:{x:pickX,y:pickY}},
        {buffer: readbackBuffer, bytesPerRow:256, rowsPerImage:1},
        [1,1,1]
      );
      device.queue.submit([cmd.finish()]);

      if (currentPickingId !== pickingId) return;
      await readbackBuffer.mapAsync(GPUMapMode.READ);
      if (currentPickingId !== pickingId) {
        readbackBuffer.unmap();
        return;
      }
      const arr = new Uint8Array(readbackBuffer.getMappedRange());
      const r=arr[0], g=arr[1], b=arr[2];
      readbackBuffer.unmap();
      const pickedID = (b<<16)|(g<<8)|r;

      if(mode==='hover'){
        handleHoverID(pickedID);
      } else {
        handleClickID(pickedID);
      }
    } finally {
      pickingLockRef.current = false;
    }
  }

  function handleHoverID(pickedID: number) {
    if (!gpuRef.current) return;

    // Get combined instance index
    const combinedIndex = unpackID(pickedID);
    if (combinedIndex === null) {
        // Clear previous hover if it exists
        if (lastHoverState.current) {
            const prevComponent = components[lastHoverState.current.componentIdx];
            prevComponent?.onHover?.(null);
            lastHoverState.current = null;
        }
        return;
    }

    // Find which component this instance belongs to by searching through all render objects
    let newHoverState = null;
    for (const ro of gpuRef.current.renderObjects) {
        // Skip if no component offsets
        if (!ro?.componentOffsets) continue;

        // Check each component in this render object
        for (const offset of ro.componentOffsets) {
            if (combinedIndex >= offset.start && combinedIndex < offset.start + offset.count) {
                newHoverState = {
                    componentIdx: offset.componentIdx,
                    instanceIdx: combinedIndex - offset.start
                };
                break;
            }
        }
        if (newHoverState) break;  // Found the matching component
    }

    // If hover state hasn't changed, do nothing
    if ((!lastHoverState.current && !newHoverState) ||
        (lastHoverState.current && newHoverState &&
         lastHoverState.current.componentIdx === newHoverState.componentIdx &&
         lastHoverState.current.instanceIdx === newHoverState.instanceIdx)) {
        return;
    }

    // Clear previous hover if it exists
    if (lastHoverState.current) {
        const prevComponent = components[lastHoverState.current.componentIdx];
        prevComponent?.onHover?.(null);
    }

    // Set new hover if it exists
    if (newHoverState) {
        const { componentIdx, instanceIdx } = newHoverState;
        if (componentIdx >= 0 && componentIdx < components.length) {
            components[componentIdx].onHover?.(instanceIdx);
        }
    }

    // Update last hover state
    lastHoverState.current = newHoverState;
  }

  function handleClickID(pickedID: number) {
    if (!gpuRef.current) return;

    // Get combined instance index
    const combinedIndex = unpackID(pickedID);
    if (combinedIndex === null) return;

    // Find which component this instance belongs to by searching through all render objects
    for (const ro of gpuRef.current.renderObjects) {
        // Skip if no component offsets
        if (!ro?.componentOffsets) continue;

        // Check each component in this render object
        for (const offset of ro.componentOffsets) {
            if (combinedIndex >= offset.start && combinedIndex < offset.start + offset.count) {
                const componentIdx = offset.componentIdx;
                const instanceIdx = combinedIndex - offset.start;
                if (componentIdx >= 0 && componentIdx < components.length) {
                    components[componentIdx].onClick?.(instanceIdx);
                }
                return;  // Found and handled the click
            }
        }
    }
  }

  /******************************************************
   * E) Mouse Handling
   ******************************************************/
  const draggingState = useRef<DraggingState | null>(null);

  // Helper function to compare modifiers arrays
  function hasModifiers(actual: string[] | undefined, expected: string[]): boolean {
    if (!actual) return expected.length === 0;
    if (actual.length !== expected.length) return false;

    const sortedActual = [...actual].sort();
    const sortedExpected = [...expected].sort();

    return isEqual(sortedActual, sortedExpected);
  }

  // Add throttling for hover picking
  const throttledPickAtScreenXY = useCallback(
    throttle((x: number, y: number, mode: 'hover'|'click') => {
      pickAtScreenXY(x, y, mode);
    }, 32), // ~30fps
    [pickAtScreenXY]
  );

  // Picking handler - always registered on canvas
  const handlePickingMouseMove = useCallback((e: MouseEvent) => {
    if (!canvasRef.current || draggingState.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    throttledPickAtScreenXY(x, y, 'hover');
  }, [throttledPickAtScreenXY]);

  // Drag handler - attached/detached directly during drag
  const handleDragMouseMove = useCallback((e: MouseEvent) => {
    if (!canvasRef.current || !draggingState.current) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const st = draggingState.current;
    st.x = x;
    st.y = y;
    if (e.button === 2 || hasModifiers(st.modifiers, ['shift'])) {
      handleCameraUpdate(cam => pan(st));
    } else if (hasModifiers(st.modifiers, ['alt'])) {
      handleCameraUpdate(cam => roll(st));
    } else if (st.button === 0) {
      handleCameraUpdate(cam => orbit(st));
    }
  }, [handleCameraUpdate]);

  const handleMouseUp = useCallback((e: MouseEvent) => {
    const st = draggingState.current;
    if (st) {
      if (!canvasRef.current) return;
      const dx = st.x! - st.startX;
      const dy = st.y! - st.startY;
      const dragDistance = Math.sqrt(dx*dx + dy*dy);
      if ((dragDistance || 0) < 4) {
        pickAtScreenXY(st.x!, st.y!, 'click');
      }
      // Remove window listeners
      window.removeEventListener('mousemove', handleDragMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    }
    draggingState.current = null;
  }, [pickAtScreenXY, handleDragMouseMove]);

  const handleScene3dMouseDown = useCallback((e: MouseEvent) => {
    if (!canvasRef.current) return;
    const rect = canvasRef.current.getBoundingClientRect();

    const modifiers: string[] = [];
    if (e.shiftKey) modifiers.push('shift');
    if (e.ctrlKey) modifiers.push('ctrl');
    if (e.altKey) modifiers.push('alt');

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    draggingState.current = {
      button: e.button,
      startX: x,
      startY: y,
      x: x,
      y: y,
      rect: rect,
      modifiers,
      startCam: activeCameraRef.current!
    };

    // Add window listeners immediately when drag starts
    window.addEventListener('mousemove', handleDragMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    e.preventDefault();
  }, [handleDragMouseMove, handleMouseUp]);

  // Update canvas event listener references - only for picking and mousedown
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    canvas.addEventListener('mousemove', handlePickingMouseMove);
    canvas.addEventListener('mousedown', handleScene3dMouseDown);

    return () => {
      canvas.removeEventListener('mousemove', handlePickingMouseMove);
      canvas.removeEventListener('mousedown', handleScene3dMouseDown);
    };
  }, [handlePickingMouseMove, handleScene3dMouseDown]);

  /******************************************************
   * F) Lifecycle & Render-on-demand
   ******************************************************/
  // Init once
  useEffect(()=>{
    initWebGPU();
    return () => {
      if (gpuRef.current) {
        const { device, resources, pipelineCache } = gpuRef.current;

        device.queue.onSubmittedWorkDone().then(() => {
          for (const resource of Object.values(resources)) {
            if (resource) {
              resource.vb.destroy();
              resource.ib.destroy();
            }
          }

          // Clear instance pipeline cache
          pipelineCache.clear();
        });
      }
    };
  },[initWebGPU]);

  // Create/recreate depth + pick textures
  useEffect(()=>{
    if(isReady){
      createOrUpdateDepthTexture();
      createOrUpdatePickTextures();
    }
  },[isReady, containerWidth, containerHeight, createOrUpdateDepthTexture, createOrUpdatePickTextures]);

  // Update canvas size effect
  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const dpr = window.devicePixelRatio || 1;
    const displayWidth = Math.floor(containerWidth * dpr);
    const displayHeight = Math.floor(containerHeight * dpr);

    // Only update if size actually changed
    if (canvas.width !== displayWidth || canvas.height !== displayHeight) {
        canvas.width = displayWidth;
        canvas.height = displayHeight;

        // Update textures after canvas size change
        createOrUpdateDepthTexture();
        createOrUpdatePickTextures();
        renderFrame(activeCameraRef.current!);
    }
}, [containerWidth, containerHeight, createOrUpdateDepthTexture, createOrUpdatePickTextures, renderFrame]);

  // Render when camera or components change
  useEffect(() => {
    if (isReady && gpuRef.current) {
      renderFrame(activeCameraRef.current!, components);
      onReady();
    }
  }, [isReady, components, activeCameraRef.current]);

  // Wheel handling
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleWheel = (e: WheelEvent) => {
        if (!draggingState.current) {
            e.preventDefault();
            handleCameraUpdate(cam => {
              if (e.shiftKey) {
                if (e.ctrlKey) {
                  return adjustFov(cam, e.deltaY)
                } else {
                  return dolly(cam, e.deltaY);
                }
            } else {
                return zoom(cam, e.deltaY);
            }
            })
        }
    };

    canvas.addEventListener('wheel', handleWheel, { passive: false });
    return () => canvas.removeEventListener('wheel', handleWheel);
  }, [handleCameraUpdate]);


  return (
    <div style={{ width: '100%', border: '1px solid #ccc', position: 'relative' }}>
        <canvas
            ref={canvasRef}
            style={{border: 'none', ...style}}
        />
    </div>
  );
}

function componentHasAlpha(component: ComponentConfig) {
  return (
    (component.alphas && component.alphas?.length > 0)
    || (component.alpha && component.alpha !== 1.0)
    || component.decorations?.some(d => (d.alpha !== undefined && d.alpha !== 1.0 && d.indexes?.length > 0))
  )
}

/**
 * Partitions indices by component offsets
 */
function partitionIndices(
  indices: Uint32Array,
  offsets: ComponentOffset[]
): Uint32Array[] {
  const result: Uint32Array[] = [];
  const writeIndices: number[] = [];

  // Initialize result arrays and write indices
  for (let j = 0; j < offsets.length; j++) {
    const { count } = offsets[j];
    result[j] = new Uint32Array(count);
    writeIndices[j] = 0;
  }

  // Partition indices by component
  for (let i = 0; i < indices.length; i++) {
    const globalIdx = indices[i];

    // Find the component this index belongs to
    // For a small number of components, a simple linear scan is efficient
    for (let j = 0; j < offsets.length; j++) {
      const { start, count } = offsets[j];
      if (globalIdx >= start && globalIdx < start + count) {
        // Store the relative index in the appropriate partition
        result[j][writeIndices[j]++] = globalIdx - start;
        break;
      }
    }
  }

  return result;
}
