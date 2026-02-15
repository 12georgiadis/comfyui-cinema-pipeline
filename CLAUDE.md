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

## Workflows disponibles
| Template | Description | VRAM |
|---|---|---|
| `sdxl_cinema_image` | Image SDXL (concept art, stills) | 8GB |
| `wan_t2v` | Wan 2.1 Text-to-Video | 24GB |
| `img2img_cinema` | Image-to-Image (variations, looks) | 8GB |
| `upscale_esrgan` | Upscale 4x (Real-ESRGAN) | 2GB |
| `frame_interpolation` | Slow-motion RIFE | 4GB |
| `wan_i2v` | Wan 2.1 Image-to-Video | 28GB |
| `depth_map` | Depth Anything V2 (VFX) | 2GB |

Chaque workflow a un `.meta.json` avec les defaults, contraintes, modeles recommandes.

## Scripts utilitaires
- `scripts/start-mcp-server.sh` -- Demarre le MCP server (charge .env)
- `scripts/detect-nodes.py` -- Detecte les nodes installes et verifie compatibilite
- `scripts/comfy-cloud-proxy.py` -- Client API Comfy Cloud
- `scripts/test-connection.sh` -- Test connexion Tailscale
- `scripts/export-pinokio-workflows.py` -- Export workflows Pinokio
- `scripts/install-cinema-nodes.md` -- Guide d'installation des custom nodes

## Fichiers importants
- `specs.md` -- Specs detaillees du projet
- `.mcp.json` -- Config MCP server
- `.env.example` -- Variables d'environnement (copier vers .env)
- `workflows/` -- Templates de workflows avec placeholders et metadata
- `scripts/` -- Scripts utilitaires
- `docs/` -- Research complete (70+ workflows, NLE integration, etc.)
