# CLAUDE.md -- ComfyUI Cinema Pipeline

## Projet
Infrastructure de production cinema avec ComfyUI, orchestree par Claude Code via MCP.

## Architecture
- **Mac (Mini ou MacBook)** : Claude Code, montage (FCP/DaVinci), orchestration
- **PC Windows RTX 5090** : ComfyUI via Pinokio, port 8188, accessible via Tailscale
- **Comfy Cloud** : Overflow GPU (96GB, $20/mois), API compatible local
- **Reseau** : Tailscale mesh VPN entre toutes les machines + iPhone

## Config ComfyUI
- **Local** : `http://TAILSCALE_IP_PC:8188` (remplacer par l'IP reelle)
- **Cloud** : `https://cloud.comfy.org/api/prompt` avec header `X-API-Key`
- **Workflows** : dans `./workflows/` (format API JSON avec placeholders MCP)

## Commandes disponibles
- `/user:comfy-generate <prompt>` -- Genere image/video
- `/user:comfy-workflow <description>` -- Cree un nouveau workflow en Python
- `/user:comfy-debug <error>` -- Debug une erreur ComfyUI
- `/user:comfy-batch <folder> <workflow>` -- Traitement batch
- `/user:comfy-status` -- Status du systeme

## Regles
- Toujours verifier que ComfyUI repond avant de lancer une generation
- Utiliser ComfyScript (Python) pour creer des workflows, pas du JSON brut
- Notifier via `~/.claude/scripts/notify.sh` en fin de generation
- Ne jamais telecharger de modeles sans demander (seulement recommander)
- En cas d'erreur VRAM : proposer Comfy Cloud, ne pas retry en boucle
- `@cloud` dans une commande = forcer Comfy Cloud
- `@local` = forcer le PC local (defaut)

## Fichiers importants
- `specs.md` -- Specs detaillees du projet
- `.mcp.json` -- Config MCP server
- `workflows/` -- Templates de workflows avec placeholders
- `scripts/` -- Scripts utilitaires (test connexion, export Pinokio)
- `docs/` -- Research complete (70+ workflows, NLE integration, etc.)
