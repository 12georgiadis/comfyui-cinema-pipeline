# /user:comfy-generate -- Generate image/video via ComfyUI

Generate content using ComfyUI via MCP server.

## Usage
```
/user:comfy-generate <prompt>
```

## Instructions

1. Determine the type of content from the prompt:
   - If it mentions "video", "clip", "animation", "mouvement" → use video workflow (Wan 2.2 T2V or LTX Quick)
   - If it mentions "upscale", "ameliorer", "restaurer" → use upscale workflow
   - If it mentions "style", "transfert", "look" → use style transfer workflow
   - Otherwise → use image generation (SDXL or Flux)

2. Use the MCP tool `run_workflow` with the appropriate workflow template from the `workflows/` directory

3. Pass the user's prompt as `PARAM_PROMPT`

4. Monitor the generation via `get_job` or WebSocket

5. When done:
   - Report the output file path
   - If running in a terminal that supports images (iTerm2), display it
   - Run `~/.claude/scripts/notify.sh "Generation terminee"` to notify

6. If it fails:
   - Read the error from ComfyUI
   - If it's a missing node: tell the user which custom node to install
   - If it's VRAM: suggest reducing resolution or using @cloud
   - If it's a missing model: tell the user which model to download
   - For simple errors (wrong parameter type, etc.): fix and retry automatically

## Parameters

- `@cloud` anywhere in the prompt → force Comfy Cloud instead of local
- `@local` → force local (default)
- Resolution can be specified: `1024x1024`, `720p`, `1080p`
- Duration for video: `3s`, `5s`, `10s`

## Examples

```
/user:comfy-generate plan large nocturne Tokyo pluie neon film noir
/user:comfy-generate @cloud video dolly in foret brumeuse aube 5s
/user:comfy-generate upscale ./input/frame_001.png 4x
/user:comfy-generate style transfer ./reference.jpg sur ./footage.mp4
```

ARGUMENTS: $ARGUMENTS
