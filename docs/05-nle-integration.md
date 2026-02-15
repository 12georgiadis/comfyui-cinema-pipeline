# NLE Integration with ComfyUI

Status of ComfyUI integration with professional video editing software. Honest assessments.

**TL;DR**: No NLE has native ComfyUI integration. DaVinci Resolve is closest. The workflow today is export -> process in ComfyUI -> reimport.

---

## 1. DaVinci Resolve + ComfyUI

### Stability: 5/10 -- Best positioned

**Direct integrations**:

- [comfyUI_DaVinciResolve](https://github.com/barckley75/comfyUI_DaVinciResolve) -- TTS audio only. Dormant. 2/10 stability.
- [DaVinci Resolve MCP (Gursky)](https://github.com/samuelgursky/davinci-resolve-mcp) -- MCP bridge for AI assistants. Claude/Cursor can control Resolve.
- [DaVinci Resolve MCP (Tooflex)](https://glama.ai/mcp/servers/@Tooflex/davinci-resolve-mcp) -- Can execute Lua scripts in Fusion, control all pages.

**Why Resolve is the best option**:
- Full [Python/Lua scripting API](https://deric.github.io/DaVinciResolve-API-Docs/)
- Fusion has its own [scripting guide](https://documents.blackmagicdesign.com/UserManuals/Fusion8_Scripting_Guide.pdf)
- 2 MCP servers already exist
- A custom pipeline is technically feasible:
  1. Script exports clips from timeline (Python API)
  2. Send to ComfyUI via REST/WebSocket API
  3. Receive processed frames
  4. Re-import into timeline via script

**No one has built a production-ready roundtrip yet.** This is the development opportunity.

**Training resources**:
- [Mixing Light ComfyUI Series](https://mixinglight.com/color-grading-tutorials/comfyui-localhost-overview-digital-post-production-part-1/) (5 parts, Oct 2025 - Feb 2026) by Igor Ridjanovic
- [Blackmagic Forum discussions](https://forum.blackmagicdesign.com/viewtopic.php?t=203462&p=1056812) on depth maps + Resolve relight
- [ActionVFX "ComfyUI for VFX"](https://www.actionvfx.com/blog/comfyui-for-vfx) -- EXR workflow for compositing

---

## 2. Final Cut Pro + ComfyUI

### Stability: 0/10 -- Dead end

- **No integration exists**. Apple's walled garden.
- [FxPlug](https://developer.apple.com/documentation/fxplug) SDK (Metal only, v4.3.x) is the only path. Would require building a Swift/Metal plugin that communicates with ComfyUI HTTP.
- Third-party AI plugins (MotionVFX, CommandPost) focus on captions/auto-editing, not generative AI.
- FCP 11 has built-in ML (Magnetic Mask, Smart Conform, Object Tracking) but limited to Apple's models.
- **Verdict**: Impractical. Would require major Swift/Metal development with no existing building blocks.

---

## 3. Adobe Premiere Pro + ComfyUI

### Stability: 0/10 -- Nothing exists, but buildable

- **No plugin exists**.
- Adobe transitioning from CEP (legacy) to [UXP](https://blog.developer.adobe.com/en/publish/2025/12/uxp-arrives-in-premiere-a-new-era-for-plugin-development) (Premiere Pro 25.6, Dec 2025).
- **UXP makes building a bridge feasible**:
  1. JavaScript-based panel calls ComfyUI REST API
  2. Sends selected clip frames to ComfyUI
  3. Receives results, imports to timeline
- Probably the easiest NLE to build a bridge for (after Blender), thanks to JS extensions.
- Adobe's Firefly is cloud-based and limited compared to ComfyUI.

---

## 4. Blender + ComfyUI

### 4a. Pallaidium (tin2tin) -- 5/10

- **URL**: https://github.com/tin2tin/Pallaidium (1.3K stars)
- **What**: Generative AI movie studio in Blender's VSE. Does NOT use ComfyUI -- runs models directly.
- **Capabilities**: T2V, T2I, T2S, T2M, V2V, I2I, I2V, LoRA, cloud (MiniMax)
- **Limitations**:
  - **Windows only** (macOS officially unsupported)
  - Painful installation
  - Rapid churn breaks workflows
  - img2img video disabled ("too flickering")
  - Low community engagement
  - VSE is not a serious NLE

### 4b. ComfyUI-BlenderAI-node (AIGODLIKE) -- 4/10

- **URL**: https://github.com/AIGODLIKE/ComfyUI-BlenderAI-node (1.4K stars)
- **What**: ComfyUI nodes as Blender nodes. ComfyUI as server, controlled from Blender.
- **Capabilities**: AI materials, camera input, animation interpolation, grease pencil masks, VSE export
- **Companion**: [ComfyUI-CUP](https://github.com/AIGODLIKE/ComfyUI-CUP)
- **Problems** (acknowledged by devs):
  - "90% of users fail installation"
  - "Cumbersome user interaction"
  - "Failure to work out of the box"
  - Major update planned Feb 2026
- **Fork**: [a-One-Fan/ComfyUI-BlenderAI-node-editor](https://github.com/a-One-Fan/ComfyUI-BlenderAI-node-editor) -- improved version

---

## 5. After Effects + ComfyUI

### Stability: 1/10

- [AppMana plugin](https://github.com/AppMana/appmana-comfyui-after-effects-plugin) -- Pre-alpha. 7 stars, Rust, requires AE 2023 SDK.
- Practical path: render from ComfyUI to EXR/PNG sequences, import into AE.
- [ActionVFX course](https://www.actionvfx.com/blog/comfyui-for-vfx) teaches this ($197, 15 modules).
- [fxphd course](https://www.fxphd.com/details/713/) -- Generative AI for VFX with ComfyUI & InvokeAI.

---

## 6. ComfyUI as NLE (Timeline Nodes)

### ComfyUI-Montagen -- 3/10
- **URL**: https://github.com/MontagenAI/ComfyUI-Montagen (28 stars, v0.2.4)
- Timeline editor inside ComfyUI. Early stage.

### TimeUI -- 2/10
- **URL**: https://github.com/jimmm-ai/TimeUi-a-ComfyUi-Timeline-Node
- Timeline node system. Very experimental.

Not practical for serious editing.

---

## 7. Real-Time Processing

### ComfyStream (Livepeer)
- **URL**: https://blog.livepeer.org/comfyui-and-real-time-video-ai-processing/
- Applies workflows to live video streams.

### ComfyUI_RealtimeNodes
- **URL**: https://github.com/ryanontheinside/ComfyUI_RealtimeNodes
- Webcam capture, motion detection, real-time multimedia.

Real-time works for simple workflows (style transfer, LTX). Not for heavy processing.

---

## 8. General Approaches

### A. Manual Roundtrip (Works Now)
Export -> Load in ComfyUI -> Process -> Export -> Reimport. Works with any NLE.

### B. API + Custom Script (Semi-automated)
Watch folder -> Queue ComfyUI workflows -> Move results -> Trigger NLE import.

### C. Batch Automation
ComfyUI supports [robust batch processing](https://apatero.com/blog/automate-images-videos-comfyui-workflow-guide-2025):
- Auto Queue (continuous loop)
- CSV-driven batch
- Folder-based batch

---

## 9. Krea.ai Feature Mapping

| Krea Feature | ComfyUI Equivalent |
|---|---|
| Inpainting | comfyui-inpaint-nodes (Acly), Fooocus, LaMa, MAT |
| Outpainting | Pad Image, Wan 2.1 VACE (video outpaint) |
| Style Transfer | IPAdapter + ControlNet |
| Upscaling | ESRGAN, SeedVR2, SUPIR |
| Extend Shots | Wan 2.1, LTX, HunyuanVideo (I2V from last frame) |
| Camera Motion | Wan 2.1 camera control, AnimateDiff MotionLoRA |
| Lip-sync | LatentSync, Wav2Lip nodes |

Krea has an [API (Dec 2025)](https://docs.krea.ai/home) but no NLE plugin.

---

## Summary

| NLE | Integration Score | Path Forward |
|---|---|---|
| **DaVinci Resolve** | 5/10 | Python API + MCP + custom bridge. Best bet. |
| **Premiere Pro** | 0/10 | UXP plugin buildable. JS-based, feasible. |
| **Final Cut Pro** | 0/10 | Apple walled garden. Impractical. |
| **Blender** | 4/10 | Has nodes but 90% fail rate. Wait for Feb 2026 update. |
| **After Effects** | 1/10 | Pre-alpha plugin only. Use EXR workflow. |
| **Manual batch** | 8/10 | Most practical today. |
