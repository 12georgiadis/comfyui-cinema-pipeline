#!/bin/bash
# Test la connexion entre cette machine et ComfyUI sur le PC Windows
# Usage: ./test-connection.sh [IP_TAILSCALE]

IP="${1:-TAILSCALE_IP_PC}"
PORT="8188"
URL="http://${IP}:${PORT}"

echo "=== Test connexion ComfyUI ==="
echo "Cible: ${URL}"
echo ""

# Test 1: Ping Tailscale
echo "[1/4] Ping Tailscale..."
if ping -c 1 -W 3 "$IP" > /dev/null 2>&1; then
    echo "  OK - Le PC repond au ping"
else
    echo "  ERREUR - Le PC ne repond pas. Verifier:"
    echo "    - Tailscale est installe et connecte sur le PC ?"
    echo "    - Le PC est allume ?"
    echo "    - L'IP est correcte ? (check https://login.tailscale.com/admin/machines)"
    exit 1
fi

# Test 2: Port ComfyUI
echo "[2/4] Port ComfyUI (${PORT})..."
if curl -s --connect-timeout 5 "${URL}/system_stats" > /dev/null 2>&1; then
    echo "  OK - ComfyUI repond sur le port ${PORT}"
else
    echo "  ERREUR - ComfyUI ne repond pas. Verifier:"
    echo "    - ComfyUI est lance dans Pinokio ?"
    echo "    - ComfyUI est lance avec --listen 0.0.0.0 ?"
    echo "    - Le pare-feu Windows bloque le port ${PORT} ?"
    exit 1
fi

# Test 3: System stats
echo "[3/4] System stats..."
STATS=$(curl -s --connect-timeout 5 "${URL}/system_stats")
if [ -n "$STATS" ]; then
    echo "  OK - Stats recues:"
    echo "$STATS" | python3 -m json.tool 2>/dev/null || echo "$STATS"
else
    echo "  ERREUR - Pas de stats retournees"
    exit 1
fi

# Test 4: Object info (verifie que les nodes sont charges)
echo "[4/4] Noeuds disponibles..."
NODE_COUNT=$(curl -s --connect-timeout 10 "${URL}/object_info" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ -n "$NODE_COUNT" ] && [ "$NODE_COUNT" -gt 0 ]; then
    echo "  OK - ${NODE_COUNT} noeuds disponibles"
else
    echo "  ATTENTION - Impossible de compter les noeuds (peut etre long a charger)"
fi

echo ""
echo "=== Tous les tests passes ==="
echo "ComfyUI est accessible a ${URL}"
echo ""
echo "Prochaine etape: mettre a jour .mcp.json avec IP=${IP}"
