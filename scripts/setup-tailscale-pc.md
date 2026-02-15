# Installer Tailscale sur le PC Windows (RTX 5090)

## Etape 1 : Installer Tailscale

1. Ouvrir un navigateur sur le PC Windows
2. Aller sur https://tailscale.com/download/windows
3. Telecharger et installer
4. Se connecter avec le **meme compte** que sur le Mac (Google, GitHub, etc.)

## Etape 2 : Noter l'IP Tailscale du PC

1. Clic droit sur l'icone Tailscale dans la barre des taches (en bas a droite)
2. Cliquer sur "My devices" ou ouvrir https://login.tailscale.com/admin/machines
3. Trouver le PC Windows dans la liste
4. Noter son IP (format `100.x.y.z`)

## Etape 3 : Ouvrir ComfyUI au reseau

ComfyUI dans Pinokio doit accepter les connexions externes.

### Option A : Via les settings Pinokio
1. Ouvrir Pinokio
2. Aller dans les parametres de ComfyUI
3. Ajouter `--listen 0.0.0.0` aux arguments de lancement
4. Relancer ComfyUI

### Option B : Editer le script de demarrage
1. Trouver le dossier Pinokio (par defaut `C:\Users\<nom>\pinokio\`)
2. Chercher le fichier de config/lancement de ComfyUI
3. Ajouter `--listen 0.0.0.0` aux arguments `main.py`
4. Relancer ComfyUI

## Etape 4 : Tester depuis le Mac

Ouvrir un terminal sur le Mac et taper :

```bash
# Remplacer 100.x.y.z par l'IP Tailscale du PC
curl http://100.x.y.z:8188/system_stats
```

Si ca retourne du JSON avec les infos GPU, c'est bon.

## Etape 5 : Tester depuis l'iPhone

1. Installer Tailscale sur l'iPhone (App Store)
2. Se connecter avec le meme compte
3. Ouvrir Safari : `http://100.x.y.z:8188`
4. L'interface ComfyUI doit s'afficher

## Etape 6 : Mettre a jour la config

Une fois l'IP connue, mettre a jour :
- `.mcp.json` dans le repo (remplacer `TAILSCALE_IP_PC`)
- `scripts/test-connection.sh` (remplacer `TAILSCALE_IP_PC`)
