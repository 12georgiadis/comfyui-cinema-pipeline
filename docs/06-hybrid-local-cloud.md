# Hybrid Local/Cloud GPU for ComfyUI

How to use both a local GPU and cloud GPUs, switching or combining them.

---

## Local: RTX 5090 (32GB VRAM)

### Performance Estimates
| Task | Time |
|---|---|
| LTX-Video 720p 4s clip | ~25 seconds |
| Wan 2.1 clip | 2-4 minutes |
| HunyuanVideo clip | 8-15 minutes |
| SDXL style transfer (4 images) | ~15 seconds |
| SAM 2 rotoscoping | < 1 minute |

### Optimization
- NVFP4 format: 3x faster, 60% less VRAM vs FP16
- RTX Video upscaling to 4K in seconds
- [Setup guide](https://blog.comfy.org/p/how-to-get-comfyui-running-on-your)
- [NVIDIA RTX AI video guide](https://www.nvidia.com/en-us/geforce/news/rtx-ai-video-generation-guide/)

---

## Cloud Options

### Comfy Cloud (Official)
- **URL**: https://www.comfy.org/cloud
- **GPU**: NVIDIA RTX 6000 Pro -- 96GB VRAM, 180GB system RAM (~2x A100 speed)
- **900+ models** pre-installed
- **Pay only for active GPU** (not editing, not downloading)

**Pricing (Jan 2026, after 30% drop)**:

| Plan | Price | Credits/mo | LoRAs | Max workflow |
|---|---|---|---|---|
| Standard | $20/mo | 4,200 | No | 30 min |
| Creator | $35/mo | More | Yes (CivitAI, HF) | 30 min |
| Pro | $100/mo | Maximum | Yes | 1 hour |

- GPU cost: ~0.266 credits/sec
- 211 credits = 1 USD
- Standard = ~4h23 of GPU/month
- Top-up credits available (valid 1 year)

**API**: Compatible with local API. Same endpoints, same format.
- URL: `https://cloud.comfy.org/api/prompt`
- Auth: `X-API-Key` header
- Docs: https://docs.comfy.org/development/cloud/overview

### RunComfy
- **URL**: https://www.runcomfy.com/
- **What**: "Unmodified ComfyUI experience" in cloud. Machines 16GB to 141GB VRAM.
- **Pricing**: $29.99/mo Pro + pay-as-you-go (~$1.39/h large machine)
- **Advantage**: Workflows from local work directly. Serverless API deploy in one click.

### ThinkDiffusion
- **URL**: https://www.thinkdiffusion.com/comfyui
- **What**: Dedicated VM with ComfyUI pre-installed. 16GB to 48GB VRAM (80GB coming).
- **Advantage**: More mature UX. Models from HuggingFace, CivitAI, or custom.

### CloudRift
- **URL**: https://www.cloudrift.ai/
- **Pricing**: RTX 4090 ~$0.39/h, RTX 5090 ~$0.65/h, RTX PRO 6000 ~$1.29/h
- **What**: GPU on-demand, no subscription. ComfyUI pre-installed.

---

## Hybrid Orchestration

### ComfyUI-Distributed -- TRUE HYBRID
- **URL**: https://github.com/robertvoy/ComfyUI-Distributed
- **What**: Your local machine orchestrates local AND cloud workers. Auto-failover to local if cloud goes down. RunPod + Cloudflare tunnels support.
- **Limitation**: Doesn't combine VRAM. Doesn't accelerate a single generation. Enables parallel generations.
- **Best for**: RTX 5090 local + RunPod cloud workers for heavy batches.

### ComfyUI-Cloud Plugin
- **URL**: https://github.com/nathannlu/ComfyUI-Cloud
- **What**: Send workflows from local ComfyUI to cloud GPU. Closest to transparent switching.

### Same MCP Server for Both
Since the Comfy Cloud API is compatible with local, a single MCP server can control both. Just switch the URL:
- Local: `http://127.0.0.1:8188`
- Cloud: `https://cloud.comfy.org/api` + `X-API-Key`

---

## Recommended Strategy

1. **Default**: Run everything on local RTX 5090 (32GB handles most workflows)
2. **Heavy workflows**: Switch to Comfy Cloud for VACE 14B, HunyuanVideo, multi-ControlNet (96GB)
3. **Batch processing**: Use ComfyUI-Distributed with RTX 5090 + RunPod workers
4. **On the go**: Comfy Cloud via browser/API (no local machine needed)

The 32GB of the RTX 5090 covers ~90% of cinema workflows. The cloud is for the 10% that needs more.
