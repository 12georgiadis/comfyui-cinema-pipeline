# /user:comfy-batch -- Batch process files through ComfyUI

Process multiple files through a ComfyUI workflow.

## Usage
```
/user:comfy-batch <input_folder_or_files> <workflow_name_or_operation>
```

## Instructions

1. Identify input files:
   - If a folder path: list all compatible files (images: png/jpg/webp, videos: mp4/mov/webm)
   - If specific files: use those
   - Report the count to the user before starting

2. Identify the workflow:
   - If a workflow name from `workflows/`: use it
   - If an operation keyword: map to the right workflow
     - "upscale" → upscale.json
     - "style" → sdxl-style.json
     - "depth" → depth map extraction
     - "roto" / "mask" → SAM segmentation

3. Create output directory:
   - Same parent as input, with suffix `_processed`
   - Example: `input/frames/` → `input/frames_processed/`

4. Process sequentially (ComfyUI handles one at a time):
   - For each file:
     a. Submit to ComfyUI via MCP/API
     b. Wait for completion
     c. Save output to output directory
     d. Report progress: `[12/50] Processing frame_012.png...`

5. Error handling:
   - If a single file fails: log the error, skip, continue with next
   - If 3+ consecutive failures: stop and report the issue
   - At the end: report success count, failure count, and failed files

6. When complete:
   - Run `~/.claude/scripts/notify.sh "Batch termine: X/Y reussis"`
   - Report total processing time and output location

## Examples

```
/user:comfy-batch ./footage/frames/ upscale 4x
/user:comfy-batch ./stills/*.png style transfer avec reference.jpg
/user:comfy-batch ./clips/ wan22-camera dolly_in
```

ARGUMENTS: $ARGUMENTS
