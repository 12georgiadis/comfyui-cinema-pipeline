# Hardware Guide for ComfyUI Cinema Production

---

## VRAM Requirements by Workflow

| VRAM | What Runs |
|---|---|
| **8GB** | Wan 2.1 1.3B, AnimateDiff, LTX-Video basic |
| **12GB** | LTX-Video, Wan 2.1 GGUF quantized, CogVideoX optimized |
| **16GB** | Most models with optimization, WAN 2.2 Animate, video restoration |
| **24GB** (RTX 4090) | Professional baseline. All models run: HunyuanVideo, Wan 14B, SUPIR, LatentSync, VACE |
| **32GB** (RTX 5090) | Comfortable for everything. Multi-model pipelines, no optimization needed |
| **48GB** | VACE 14B optimal, LatentSync optimal, multi-ControlNet |
| **96GB** (Cloud) | Multiple heavy models simultaneously, massive batches |

---

## GPU Comparison for Video Generation

### RTX 5090 (32GB, local)
- LTX-Video 720p 4s: ~25 seconds
- Wan 2.1 per clip: 2-4 minutes
- HunyuanVideo per clip: 8-15 minutes
- SDXL style transfer: ~15 seconds (4 images)
- NVFP4 format: 3x faster, 60% less VRAM vs FP16
- RTX Video upscaling to 4K in seconds

### RTX 6000 Pro (96GB, Comfy Cloud)
- ~2x A100 speed
- Can run workflows impossible on 32GB
- All popular models pre-installed

### Key optimization: GGUF Quantization
- Reduces VRAM requirements significantly
- Available for Wan 2.1/2.2, most major models
- Small quality loss, major VRAM savings
- Example: Wan 14B fp8 needs 24GB, GGUF Q4 needs ~12GB

---

## Dual Machine Setup (Mac + Windows)

### Windows PC (GPU workstation)
- ComfyUI with CUDA GPU
- Runs all generation/processing
- Accessible via Tailscale

### Mac (editing station)
- DaVinci Resolve / Final Cut Pro for editing
- Connects to Windows ComfyUI via network
- Manages workflows, queues generations

### Network
- Tailscale mesh: encrypted, works anywhere
- ComfyUI `--listen 0.0.0.0` on Windows
- Mac accesses via `http://<tailscale-ip>:8188`
- Mobile (iPhone/iPad) also via Tailscale

---

## References

- [2025 GPU Guide for ComfyUI](https://www.promptus.ai/blog/2025-gpu-guide-for-comfyui)
- [RTX 5090 ComfyUI Setup](https://blog.comfy.org/p/how-to-get-comfyui-running-on-your)
- [NVIDIA RTX AI Video Generation](https://www.nvidia.com/en-us/geforce/news/rtx-ai-video-generation-guide/)
- [NVIDIA RTX 4K Video + ComfyUI](https://blogs.nvidia.com/blog/rtx-ai-garage-ces-2026-open-models-video-generation/)
