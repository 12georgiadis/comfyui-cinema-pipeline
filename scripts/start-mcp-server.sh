#!/bin/bash
# Lance le MCP server ComfyUI
# Usage: ./start-mcp-server.sh [COMFYUI_URL]
#
# Le server ecoute sur http://127.0.0.1:9000/mcp
# Claude Code s'y connecte via .mcp.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MCP_DIR="${PROJECT_DIR}/mcp-server"

# Load .env file if it exists
ENV_FILE="${PROJECT_DIR}/.env"
if [ -f "$ENV_FILE" ]; then
    echo "Loading config from .env..."
    set -a
    source "$ENV_FILE"
    set +a
fi

# ComfyUI target (CLI arg > .env > placeholder)
export COMFYUI_URL="${1:-${COMFYUI_URL:-http://TAILSCALE_IP_PC:8188}}"

# Workflow directory (cinema templates)
export COMFY_MCP_WORKFLOW_DIR="${PROJECT_DIR}/workflows"

echo ""
echo "========================================"
echo "  ComfyUI Cinema Pipeline - MCP Server"
echo "========================================"
echo ""
echo "  ComfyUI target: ${COMFYUI_URL}"
echo "  Workflows dir:  ${COMFY_MCP_WORKFLOW_DIR}"
echo "  MCP endpoint:   http://127.0.0.1:9000/mcp"
echo ""

# Count available workflow templates
WF_COUNT=$(ls -1 "${COMFY_MCP_WORKFLOW_DIR}"/*.json 2>/dev/null | grep -v '.meta.json' | wc -l | tr -d ' ')
echo "  Workflow templates: ${WF_COUNT}"
echo ""

# Check if ComfyUI is reachable
if curl -s --connect-timeout 5 "${COMFYUI_URL}/system_stats" > /dev/null 2>&1; then
    echo "  [+] ComfyUI: ONLINE"
    # Get GPU info if available
    GPU_INFO=$(curl -s --connect-timeout 5 "${COMFYUI_URL}/system_stats" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    devices = data.get('devices', [])
    for d in devices:
        name = d.get('name', 'Unknown')
        vram = d.get('vram_total', 0)
        vram_gb = round(vram / (1024**3), 1)
        print(f'      GPU: {name} ({vram_gb}GB VRAM)')
except: pass
" 2>/dev/null)
    if [ -n "$GPU_INFO" ]; then
        echo "$GPU_INFO"
    fi
else
    echo "  [!] ComfyUI: OFFLINE at ${COMFYUI_URL}"
    echo "      Server will start and retry connection."
fi

# Check Comfy Cloud
if [ -n "$COMFY_CLOUD_API_KEY" ] && [ "$COMFY_CLOUD_API_KEY" != "your_api_key_here" ]; then
    echo "  [+] Comfy Cloud: API key configured"
else
    echo "  [-] Comfy Cloud: No API key (local-only mode)"
fi

echo ""
echo "========================================"
echo ""

cd "$MCP_DIR"
python server.py
