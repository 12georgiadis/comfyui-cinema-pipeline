# /user:comfy-status -- Check ComfyUI system status

Check the status of ComfyUI (local and cloud), queue, and system resources.

## Usage
```
/user:comfy-status
```

## Instructions

1. Check local ComfyUI:
   - Ping the Tailscale IP
   - Query `/system_stats` for GPU info (VRAM usage, Python version, OS)
   - Query `/queue` for running and pending jobs
   - Report: online/offline, VRAM free/total, queue length

2. Check Comfy Cloud (if API key available):
   - Query the cloud API status
   - Report: available, credits remaining

3. Format output:
   ```
   === ComfyUI Status ===

   Local (RTX 5090):
     Status:  ONLINE
     VRAM:    8.2 / 32.0 GB used
     Queue:   2 running, 0 pending
     Uptime:  3h 42m

   Cloud (RTX 6000 Pro):
     Status:  AVAILABLE
     Credits: 2,150 remaining (~1h48 GPU)

   Network:
     Tailscale: Connected
     Latency:   12ms
   ```

4. If local is offline, suggest:
   - Check if Pinokio/ComfyUI is running on the PC
   - Check Tailscale connection
   - Offer to use Comfy Cloud instead

ARGUMENTS: $ARGUMENTS
