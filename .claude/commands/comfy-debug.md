# /user:comfy-debug -- Debug a ComfyUI workflow error

Diagnose and fix ComfyUI workflow errors.

## Usage
```
/user:comfy-debug <error message or description of the problem>
```

## Instructions

1. Gather information:
   - Read the error message provided by the user
   - Query ComfyUI `/queue` to check current state
   - Query `/history` for recent execution results
   - If a workflow file is mentioned, read it

2. Common error patterns and fixes:

   | Error pattern | Likely cause | Fix |
   |---|---|---|
   | `NodeNotFound` | Custom node not installed | Tell user which package to install |
   | `OutOfMemoryError` / `CUDA OOM` | Insufficient VRAM | Reduce resolution, use GGUF model, or switch to @cloud |
   | `FileNotFoundError` for model | Model not downloaded | Give download link and path |
   | `Input type mismatch` | Wrong connection between nodes | Identify the incompatible types and suggest fix |
   | `ValueError: Sampler` | Invalid sampler/scheduler combo | List valid options for the model |
   | `Connection refused` | ComfyUI not running | Check if Pinokio/ComfyUI is started |
   | `Timeout` | Generation too long or crashed | Check queue status, suggest interrupt |

3. For simple errors (parameter types, missing connections):
   - Fix automatically if possible
   - Re-run the workflow
   - Notify the user of the fix

4. For complex errors (node incompatibilities, model issues):
   - Explain the problem clearly
   - Propose 2-3 solutions ranked by simplicity
   - Ask the user which approach to take

5. If the error is in a custom ComfyScript workflow:
   - Read the Python script
   - Identify the issue
   - Fix and save the corrected version

ARGUMENTS: $ARGUMENTS
