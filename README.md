# ComfyUI Cinema Pipeline

Research & architecture for using ComfyUI as a professional cinema production tool, orchestrated by Claude Code (LLM CLI agent).

**Target**: auteur cinema (feature films, post-documentary, experimental). Not hobbyist image generation.

**Hardware**: RTX 5090 (32GB local) + Comfy Cloud (96GB RTX 6000 Pro) + Mac for editing.

---

## Why this repo exists

No one has compiled a comprehensive, honest assessment of the ComfyUI ecosystem from a **filmmaker's perspective**. Most resources are for hobbyist image generation. This repo documents:

1. Every relevant ComfyUI workflow for cinema production
2. How to connect Claude Code (LLM) to ComfyUI via MCP
3. How to integrate ComfyUI with professional NLEs (DaVinci Resolve, Premiere, FCP)
4. Simplified frontends for mobile/remote access
5. Hybrid local/cloud GPU orchestration

All links are real. All stability ratings are honest. No hype.

---

## Architecture

```
                    ┌─────────────────┐
                    │   Claude Code   │  ← Brain / orchestrator
                    │   (MCP Server)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───────┐ ┌───▼────┐ ┌───────▼───────┐
     │  ComfyUI Local │ │ Comfy  │ │ DaVinci       │
     │  RTX 5090 32GB │ │ Cloud  │ │ Resolve       │
     │  (Windows)     │ │ 96GB   │ │ (MCP + API)   │
     └────────┬───────┘ └───┬────┘ └───────────────┘
              │              │
     ┌────────▼──────────────▼────────┐
     │       Access Interfaces        │
     ├────────────────────────────────┤
     │ SwarmUI/MCWW   (browser)       │
     │ ComfyUI-TG     (Telegram)      │
     │ Comfy Portal   (iOS app)       │
     │ Pocket-Comfy   (PWA mobile)    │
     └────────────────────────────────┘
              │
     ┌────────▼────────┐
     │  Tailscale VPN  │
     │  (mesh network) │
     └─────────────────┘
```

---

## Documentation

| Document | Description |
|---|---|
| [Claude Code + ComfyUI Integration](docs/01-claude-code-integration.md) | MCP servers, API, ComfyScript, LLM-driven workflows |
| [Cinema Workflows Catalog](docs/02-cinema-workflows.md) | 70+ workflows organized by category (video gen, VFX, style transfer, etc.) |
| [Simplified Frontends](docs/03-simplified-frontends.md) | Krea-like interfaces, mobile-first UIs, SwarmUI |
| [Mobile & Remote Access](docs/04-mobile-remote-access.md) | Tailscale setup, iOS apps, Telegram bots, PWA |
| [NLE Integration](docs/05-nle-integration.md) | DaVinci Resolve, Premiere Pro, FCP, Blender, After Effects |
| [Hybrid Local/Cloud](docs/06-hybrid-local-cloud.md) | RTX 5090 + Comfy Cloud + RunComfy + ComfyUI-Distributed |
| [Open Creative Studio (OCS)](docs/07-ocs-perilli.md) | Alessandro Perilli's all-in-one ComfyUI system |
| [Hardware Guide](docs/08-hardware.md) | VRAM requirements, GPU benchmarks, optimization |

---

## Key findings (TL;DR)

### What works now
- ComfyUI + MCP servers = Claude Code can generate images/video programmatically
- Wan 2.1/2.2 video generation is production-quality for specific use cases
- SAM 3 rotoscoping replaces hours of manual work
- StyleTransferPlus + EbSynth = temporal-consistent artistic looks
- Mobile access via Tailscale + Telegram bot or PWA

### What doesn't work yet
- No NLE has native ComfyUI integration (DaVinci Resolve is closest via API)
- No "CapCut but pro" exists -- the workflow is still export/process/reimport
- ComfyUI-BlenderAI-node has 90% installation failure rate
- Final Cut Pro is a dead end (Apple walled garden)
- Comfy Cloud and local ComfyUI don't have transparent switching

### What we're building
- MCP server configured for cinema workflows
- DaVinci Resolve <-> ComfyUI bridge (Python API)
- Mobile-first frontend for on-set/remote use
- This repo as a living reference

---

## Stability ratings

| Tool | Score | Notes |
|---|---|---|
| ComfyUI core | 9/10 | Rock solid |
| Wan 2.1/2.2 workflows | 8/10 | Dominant video ecosystem |
| ComfyUI MCP servers | 6/10 | Multiple options, some rough edges |
| DaVinci Resolve MCP | 5/10 | Functional, needs custom dev |
| SwarmUI | 7/10 | Good compromise simplicity/power |
| MCWW (mobile UI) | 7/10 | Auto-adapts to any workflow |
| Comfy Cloud | 7/10 | Works but expensive for heavy use |
| Blender Pallaidium | 5/10 | Windows only, fragile |
| FCP + ComfyUI | 0/10 | Does not exist |

---

## Contributing

This is a living document. If you're a filmmaker working with ComfyUI, PRs are welcome. Focus on:
- Real-world production experience (not just "it generates cool images")
- Honest stability assessments
- New NLE integration approaches
- Mobile/remote workflow improvements

---

## Credits

Research compiled by [Ismael Joffroy Chandoutis](https://ismaeljoffroychandoutis.com/) with Claude Code (Anthropic).

February 2025. Updated regularly.

---

## License

MIT
