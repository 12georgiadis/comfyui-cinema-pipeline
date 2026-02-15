# Simplified Frontends for ComfyUI

Alternatives to the default node-based UI. From "Krea-like webapp" to "just a text field and a button".

---

## Web Frontends (Krea-like)

### ViewComfy -- Workflow to Webapp
- **URL**: https://github.com/ViewComfy/ViewComfy
- **Site**: https://www.viewcomfy.com/
- **Stack**: Next.js
- **What**: Transforms any ComfyUI workflow into a clean webapp. Choose which inputs to expose, hide the rest. Mask editor, history, side-by-side comparison.
- **Deploy**: Local with ngrok, ViewComfy Cloud, or self-hosted on Modal.
- **Playground mode**: Shareable UI without revealing the JSON. Config via `.env` with `NEXT_PUBLIC_VIEW_MODE=true`.
- **Verdict**: Closest to "Fisher-Price for any workflow".

### MCWW -- Minimalistic Comfy Wrapper WebUI
- **URL**: https://github.com/light-and-ray/Minimalistic-Comfy-Wrapper-WebUI
- **Article**: https://medium.com/@light.and.ray/the-missing-layer-for-comfyui-a-minimalist-ui-that-automatically-adapts-to-your-existing-workflows-8e9a78d6d0c8
- **Stack**: Gradio
- **What**: Tag node names with `<Label:Category:SortOrder>` and UI auto-generates. Tabs, columns, accordions. State in localStorage. Works as ComfyUI extension or standalone.
- **Mobile**: PWA via local network.
- **Verdict**: Most "zero config" -- auto-adapts any existing workflow.

### Comfy Controller (cg-controller)
- **URL**: https://github.com/chrisgoringe/cg-controller
- **What**: Integrated panel in ComfyUI. Right-click node > "Include this node" > appears in Controller with sliders, toggles, text fields. Workflow stays intact. Controller saved in workflow JSON.
- **Verdict**: Best for custom mini-UI directly inside ComfyUI.

### ComfyUI-disty-Flow
- **URL**: https://github.com/diStyApps/ComfyUI-disty-Flow
- **Access**: `http://127.0.0.1:8188/flow`
- **What**: Execution-focused interface. Canvas, inpainting, live previews, model gallery. Pre-made Flows for Flux, SD3.5, etc.
- **Verdict**: Good out-of-the-box with presets.

### SwarmUI (ex-StableSwarmUI)
- **URL**: https://github.com/mcmonkeyprojects/SwarmUI
- **Site**: https://swarmui.net/
- **What**: Full interface using ComfyUI as backend. Simple Generate tab (like A1111) + full Comfy Workflow tab. Near-automatic install.
- **Supports**: Flux, SD, Z-Image, Qwen Image, video (Wan, Hunyuan).
- **Verdict**: Best compromise simplicity/power. Recommended as primary frontend.

### Comflowy / Comflowyspace
- **URL**: https://github.com/6174/comflowy
- **Site**: https://www.comflowy.com/
- **What**: Desktop app + community. Simplified ComfyUI UX with built-in tutorials.

### comfyui-simple-frontend
- **URL**: https://github.com/Tiefflieger06/comfyui-simple-frontend
- **Stack**: Flask + Python
- **What**: Text field, Generate button, image. That's it. Keeps last 20 images.
- **Verdict**: Ultra-minimal. Kiosk mode.

---

## Curated List of All Alternative UIs

The same author as MCWW maintains an exhaustive, regularly updated list:

https://github.com/light-and-ray/awesome-alternative-uis-for-comfyui

---

## Recommendations by Use Case

| Need | Solution |
|---|---|
| Simplest possible per-workflow UI | ViewComfy (Playground mode) |
| Auto-generated UI from any workflow | MCWW |
| Full power + simple mode toggle | SwarmUI |
| Custom panel inside ComfyUI | cg-controller |
| Out-of-box with presets | disty-Flow |
| Total beginner | comfyui-simple-frontend |
