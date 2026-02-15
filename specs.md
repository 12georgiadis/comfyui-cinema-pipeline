# Specs -- ComfyUI Cinema Pipeline

## Vue d'ensemble

Systeme d'orchestration connectant **Claude Code** (LLM CLI) a **ComfyUI** pour la production cinema. Un seul MCP server pilote ComfyUI local (RTX 5090) et Comfy Cloud (96GB), avec acces mobile et notifications.

**Utilisateur** : Ismael Joffroy Chandoutis, cineaste, usage solo.
**Objectif** : Pouvoir depuis n'importe quel terminal (Mac, Mac Mini, iPhone) demander a Claude de generer, transformer, debugger, et creer des workflows ComfyUI.

---

## Architecture physique

```
┌──────────────────────────────────────────────────────────────┐
│                        RESEAU TAILSCALE                      │
│                                                              │
│  ┌───────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ Mac Mini  │    │ MacBook Air  │    │ iPhone / iPad    │  │
│  │ (hub 24/7)│    │ (mobile)     │    │ (Telegram/Safari)│  │
│  │           │    │              │    │                  │  │
│  │ Claude    │    │ Claude Code  │    │ ComfyUI-TG bot   │  │
│  │ Code      │    │ FCP montage  │    │ MCWW PWA         │  │
│  │ DaVinci   │    │              │    │ Comfy Portal app │  │
│  └─────┬─────┘    └──────┬───────┘    └────────┬─────────┘  │
│        │                 │                     │             │
│        └────────────┬────┴─────────────────────┘             │
│                     │                                        │
│           ┌─────────▼──────────┐                             │
│           │ PC Windows         │                             │
│           │ RTX 5090 32GB      │                             │
│           │ ComfyUI (Pinokio)  │                             │
│           │ Port 8188          │                             │
│           │ Always on          │                             │
│           └────────────────────┘                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                          │
                ┌─────────▼──────────┐
                │ Comfy Cloud        │
                │ RTX 6000 Pro 96GB  │
                │ $20/mois Standard  │
                │ API compatible     │
                └────────────────────┘
```

---

## Phase 0 : Prerequis reseau

### Installer Tailscale sur le PC Windows

**Pourquoi** : Sans Tailscale, Claude Code sur le Mac ne peut pas joindre ComfyUI sur le PC quand on est hors du reseau local. AnyDesk/Parsec sont des solutions d'ecran distant, pas de reseau.

**Actions** :
1. Telecharger Tailscale sur le PC Windows : https://tailscale.com/download/windows
2. Se connecter avec le meme compte que le Mac
3. Noter l'IP Tailscale du PC (ex: `100.x.y.z`)
4. Verifier : depuis le Mac, `ping 100.x.y.z` doit repondre
5. Verifier : depuis le Mac, `curl http://100.x.y.z:8188/system_stats` doit retourner du JSON

### Ouvrir ComfyUI au reseau

ComfyUI dans Pinokio doit etre lance avec `--listen 0.0.0.0` pour accepter les connexions externes.

**Action** : Dans les parametres Pinokio de ComfyUI, ajouter le flag `--listen 0.0.0.0` aux arguments de lancement. Ou editer le script de demarrage.

---

## Phase 1 : MCP Server ComfyUI

### Choix technique : joenorton/comfyui-mcp-server

**Pourquoi celui-la** :
- Auto-decouverte des workflows (drop un JSON dans `workflows/`, il devient un outil)
- Transport HTTP (pas WebSocket = plus stable via Tailscale)
- Le plus riche en outils (12 outils natifs)
- Supporte les placeholders types (`PARAM_PROMPT`, `PARAM_INT_STEPS`, etc.)

**Alternative si probleme** : IO-AtelierTech/comfyui-mcp (29 outils, validation schema)

### Installation

Le MCP server tourne **sur la meme machine que Claude Code** (Mac Mini ou MacBook). Il se connecte a ComfyUI distant via HTTP.

```
Claude Code (Mac) → MCP Server (Mac) → HTTP → ComfyUI (PC Windows :8188)
                                       → HTTP → Comfy Cloud API
```

**Config `.mcp.json`** dans le projet :
```json
{
  "mcpServers": {
    "comfyui-local": {
      "command": "node",
      "args": ["/path/to/comfyui-mcp-server/dist/index.js"],
      "env": {
        "COMFYUI_URL": "http://<tailscale-ip-pc>:8188",
        "WORKFLOW_DIR": "./workflows"
      }
    }
  }
}
```

### Dual target (local + cloud)

Un seul MCP server avec un wrapper qui route vers local ou cloud :

- **Defaut** : ComfyUI local (RTX 5090). Gratuit, rapide, toujours dispo.
- **Explicite** : `@cloud` dans la commande pour forcer Comfy Cloud.
- **Auto-fallback** : Si le local ne repond pas, proposer de basculer sur cloud (ne pas le faire sans demander).

L'API Comfy Cloud est compatible avec l'API locale. Seuls changements :
- URL : `https://cloud.comfy.org/api/prompt`
- Header : `X-API-Key: <token>`

### Workflows a pre-charger

Copier les workflows les plus utilises dans le dossier `workflows/` du MCP server avec les placeholders :

| Workflow | Fichier | Placeholders |
|---|---|---|
| Wan 2.2 T2V | `wan22-t2v.json` | `PARAM_PROMPT`, `PARAM_INT_STEPS`, `PARAM_INT_WIDTH`, `PARAM_INT_HEIGHT` |
| Wan 2.2 Camera | `wan22-camera.json` | `PARAM_PROMPT`, `PARAM_COMBO_CAMERA_TYPE` |
| HunyuanVideo T2V | `hunyuan-t2v.json` | `PARAM_PROMPT`, `PARAM_INT_STEPS` |
| LTX Quick | `ltx-quick.json` | `PARAM_PROMPT` |
| SDXL Style Transfer | `sdxl-style.json` | `PARAM_PROMPT`, `PARAM_IMAGE_STYLE` |
| Upscale SeedVR2 | `upscale.json` | `PARAM_IMAGE_INPUT` |
| VACE Inpaint | `vace-inpaint.json` | `PARAM_VIDEO_INPUT`, `PARAM_MASK` |

Les workflows existants dans Pinokio seront exportes au format API et places dans ce dossier.

---

## Phase 2 : ComfyScript (creation de workflows par LLM)

### Pourquoi ComfyScript

Claude Code genere du Python plus fiable que du JSON brut. ComfyScript offre :
- Type hints (enums pour modeles, samplers, schedulers)
- Auto-completion / validation
- Lisible et debuggable
- Executable directement

### Installation

```bash
pip install comfy-script
```

ComfyScript se connecte au meme ComfyUI distant :
```python
from comfy_script.runtime import *
load("http://<tailscale-ip-pc>:8188/")
```

### Usage type

Claude Code recoit : "Fais-moi un workflow qui prend une image, applique un depth map, puis genere une video Wan 2.2 avec camera dolly in"

Claude ecrit :
```python
from comfy_script.runtime import *
load("http://100.x.y.z:8188/")

with Workflow():
    image = LoadImage("input.png")
    depth = DepthAnythingV3(image, model="large")
    video = Wan22FunCamera(image, depth, camera_type="dolly_in", steps=30)
    SaveVideo(video, "output.mp4")
```

### Validation

Avant execution, Claude :
1. Verifie que les noeuds existent via `/object_info`
2. Verifie que les modeles sont charges via `/models`
3. Soumet et surveille via WebSocket
4. Rapporte le resultat ou l'erreur

---

## Phase 3 : Acces mobile

### Telegram Bot (ComfyUI-TG)

**Installation sur le PC Windows** (dans ComfyUI custom_nodes) :
```
comfy node registry-install ComfyUI-TG
```

**Config** :
1. Creer un bot via @BotFather (nom : `ComfyCinemaBot` ou similaire)
2. Token dans `ComfyUI/Telegram/telegram.json`
3. Exporter les workflows principaux au format API avec le noeud `TG-ImageSaver`
4. Uploader via le dashboard Telegram

**Usage** : `/wf 1` → `/s 6 1 "plan large nocturne Tokyo"` → `/q` → image dans le chat.

### MCWW (PWA mobile)

**Installation** : Via ComfyUI Manager, rechercher "Minimalistic Comfy Wrapper WebUI".

**Config** :
1. Taguer les noeuds editables dans les workflows principaux avec `<Label:Category:Order>`
2. Acceder via `http://<tailscale-ip-pc>:8188/mcww` depuis Safari sur iPhone
3. Ajouter a l'ecran d'accueil (Share → Add to Home Screen)

### Comfy Portal (App Store)

Installer depuis l'App Store. Ajouter le serveur : `<tailscale-ip-pc>:8188`.

---

## Phase 4 : Notifications

### Systeme unifie

Utiliser le script `~/.claude/scripts/notify.sh` deja en place (son Zelda + push Telegram).

**Declencheurs** :
- Fin de generation : Claude appelle `notify.sh "Generation terminee : <description>"`
- Erreur : Claude appelle `notify.sh "Erreur ComfyUI : <message>"`
- Batch termine : Claude appelle `notify.sh "Batch X/Y termine"`

### Telegram Sender (en complement du bot)

Installer `Comfyui-TelegramSender` pour les generations lancees directement dans ComfyUI (pas via Claude) :
- Les resultats arrivent dans un channel Telegram dedie
- Utile quand on lance depuis l'interface web et qu'on est parti

---

## Phase 5 : NLE Round-trip

### Workflow FCP → ComfyUI → FCP

FCP n'a pas d'API. Le round-trip est manuel mais structurable :

1. **Export depuis FCP** : Selection → Share → Master File (ProRes) dans un dossier surveille (`~/ComfyUI-Exchange/input/`)
2. **ComfyUI traite** : Un workflow batch surveille le dossier, traite les fichiers, sort dans `~/ComfyUI-Exchange/output/`
3. **Import dans FCP** : Reimporter le fichier traite dans le projet

Claude Code peut automatiser les etapes 2 (lancer le bon workflow via MCP) et notifier quand c'est pret.

### DaVinci Resolve (VFX round-trips)

Pour les operations VFX lourdes :
1. Installer le MCP DaVinci Resolve (Tooflex) sur le Mac
2. Claude Code orchestre : export plan depuis Resolve → envoie a ComfyUI → reimporte
3. Script Python utilisant l'API Resolve pour automatiser export/import

**A developper en Phase 5** : pas prioritaire maintenant.

---

## Structure du repo

```
comfyui-cinema-pipeline/
├── README.md                          # Overview + architecture
├── specs.md                           # Ce document
├── docs/                              # Research (public, deja pousse)
│   ├── 01-claude-code-integration.md
│   ├── 02-cinema-workflows.md
│   ├── 03-simplified-frontends.md
│   ├── 04-mobile-remote-access.md
│   ├── 05-nle-integration.md
│   ├── 06-hybrid-local-cloud.md
│   ├── 07-ocs-perilli.md
│   └── 08-hardware.md
├── workflows/                         # Workflow JSON templates pour MCP
│   ├── wan22-t2v.json
│   ├── wan22-camera.json
│   ├── hunyuan-t2v.json
│   ├── ltx-quick.json
│   ├── sdxl-style.json
│   ├── upscale.json
│   └── vace-inpaint.json
├── scripts/                           # Scripts utilitaires
│   ├── export-pinokio-workflows.py    # Exporte les workflows Pinokio en format API
│   ├── setup-tailscale-pc.md          # Guide d'install Tailscale sur le PC
│   └── test-connection.sh             # Teste la connexion Mac → PC ComfyUI
├── .mcp.json                          # Config MCP server pour Claude Code
└── .claude/
    └── commands/
        ├── comfy-generate.md          # /user:comfy-generate <prompt>
        ├── comfy-workflow.md           # /user:comfy-workflow <description>
        ├── comfy-debug.md              # /user:comfy-debug <error>
        └── comfy-batch.md              # /user:comfy-batch <folder> <workflow>
```

---

## Stack technique

| Composant | Technologie |
|---|---|
| MCP Server | joenorton/comfyui-mcp-server (Node.js) |
| Workflow creation | ComfyScript (Python) |
| ComfyUI local | Pinokio sur Windows, port 8188 |
| ComfyUI cloud | Comfy Cloud Standard ($20/mois) |
| Reseau | Tailscale (mesh VPN) |
| Mobile | ComfyUI-TG (Telegram) + MCWW (PWA) + Comfy Portal (iOS) |
| Notifications | notify.sh (Zelda + Telegram) |
| NLE principal | Final Cut Pro (montage) + DaVinci Resolve (VFX) |
| Repo | GitHub public (comfyui-cinema-pipeline) |

---

## Plan d'implementation

### Etape 0 : Reseau (prerequis)
- [ ] Installer Tailscale sur le PC Windows
- [ ] Configurer ComfyUI Pinokio avec `--listen 0.0.0.0`
- [ ] Tester la connexion depuis le Mac : `curl http://<ip>:8188/system_stats`
- [ ] Tester depuis l'iPhone (Safari via Tailscale)

### Etape 1 : MCP Server basique
- [ ] Cloner joenorton/comfyui-mcp-server
- [ ] Configurer `.mcp.json` avec l'IP Tailscale du PC
- [ ] Tester : `Claude, liste les modeles disponibles sur ComfyUI`
- [ ] Tester : `Claude, genere une image avec le prompt "X"`
- [ ] Ajouter la config Comfy Cloud (URL + API key)
- [ ] Tester : `Claude, genere sur le cloud avec le prompt "X"`

### Etape 2 : Workflows cinema
- [ ] Exporter les workflows principaux depuis Pinokio au format API
- [ ] Placer dans `workflows/` avec les placeholders MCP
- [ ] Tester chaque workflow via Claude Code
- [ ] Creer les Claude commands (`.claude/commands/`)

### Etape 3 : ComfyScript
- [ ] Installer ComfyScript sur le Mac
- [ ] Tester la connexion distante a ComfyUI
- [ ] Creer un premier workflow en Python via Claude
- [ ] Valider : Claude cree + execute + recoit le resultat

### Etape 4 : Mobile
- [ ] Installer ComfyUI-TG sur le PC (dans Pinokio custom_nodes)
- [ ] Configurer le bot Telegram
- [ ] Exporter 3-5 workflows cles avec TG-ImageSaver
- [ ] Installer MCWW via ComfyUI Manager
- [ ] Taguer les noeuds editables
- [ ] Installer Comfy Portal sur iPhone

### Etape 5 : Notifications
- [ ] Integrer notify.sh dans les commandes Claude
- [ ] Installer Comfyui-TelegramSender sur le PC
- [ ] Configurer le channel Telegram dedie

### Etape 6 (future) : NLE Bridge
- [ ] Creer le dossier `~/ComfyUI-Exchange/` sur le Mac
- [ ] Script de surveillance + lancement workflow
- [ ] Installer MCP DaVinci Resolve
- [ ] Tester le round-trip Resolve → ComfyUI → Resolve

---

## Edge cases et gestion d'erreurs

| Situation | Comportement |
|---|---|
| PC Windows eteint | Claude detecte (timeout HTTP), propose de lancer via Comfy Cloud |
| Workflow echoue (noeud manquant) | Claude lit l'erreur, identifie le custom node manquant, recommande l'installation |
| Workflow echoue (VRAM insuffisante) | Claude propose de basculer sur Comfy Cloud ou de reduire la resolution |
| Modele non installe | Claude identifie le modele requis, donne les instructions d'installation |
| Tailscale deconnecte | Claude detecte (timeout), rappelle de verifier Tailscale sur les deux machines |
| Generation trop longue (>10 min) | Claude notifie "en cours" puis notifie a la fin |
| Comfy Cloud credits epuises | Claude detecte (erreur API), previent et propose le local |

---

## Securite

- **Tailscale** : Reseau mesh chiffre WireGuard. ComfyUI n'est PAS expose sur internet.
- **API key Comfy Cloud** : Stockee dans variable d'environnement, pas dans le code.
- **Pas d'auth ComfyUI** : ComfyUI n'a pas d'auth native. La securite repose sur Tailscale (seuls les appareils du mesh peuvent acceder au port 8188).

---

## Limites connues

1. **FCP n'a pas d'API** : Le round-trip sera toujours semi-manuel (export/import fichier).
2. **ComfyUI-TG ne supporte pas la video en output** : Seulement les images. Les videos devront etre recuperees via le navigateur ou Comfy Portal.
3. **Comfy Cloud $20/mois = ~4h23 GPU/mois** : Suffisant pour des generations ponctuelles, pas pour du batch lourd.
4. **ComfyScript ne couvre pas tous les custom nodes** : Certains noeuds exotiques devront etre pilotes en JSON.
5. **Pinokio path** : Le chemin d'installation Pinokio par defaut sur Windows est `C:\Users\<user>\pinokio\api\comfyui.git\app`. A verifier.
