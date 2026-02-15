#!/bin/bash
# Lance le MCP server ComfyUI
# Usage: ./start-mcp-server.sh [COMFYUI_IP:PORT]
#
# Le server ecoute sur http://127.0.0.1:9000/mcp
# Claude Code s'y connecte via .mcp.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MCP_DIR="${PROJECT_DIR}/mcp-server"

# ComfyUI target (PC Windows via Tailscale)
export COMFYUI_URL="${1:-http://TAILSCALE_IP_PC:8188}"

# Workflow directory
export COMFY_MCP_WORKFLOW_DIR="${PROJECT_DIR}/workflows"

echo "=== ComfyUI MCP Server ==="
echo "ComfyUI target: ${COMFYUI_URL}"
echo "Workflows dir:  ${COMFY_MCP_WORKFLOW_DIR}"
echo "MCP endpoint:   http://127.0.0.1:9000/mcp"
echo ""

# Check if ComfyUI is reachable
if curl -s --connect-timeout 5 "${COMFYUI_URL}/system_stats" > /dev/null 2>&1; then
    echo "ComfyUI: ONLINE"
else
    echo "WARNING: ComfyUI not reachable at ${COMFYUI_URL}"
    echo "The server will start but generation will fail until ComfyUI is available."
fi
echo ""

cd "$MCP_DIR"
python server.py
