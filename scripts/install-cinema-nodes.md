# Custom Nodes for Cinema Pipeline

Install these custom node packs to enable all cinema workflow templates.
Use ComfyUI Manager (recommended) or git clone into `custom_nodes/`.

## Required (Core)

These are needed for the basic cinema workflows:

### VideoHelperSuite
Video loading, saving, and processing. Required for ALL video workflows.
```
ComfyUI Manager: ComfyUI-VideoHelperSuite
Git: https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
```

## Recommended (Cinema)

### Frame Interpolation (RIFE)
Slow-motion and frame rate conversion.
```
ComfyUI Manager: ComfyUI-Frame-Interpolation
Git: https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
```

### Depth Anything V2
Depth map estimation for VFX compositing.
```
ComfyUI Manager: ComfyUI-DepthAnythingV2
Git: https://github.com/kijai/ComfyUI-DepthAnythingV2
```

### IPAdapter Plus
Style transfer and face consistency across shots.
```
ComfyUI Manager: ComfyUI_IPAdapter_plus
Git: https://github.com/cubiq/ComfyUI_IPAdapter_plus
```

### ControlNet Auxiliary Preprocessors
Canny, depth, pose, normal map preprocessing.
```
ComfyUI Manager: comfyui_controlnet_aux
Git: https://github.com/Fannovel16/comfyui_controlnet_aux
```

### SAM 2 (Segment Anything)
AI-powered rotoscoping and segmentation.
```
ComfyUI Manager: ComfyUI-SAM2
Git: https://github.com/neverbiasu/ComfyUI-SAM2
```

## Optional (Advanced)

### AnimateDiff Evolved
Animation from single images.
```
ComfyUI Manager: ComfyUI-AnimateDiff-Evolved
Git: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
```

### ReActor
Face swap for maintaining character consistency.
```
ComfyUI Manager: comfyui-reactor-node
Git: https://github.com/Gourieff/comfyui-reactor-node
```

### Film Grain
Add realistic film grain textures.
```
ComfyUI Manager: ComfyUI-Film-Grain
Search in Manager for "film grain"
```

### KJNodes
Utility nodes (batch processing, image manipulation).
```
ComfyUI Manager: ComfyUI-KJNodes
Git: https://github.com/kijai/ComfyUI-KJNodes
```

### Impact Pack
Detection, segmentation, and region-based processing.
```
ComfyUI Manager: ComfyUI-Impact-Pack
Git: https://github.com/ltdrdata/ComfyUI-Impact-Pack
```

## Models to Download

### Checkpoints (Image Generation)
- `sd_xl_base_1.0.safetensors` - Base SDXL
- `juggernautXL_v9Rundiffusion.safetensors` - Best photorealistic SDXL
- `realvisxlV50_v50Bakedvae.safetensors` - Photorealistic with baked VAE

### UNET (Video Generation)
- `wan2.1_t2v_14B_bf16.safetensors` - Wan 2.1 Text-to-Video (14B, best quality)
- `wan2.1_t2v_1.3B_bf16.safetensors` - Wan 2.1 T2V lightweight

### CLIP / Text Encoders
- `clip_l.safetensors` - CLIP-L for Wan
- `umt5_xxl_fp8_e4m3fn.safetensors` - T5-XXL for Wan (fp8 quantized)

### VAE
- `wan_2.1_vae.safetensors` - Wan 2.1 VAE

### Upscale
- `RealESRGAN_x4plus.pth` - General purpose 4x upscale
- `4x-UltraSharp.pth` - Best for photorealistic images

### Frame Interpolation
- `rife49.pth` - Latest RIFE model

### Depth
- `depth_anything_v2_vitl_fp32.safetensors` - Best accuracy depth estimation
