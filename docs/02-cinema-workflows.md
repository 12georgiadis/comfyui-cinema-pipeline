# ComfyUI Workflows for Auteur Cinema & Artistic Filmmaking

All workflows listed are **free** unless noted otherwise. All run on ComfyUI (free, open-source).

---

## 1. Video Generation (Text-to-Video, Image-to-Video)

### Wan 2.1 / Wan 2.2 (Alibaba) -- TOP RECOMMENDATION
- **What**: Full text-to-video and image-to-video. Wan 2.2 adds cinematic camera control (dolly, pan, tilt, zoom, parallax), MoE architecture, lighting/color grading via prompts. Bilingual EN/CN.
- **Models**: 14B (pro quality) and 1.3B (lightweight, 8GB VRAM)
- **Links**:
  - Official docs: https://docs.comfy.org/tutorials/video/wan/wan-video
  - Wan 2.2 Camera Control: https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-camera
  - RunComfy workflow: https://www.runcomfy.com/comfyui-workflows/wan2-2-fun-camera-in-comfyui-cinematic-panning-zoom-rotation
  - RunComfy Wan 2.2 overview: https://www.runcomfy.com/comfyui-workflows/wan-2-2-comfyui-leading-ai-video-generation-2025
  - GGUF (low VRAM): https://www.kombitz.com/2025/03/05/simple-comfyui-workflow-for-wan2-1-text-to-video-t2v-using-gguf-models/
  - Civitai GGUF Camera: https://civitai.com/models/1945009/wan22-fun-camera-control-gguf-4-steps
  - ComfyUI Wiki: https://comfyui-wiki.com/en/tutorial/advanced/video/wan2.1/wan2-1-video-model
- **Hardware**: 14B needs 24GB+ VRAM. 1.3B runs on 8GB. GGUF quantized for lower VRAM.

### VACE Wan 2.1 (Video Editing All-in-One)
- **What**: Unified framework for video inpainting, outpainting, reference-to-video, V2V, move/swap/expand/animate anything. Critical for post-production.
- **Links**:
  - Official docs: https://docs.comfy.org/tutorials/video/wan/vace
  - Outpainting: https://comfyui.org/en/wan2-1-vace-video-outpainting-pipeline
  - Transformation: https://comfyui.org/en/wan2-1-vace-video-transformation-workflow
  - V2V tutorial: https://stable-diffusion-art.com/wan-vace-v2v/
  - Ref-to-video: https://stable-diffusion-art.com/wan-vace-ref/
- **Hardware**: 24GB min, 48GB recommended

### HunyuanVideo (Tencent)
- **What**: 13B-param text-to-video. Cinema-quality realism, exceptional temporal consistency. Best for face content. Rival to Sora.
- **Links**:
  - Official: https://docs.comfy.org/tutorials/video/hunyuan-video
  - T2V: https://comfyui-wiki.com/en/tutorial/advanced/hunyuan-text-to-video-workflow-guide-and-example
  - I2V: https://comfyui-wiki.com/en/tutorial/advanced/hunyuan-image-to-video-workflow-guide-and-example
  - Flux + Hunyuan: https://stable-diffusion-art.com/flux-hunyuan-text-to-video-workflow-comfyui/
- **Hardware**: 24GB+ VRAM. Budget 10-15 min/clip.

### LTX-Video (Lightricks) -- FASTEST
- **What**: 2B params, fastest generation (real-time on RTX 4090). T2V, I2V, V2V. Good for rapid prototyping.
- **Links**:
  - GitHub: https://github.com/Lightricks/ComfyUI-LTXVideo
  - Wiki: https://comfyui-wiki.com/en/tutorial/advanced/ltx-video-workflow-step-by-step-guide
  - LTX-2 ControlNet: https://www.runcomfy.com/comfyui-workflows/ltx-2-controlnet-in-comfyui-depth-controlled-video-workflow
- **Hardware**: 12GB+ VRAM

### CogVideoX-5B (Tsinghua/Zhipu)
- **What**: Best I2V quality. LoRA training support (50-200 clips).
- **Links**:
  - Civitai I2V: https://civitai.com/models/1117606/cogvideox-image-to-video-comfyui-workflow
  - + ControlNet + LivePortrait: https://www.runcomfy.com/comfyui-workflows/comfyui-cogvideox-workflow-with-controlnet-and-live-portrait
- **Hardware**: 24GB recommended

### AnimateDiff + SVD
- **What**: AnimateDiff adds motion via SD 1.5/SDXL. SVD generates clips from single frame. MotionLoRA for camera (zoom, pan, tilt, roll).
- **Links**:
  - AnimateDiff-Evolved: https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
  - SVD: https://comfyworkflows.com/workflows/bf3b455d-ba13-4063-9ab7-ff1de0c9fa75
  - Tutorial: https://www.runcomfy.com/tutorials/how-to-use-animatediff-to-create-ai-animations-in-comfyui
  - + IP-Adapter I2V: https://civitai.com/articles/4339/image-to-video-comfyui-workflow-using-animatediff-and-ip-adapter-ready-to-use
- **Hardware**: AnimateDiff 8GB+. SVD-XT 12-16GB.

---

## 2. Style Transfer / Look Development

### ComfyUI-StyleTransferPlus -- Advanced Non-Diffusion Style Transfer
- **What**: Multiple methods (TSSAT, AesFA). Generate 1-2 stylized keyframes, propagate with EbSynth for temporal consistency.
- **URL**: https://github.com/FuouM/ComfyUI-StyleTransferPlus
- **Hardware**: 6-12GB VRAM at 1024 resolution

### ComfyUI-EbSynth -- Video Style Propagation
- **What**: Transfers keyframe style across entire video via optical flow. No AI hallucinations (example-based synthesis).
- **URL**: https://www.runcomfy.com/comfyui-nodes/ComfyUI-EbSynth
- **Note**: EbSynth V2 (Sept 2025) adds timeline, layers, real-time preview, Apple Silicon support.

### Wan 2.1 Video Style Transfer
- **What**: Transform video appearance while maintaining motion/structure.
- **URL**: https://learn.thinkdiffusion.com/top-10-comfyui-workflows-for-ai-text-to-video-and-video-to-video-2025/

### Wan 2.1 Ditto -- Video Stylization
- **What**: Robust global restyling with strong temporal coherence.
- **URL**: https://www.runcomfy.com/comfyui-workflows/wan-2-1-ditto-in-comfyui-video-stylization-and-motion-consistency

### ComfyUI-Fast-Style-Transfer
- **What**: Fast neural style transfer (TensorFlow). Includes experimental regular NST.
- **URL**: https://github.com/zeroxoxo/ComfyUI-Fast-Style-Transfer

### CozyMantis Style Transfer Workflow
- **What**: IPAdapter-based for SDXL. More abstract/creative results.
- **URL**: https://github.com/cozymantis/style-transfer-comfyui-workflow

### ComfyUI-EasyColorCorrector -- Cinematic Color Grading
- **What**: Presets: Cinematic, Teal & Orange, Film Noir, Vintage Film, Bleach Bypass. Film stock emulation.
- **URL**: https://github.com/regiellis/ComfyUI-EasyColorCorrector

### LUT Application Nodes
- **OlmLUT** (best, with browser LUT maker): https://github.com/o-l-l-i/ComfyUI-OlmLUT
- **ProPostApplyLUT** (precise blending + log/gamma): https://www.runcomfy.com/comfyui-nodes/comfyui-propost/ProPostApplyLUT
- **ComfyUI_essentials ImageApplyLUT**: https://www.runcomfy.com/comfyui-nodes/ComfyUI_essentials/ImageApplyLUT-
- **LayerColor LUT Apply**: https://www.runcomfy.com/comfyui-nodes/ComfyUI_LayerStyle/LayerColor--LUT-Apply

---

## 3. Film Grain, Anamorphic & Cinematic Post-Processing

### Anamorphic Lens Effect (DJZ-Nodes)
- **What**: Oval bokeh, lens flares, squeeze ratio, chromatic aberration, widescreen.
- **URL**: https://www.runcomfy.com/comfyui-nodes/DJZ-Nodes/anamorphic-effect

### Film Grain Nodes
- **ProPostFilmGrain**: Fine/Coarse grain + Vignette + Radial Blur. [GitHub](https://github.com/digitaljohn/comfyui-propost)
- **BetterFilmGrain**: Realistic with scale, strength, saturation, toe. [RunComfy](https://www.runcomfy.com/comfyui-nodes/ComfyUI-Image-Filters/BetterFilmGrain)
- **Fast Film Grain**: Quick application. [RunComfy](https://www.runcomfy.com/comfyui-nodes/comfyui-vrgamedevgirl/fast-film-grain)
- **Image Film Grain (WAS)**: Adjustable density. [RunComfy](https://www.runcomfy.com/comfyui-nodes/was-node-suite-comfyui/Image-Film-Grain)
- **FilmGrain + temp + vignetting**: [GitHub](https://github.com/EllangoK/ComfyUI-post-processing-nodes)

### ComfyUI-EsesImageLensEffects
- **What**: Barrel/pincushion distortion, chromatic aberration, vignette, post-process scaling.
- **URL**: https://github.com/quasiblob/ComfyUI-EsesImageLensEffects/

### ComfyUI_Photography_Nodes
- **What**: Bloom, Lens Flares, Chromatic Aberration, DoF, Halation, Lens Dirt, Vignette.
- **URL**: https://comfyai.run/documentation/Lens%20Distortion

### Lens Flare Node
- **What**: Classic, anamorphic, starburst, hexagonal flares.
- **URL**: https://www.runcomfy.com/comfyui-nodes/ComfyUI-Image-Effects/lens-flare-node

---

## 4. Rotoscoping / AI Masking

### SAM 3 (Meta, November 2025) -- LATEST
- **What**: Prompt-based segmentation (no clicking), video tracking, 3D object reconstruction.
- **Links**:
  - Workflow: https://www.runcomfy.com/comfyui-workflows/sam-3-in-comfyui-workflow-precision-image-segmentation-ai
  - Tutorial: https://stable-diffusion-art.com/sam3-comfyui-image/
- **Custom nodes**: ComfyUI-SAM3 by PozzettiAndrea

### SAM 2 (Meta) -- Production Workhorse
- **What**: Real-time video segmentation at 44 FPS. Matches pro rotoscoping for most subjects.
- **Links**:
  - Guide: https://apatero.com/blog/best-video-segmentation-tool-sam2-complete-guide-2025
  - RunComfy: https://www.runcomfy.com/comfyui-nodes/ComfyUI-SAM2
  - VFX workflow: https://princechudasama.com/sam2-segmentation-in-comfyui-fast-video-masking-for-vfx-and-ai-workflows
- **Custom nodes**: ComfyUI-segment-anything-2 by Kijai

---

## 5. Frame Interpolation / Slow Motion

### ComfyUI-Frame-Interpolation (Fannovel16)
- **What**: Multiple algorithms: RIFE (real-time, 4.0-4.9), FILM (quality), AMT, GMFSS Fortuna, Sepconv, IFUnet.
- **URL**: https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
- **Comparison**: https://apatero.com/blog/rife-vs-film-video-frame-interpolation-comparison-2025
- **Recommendation**: RIFE v4.6 for general use (5-10x faster). FILM for complex motion.

### GIMMVFI + FlashVSR
- **What**: Frame interpolation + resolution upscaling. Perfect for archival footage.
- **URL**: https://civitai.com/posts/25686256

---

## 6. Upscaling / Film Restoration

### SeedVR2 -- TOP for Archival
- **What**: Preserves original structure, no artificial features. Best for archival footage.
- **Links**:
  - GitHub: https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler
  - Handbook: https://blog.comfy.org/p/upscaling-in-comfyui

### SUPIR (Scaling-UP Image Restoration)
- **What**: 13B-param photo-realistic restoration. Works with SDXL. Chain with 4x Foolhardy Remacri for 8K.
- **Links**:
  - RunComfy: https://www.runcomfy.com/comfyui-workflows/supir-in-comfyui-realistic-image-video-upscaling
  - 8K pipeline: https://www.runcomfy.com/comfyui-workflows/8k-image-upscaling-supir-4x-foolhardy-remacri
  - Docs: https://docs.comfy.org/tutorials/basic/upscale

### Easy Video Upscaler (Mickmumpitz)
- **What**: Super-resolution + sharpening + Wan 2.x diffusion refinement. Conservative for archival.
- **URL**: https://www.runcomfy.com/comfyui-workflows/easy-video-upscaler-for-footage-in-comfyui-hd-detail-restoration

### AI Video Restoration with Wan 2.1
- **What**: Frame-level restoration using video control embeddings.
- **URL**: https://comfyui.org/en/ai-video-restoration-and-enhancement
- **Hardware**: 16GB+ VRAM

---

## 7. Depth Estimation / 3D / Parallax

### Depth Anything V3 (ByteDance, Nov 2025) -- LATEST
- **What**: State-of-the-art monocular depth. 44.3% better camera pose accuracy than VGGT.
- **Links**:
  - GitHub: https://github.com/PozzettiAndrea/ComfyUI-DepthAnythingV3
  - RunComfy: https://www.runcomfy.com/comfyui-nodes/ComfyUI-DepthAnythingV3
  - Guide: https://apatero.com/blog/depth-anything-v3-complete-guide-use-cases-2025
- **Models**: Small / Base / Large / Giant

### ComfyUI-Marigold -- Diffusion-Based Depth
- **What**: High detail at ~768p. OpenEXR export for VFX/3D software.
- **Links**:
  - GitHub: https://github.com/kijai/ComfyUI-Marigold
  - Docs: https://comfyai.run/documentation/MarigoldDepthEstimation

### ComfyUI-Depthflow-Nodes -- 2.5D Parallax
- **What**: 2D images -> 2.5D parallax animations. Zoom, dolly, circle. DoF, vignette.
- **Links**:
  - GitHub: https://github.com/akatz-ai/ComfyUI-Depthflow-Nodes
  - RunComfy: https://www.runcomfy.com/comfyui-nodes/ComfyUI-Depthflow-Nodes

---

## 8. Camera Motion (Image-to-Video)

### Wan 2.2 Fun Camera -- TOP RECOMMENDATION
- **What**: Precise virtual camera: pan, tilt, dolly, tracking, orbital arcs, crane, whip pan.
- **Prompt tips**: Use camera verbs. Keep under 5s / 120 frames.
- **Hardware**: 24GB+ VRAM (fp8 scaled)

### Uni3C (DAMO Academy)
- **What**: Transfer camera + human animations from reference video. Point cloud control.
- **URL**: https://www.runcomfy.com/comfyui-workflows/uni3c-comfyui-workflow-video-referenced-camera-motion-transfer

### Wan 2.2 Parallax "Alive Stills"
- **What**: Photographic parallax from single still. Gentle breathing, hair movement.
- **URL**: https://www.promptus.ai/blog/wan-2-2

---

## 9. ControlNet for Video

### Wan 2.1 Fun ControlNet
- **What**: Depth, Canny, OpenPose guided video generation.
- **Links**:
  - RunComfy: https://www.runcomfy.com/comfyui-workflows/wan-2-1-fun-controlnet-ai-video-generation-with-depth-canny-openpose-control
  - Tutorial: https://comfyui.org/en/mastering-video-generation-with-fun-controlnet

### LTX-2 ControlNet (Depth-Controlled)
- **What**: IC LoRA conditioning (Depth + Canny + Pose). Generates synchronized audio + visuals.
- **URL**: https://www.runcomfy.com/comfyui-workflows/ltx-2-controlnet-in-comfyui-depth-controlled-video-workflow

### CogVideoX + ControlNet + Live Portrait
- **What**: Simple footage -> cinematic scenes. Depth + acting refinement.
- **URL**: https://www.runcomfy.com/comfyui-workflows/comfyui-cogvideox-workflow-with-controlnet-and-live-portrait

### Depth ControlNet Posture Transfer
- **What**: Best combos: Depth(0.7)+Canny(0.4), Depth(0.8)+OpenPose(0.5), Depth(0.7)+IP-Adapter(0.6).
- **URL**: https://apatero.com/blog/depth-controlnet-posture-transfer-comfyui-complete-guide-2025

---

## 10. Face/Character Consistency

### IPAdapter FaceID Plus V2
- **What**: Consistent faces across shots without LoRA. Use 3-5 reference images averaged.
- **Links**:
  - RunComfy: https://www.runcomfy.com/comfyui-workflows/create-consistent-characters-in-comfyui-with-ipadapter-faceid-plus
  - Guide: https://tgecrypto365.medium.com/how-to-create-consistent-characters-comfyui-the-2025-step-by-step-workflow-ipadapter-76edbfca0baf
  - No-LoRA: https://apatero.com/blog/comfyui-ipadapter-faceid-workflow-ai-influencers-no-lora-2025

### FaceDetailer + InstantID + IP-Adapter
- **What**: High-precision face swapping.
- **Links**:
  - OpenArt: https://openart.ai/workflows/myaiforce/better-face-swap-facedetailer-instantid-ip-adapter/KMFUVKakzXeepb2pMEnT
  - Tutorial: https://myaiforce.com/comfyui-instantid-ipadapter/

### LivePortrait -- Face Animation
- **What**: Animate portraits with expressions, head movements, eye blinks.
- **Links**:
  - Img2Vid: https://www.runcomfy.com/comfyui-workflows/comfyui-liveportrait-workflow-animate-portraits
  - Vid2Vid: https://www.runcomfy.com/comfyui-workflows/comfyui-liveportrait-workflow-animate-portraits-vid2vid
  - Advanced: https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait

### WAN 2.2 Animate
- **What**: 14B char animation. Expression transfer maintaining appearance.
- **URL**: https://apatero.com/blog/wan-2-2-animate-character-animation-revolution-comfyui-2025
- **Hardware**: 16GB VRAM

### LatentSync -- Lip Sync / Film Dubbing
- **What**: ByteDance latent diffusion lip sync. Multi-language. No hallucination (TREPA module).
- **Links**:
  - GitHub: https://github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper
  - RunComfy: https://www.runcomfy.com/comfyui-workflows/latentsync-advanced-lip-sync-video-generator
  - ThinkDiffusion: https://learn.thinkdiffusion.com/seamless-lip-sync-create-stunning-videos-with-latentsync/
- **Hardware**: 24GB min, 48GB recommended

---

## 11. Post-Documentary / Experimental / Glitch Art

### DJZ Datamosh V3 -- Datamoshing & Glitch
- **What**: Intentional video corruption for glitch aesthetics. Adjustable intensity, batch processing.
- **Links**:
  - V3: https://www.runcomfy.com/comfyui-nodes/DJZ-Nodes/djz-datamosh-v3
  - V2: https://www.runcomfy.com/comfyui-nodes/DJZ-Nodes/djz-datamosh-v2
  - Tutorial: https://civitai.com/articles/10209/how-to-datamosh-glitch-video-comfyui-nodes-djzdatamosh

### RAVE + AnimateDiff -- Zero-Shot Video Editing
- **What**: Zero-shot editing using pre-trained diffusion. Changes subjects retaining motion. Surreal results.
- **URL**: https://learn.thinkdiffusion.com/how-to-create-stunning-ai-videos-with-comfyui-rave-and-animatediff/

### QWEN Next Scene LoRA -- Cinematic Sequences
- **What**: Generates cinematic image sequences with camera movements and visual continuity.
- **URL**: https://apatero.com/blog/qwen-next-scene-lora-cinematic-sequences-comfyui-2025

---

## 12. Resource Collections

| Platform | URL | Notes |
|---|---|---|
| ThinkDiffusion Top 10 Video | https://learn.thinkdiffusion.com/top-10-comfyui-workflows-for-ai-text-to-video-and-video-to-video-2025/ | Free downloads |
| RunComfy Hub | https://www.runcomfy.com/comfyui-workflows | Runnable guaranteed |
| Civitai | https://civitai.com/ | Models + LoRAs + workflows |
| ComfyUI Docs | https://docs.comfy.org/ | Official tutorials |
| ComfyUI Wiki | https://comfyui-wiki.com/ | Comprehensive guides |
| Awesome ComfyUI | https://github.com/ComfyUI-Workflow/awesome-comfyui | Master node list |
| Apatero Blog | https://apatero.com/blog/ | In-depth technical |
| MimicPC Guides | https://www.mimicpc.com/learn/ | Model comparisons |

---

## Hardware Quick Reference

| VRAM | What Runs |
|---|---|
| 8GB | Wan 1.3B, AnimateDiff, LTX basic |
| 12GB | LTX-Video, Wan GGUF quantized |
| 16GB | Most models optimized, WAN 2.2 Animate |
| 24GB (RTX 4090) | All models. HunyuanVideo, Wan 14B, SUPIR, LatentSync, VACE |
| 32GB (RTX 5090) | Comfortable for everything. Multi-model pipelines |
| 48GB+ | VACE 14B optimal, LatentSync optimal |
| 96GB (Cloud) | Multiple ControlNets, heavy batch |
