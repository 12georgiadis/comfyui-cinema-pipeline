# /user:comfy-workflow -- Create a new ComfyUI workflow

Create a new ComfyUI workflow from a natural language description using ComfyScript (Python).

## Usage
```
/user:comfy-workflow <description of what the workflow should do>
```

## Instructions

1. Parse the user's description to understand:
   - Input type (image, video, text, nothing)
   - Processing steps (style transfer, depth, inpainting, etc.)
   - Output type (image, video)
   - Required models and nodes

2. Check which nodes are available on the target ComfyUI by querying `/object_info`

3. Write the workflow as a ComfyScript Python script:
   ```python
   from comfy_script.runtime import *
   load("http://TAILSCALE_IP_PC:8188/")

   with Workflow():
       # ... nodes ...
   ```

4. Validate the script:
   - All node names exist in `/object_info`
   - All model names exist in `/models`
   - All connections are type-compatible

5. If a required node is missing, tell the user:
   - Which custom node package to install
   - The install command (via ComfyUI Manager or git clone)

6. Save the script in `workflows/` as both:
   - `.py` file (ComfyScript, for future Claude use)
   - `.json` file (API format, for MCP/Telegram/MCWW use)

7. Ask the user if they want to test it now

## Examples

```
/user:comfy-workflow prend une image, extrait le depth map, genere une video Wan 2.2 avec camera dolly in lent
/user:comfy-workflow charge une video, applique un style painterly, propage avec EbSynth, exporte
/user:comfy-workflow batch: pour chaque image dans un dossier, upscale 4x avec SeedVR2 et sauvegarde
```

ARGUMENTS: $ARGUMENTS
