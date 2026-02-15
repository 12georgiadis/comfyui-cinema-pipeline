#!/bin/bash
# Setup script for ComfyUI Cinema Pipeline
# Run this once to configure everything on a new machine.
#
# Usage: ./scripts/setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "========================================"
echo "  ComfyUI Cinema Pipeline - Setup"
echo "========================================"
echo ""

# 1. Check Python
echo "[1/6] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "  Found: $PYTHON_VERSION"
else
    echo "  ERROR: Python 3 not found. Install Python 3.10+ first."
    exit 1
fi

# 2. Clone MCP server if not present
echo ""
echo "[2/6] MCP Server..."
MCP_DIR="${PROJECT_DIR}/mcp-server"
if [ -d "$MCP_DIR" ]; then
    echo "  Already present at mcp-server/"
else
    echo "  Cloning joenorton/comfyui-mcp-server..."
    git clone https://github.com/joenorton/comfyui-mcp-server.git "$MCP_DIR"
    echo "  Done."
fi

# 3. Install Python dependencies
echo ""
echo "[3/6] Installing dependencies..."
if [ -f "$MCP_DIR/requirements.txt" ]; then
    pip install -q -r "$MCP_DIR/requirements.txt" 2>&1 | tail -1
    echo "  MCP server dependencies installed."
else
    echo "  WARNING: requirements.txt not found in mcp-server/"
fi

# Also install requests for our scripts
pip install -q requests 2>&1 | tail -1
echo "  Script dependencies installed."

# 4. Create .env from template
echo ""
echo "[4/6] Environment configuration..."
ENV_FILE="${PROJECT_DIR}/.env"
if [ -f "$ENV_FILE" ]; then
    echo "  .env already exists (keeping current config)"
else
    cp "${PROJECT_DIR}/.env.example" "$ENV_FILE"
    echo "  Created .env from template."
    echo "  IMPORTANT: Edit .env with your actual values:"
    echo "    - COMFYUI_URL (your Tailscale IP)"
    echo "    - COMFY_CLOUD_API_KEY (from platform.comfy.org)"
    echo "    - TELEGRAM_BOT_TOKEN (from @BotFather)"
    echo "    - TELEGRAM_CHAT_ID (from @userinfobot)"
fi

# 5. Make scripts executable
echo ""
echo "[5/6] Making scripts executable..."
chmod +x "${SCRIPT_DIR}/start-mcp-server.sh"
chmod +x "${SCRIPT_DIR}/test-connection.sh"
chmod +x "${SCRIPT_DIR}/detect-nodes.py"
chmod +x "${SCRIPT_DIR}/comfy-cloud-proxy.py"
chmod +x "${SCRIPT_DIR}/notify.py"
chmod +x "${SCRIPT_DIR}/export-pinokio-workflows.py"
echo "  All scripts are executable."

# 6. Verify setup
echo ""
echo "[6/6] Verifying setup..."
echo ""

# Check MCP server can import
if python3 -c "import sys; sys.path.insert(0, '$MCP_DIR'); import server" 2>/dev/null; then
    echo "  [+] MCP server: imports OK"
else
    echo "  [!] MCP server: import check failed (may need ComfyUI connection)"
fi

# Check .env values
source "$ENV_FILE" 2>/dev/null
if [ -n "$COMFYUI_URL" ] && [ "$COMFYUI_URL" != "http://TAILSCALE_IP_PC:8188" ]; then
    echo "  [+] COMFYUI_URL: configured ($COMFYUI_URL)"

    # Test connection
    if curl -s --connect-timeout 3 "${COMFYUI_URL}/system_stats" > /dev/null 2>&1; then
        echo "  [+] ComfyUI: ONLINE"
    else
        echo "  [!] ComfyUI: not reachable (start ComfyUI or check Tailscale)"
    fi
else
    echo "  [-] COMFYUI_URL: not configured yet (edit .env)"
fi

if [ -n "$COMFY_CLOUD_API_KEY" ] && [ "$COMFY_CLOUD_API_KEY" != "your_api_key_here" ]; then
    echo "  [+] Comfy Cloud: API key set"
else
    echo "  [-] Comfy Cloud: no API key"
fi

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ "$TELEGRAM_BOT_TOKEN" != "your_bot_token_here" ]; then
    echo "  [+] Telegram: configured"
else
    echo "  [-] Telegram: not configured"
fi

# Count workflows
WF_COUNT=$(ls -1 "${PROJECT_DIR}/workflows/"*.json 2>/dev/null | grep -cv '.meta.json' 2>/dev/null || echo 0)
echo "  [+] Workflows: ${WF_COUNT} templates available"

echo ""
echo "========================================"
echo "  Setup complete!"
echo "========================================"
echo ""
echo "  Next steps:"
echo "  1. Edit .env with your configuration"
echo "  2. Install Tailscale on Windows PC (see scripts/setup-tailscale-pc.md)"
echo "  3. Start MCP server: ./scripts/start-mcp-server.sh"
echo "  4. Detect nodes: python scripts/detect-nodes.py http://YOUR_IP:8188"
echo "  5. Use Claude Code commands: /user:comfy-generate, /user:comfy-status"
echo ""
