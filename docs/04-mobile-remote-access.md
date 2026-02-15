# Mobile & Remote Access to ComfyUI

How to use ComfyUI from iPhone/iPad, anywhere in the world.

---

## 1. Network Access: Tailscale (Recommended)

If you already use Tailscale, this is the simplest path.

**Setup**:
1. Launch ComfyUI with `--listen 0.0.0.0 --port 8188`
2. On iPhone/iPad with Tailscale: open Safari, go to `http://<tailscale-ip>:8188`
3. Done. No port forwarding, no internet exposure, encrypted WireGuard tunnel.

**Guide**: https://justiceshultz.com/portfolio-comfytailscale

**Problem**: The default ComfyUI node editor is painful on small screens. Solutions below.

### Alternatives to Tailscale

| Solution | Price | Speed | Notes |
|---|---|---|---|
| Cloudflare Tunnel | Free | 46 Mbps | Unstable for long generations |
| ngrok | Free limited, $8-20/mo real use | 8.8 Mbps | OK if paying |
| Pinggy | Free (SSH tunnel) | OK | Simple to launch |
| Zrok | Free (generous) | Good | Good alternative |

**Custom node**: [ComfyUI-ngrok](https://comfy.icu/extension/pkpkTech__ComfyUI-ngrok) integrates ngrok directly.

**Verdict**: If you have Tailscale, use Tailscale. The others expose ComfyUI to the public internet.

---

## 2. iOS Native Apps

### Comfy Portal -- RECOMMENDED
- **App Store**: https://apps.apple.com/us/app/comfy-portal/id6741044736
- **GitHub**: https://github.com/ShunL12324/comfy-portal
- **Rating**: 4.7/5
- **iOS**: 15.1+, iPadOS, macOS (M1+), visionOS
- **Features**:
  - Multi-server (local + cloud like RunPod)
  - Import workflows on iPhone
  - SDXL and Flux support
  - Real-time monitoring
  - Multi-image and video output
  - Workflow sync from PC (via ComfyUI extension)
  - Compatibility mode for non-optimized nodes

### Comfy Remote
- **App Store**: https://apps.apple.com/us/app/comfy-remote/id6503436538
- **Site**: https://comfyremoteapp-83050.web.app/
- **iOS**: 12.0+
- **Features**:
  - History view (done, running, queued)
  - Import from .json or .png metadata
  - Upload photos from iPhone as input (LoadImage)
  - Mask editor for inpainting
  - Node filter (hide complex nodes)
  - Queue interruption

### ComfyUInator
- **App Store**: https://apps.apple.com/us/app/comfyuinator/id6738099343
- **What**: Load workflow JSONs into app directory, generate.

### Mobile Comfy Creator
- **App Store**: https://apps.apple.com/us/app/mobile-comfy-creator/id6752901529
- **What**: txt2img, img2img, txt2video, img2video, video2video. Advanced controls.

### ComfyUI Mobile App (Android)
- **URL**: https://github.com/deni2312/ComfyUIMobileApp

---

## 3. Mobile-First Web UIs (Self-Hosted)

### MCWW as PWA
- **URL**: https://github.com/light-and-ray/Minimalistic-Comfy-Wrapper-WebUI
- **What**: Install on iPhone home screen via Safari Share > Add to Home Screen. Full-screen app-like experience.
- **Access**: `http://<tailscale-ip>:8188/mcww`
- **Best for**: Per-workflow simplified interface with state persistence.

### Pocket-Comfy -- TAILSCALE RECOMMENDED
- **URL**: https://github.com/PastLifeDreamer/Pocket-Comfy
- **What**: Mobile-first web app. ComfyUI Mini + Smart Gallery under one Python script. Large touch buttons, modern UI.
- **Explicitly recommends Tailscale** for remote access.

### ComfyUI Mini
- **URL**: https://github.com/ImDarkTom/ComfyUIMini
- **Stack**: Node.js
- **What**: Lightweight mobile-friendly WebUI for workflow execution. Gallery, progress tracking.

### ComfyUI-MobileForm
- **URL**: https://github.com/123jimin/ComfyUI-MobileForm
- **What**: Create "Mobile Form" group in workflow, add nodes to expose. Auto-generates mobile form.

### ComfyUI_CozyGen
- **URL**: https://github.com/gsusgg/ComfyUI_CozyGen
- **Stack**: React + Vite + Tailwind CSS
- **What**: Mobile-first dark theme. Auto-generates controls from workflow nodes. Real-time previews.

### comfy-webui (RioShiina47)
- **URL**: https://github.com/RioShiina47/comfy-webui
- **Stack**: Gradio
- **What**: Mobile-first, transforms workflows into APIs/MCP tools. Docker recommended. Early stage.

---

## 4. Telegram / Discord Bots

### ComfyUI-TG (Telegram) -- MOST COMPLETE
- **URL**: https://github.com/daxcay/ComfyUI-TG
- **Install**: `comfy node registry-install ComfyUI-TG` or ComfyUI Manager
- **Requires**: Node.js v20.17.0+
- **Setup**:
  1. Create bot via @BotFather
  2. Configure token in `telegram.json`
  3. Save workflows in API format with `TG-ImageSaver` node
  4. Upload workflows via Telegram dashboard
- **Commands**:
  - `/wfs` -- list workflows
  - `/wf 1` -- select workflow
  - `/wns` -- show editable nodes
  - `/s node_id input_id value` -- set parameter
  - `/q` -- queue generation
  - `/i` -- interrupt
  - `/r` -- reset to defaults
  - `/sce` / `/scd` -- auto seed change on/off
- **Image input**: Send photo with `/s node_id input_id` as caption
- **Group support**: Works in Telegram groups

### Comfyui-TelegramSender (Notifications only)
- **URL**: https://github.com/NeuralSamurAI/Comfyui-TelegramSender
- **What**: Sends results (images, text) to Telegram. No bidirectional control. Good for push notifications.

### comfyui_telegram_bot (zlsl)
- **URL**: https://github.com/zlsl/comfyui_telegram_bot
- **What**: Send image, receive transformed version. `/face`, `/upscale` commands.

### ComfyUI-Discord-Bot
- **URL**: https://github.com/stavsap/ComfyUI-Discord-Bot

### Salt AI Discord Bot
- Free, works in any Discord server. Build and deploy custom workflows.

---

## 5. Recommended Setup

### Immediate (zero extra cost)

**Tailscale + MCWW (PWA) + ComfyUI-TG**

1. **On the machine with GPU**:
   - Launch ComfyUI with `--listen 0.0.0.0 --port 8188`
   - Install MCWW via ComfyUI Manager
   - Install ComfyUI-TG and configure Telegram bot
   - Optional: Comfyui-TelegramSender for push notifications

2. **On iPhone/iPad**:
   - **Quick generations**: Telegram bot `/wf`, adjust prompt, `/q`. Images arrive in chat.
   - **More control**: Safari > `http://<tailscale-ip>:8188` > MCWW. Install as PWA.
   - **Monitoring**: Comfy Portal from App Store. Add server `<tailscale-ip>:8188`.

3. **Daily workflow**:
   - Create/edit workflows on desktop (node editor)
   - Tag editable nodes for MCWW (`<Label:Category:Order>`)
   - From iPhone: launch via Telegram (simplest) or MCWW/Comfy Portal (more control)
   - Receive results via Telegram push

### Summary

| Need | Solution |
|---|---|
| Quick generation from phone | ComfyUI-TG (Telegram bot) |
| Simplified browser interface | MCWW as PWA via Tailscale |
| Native iOS monitoring | Comfy Portal |
| Push notifications | Comfyui-TelegramSender |
| Full ComfyUI remote | Safari + Tailscale |
