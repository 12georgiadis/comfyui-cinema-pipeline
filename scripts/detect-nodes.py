#!/usr/bin/env python3
"""Detect installed ComfyUI nodes and check workflow compatibility.

Usage:
    python detect-nodes.py [COMFYUI_URL]
    python detect-nodes.py http://100.x.y.z:8188

Queries ComfyUI's /object_info endpoint to list all available nodes,
then checks which cinema workflow templates are compatible.
"""

import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

# Default ComfyUI URL
COMFYUI_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8188"
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"


def get_available_nodes(base_url: str) -> dict:
    """Fetch all available nodes from ComfyUI."""
    print(f"Connecting to ComfyUI at {base_url}...")
    try:
        resp = requests.get(f"{base_url}/object_info", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.ConnectionError:
        print(f"ERROR: Cannot connect to ComfyUI at {base_url}")
        print("Make sure ComfyUI is running and accessible.")
        sys.exit(1)
    except requests.Timeout:
        print(f"ERROR: Timeout connecting to {base_url}")
        sys.exit(1)


def get_available_models(base_url: str) -> dict:
    """Fetch available models from ComfyUI."""
    models = {}
    # Check checkpoints
    try:
        resp = requests.get(f"{base_url}/object_info/CheckpointLoaderSimple", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            ckpt_info = data.get("CheckpointLoaderSimple", {}).get("input", {}).get("required", {})
            if "ckpt_name" in ckpt_info:
                models["checkpoints"] = ckpt_info["ckpt_name"][0]
    except Exception:
        pass

    # Check UNET models
    try:
        resp = requests.get(f"{base_url}/object_info/UNETLoader", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            unet_info = data.get("UNETLoader", {}).get("input", {}).get("required", {})
            if "unet_name" in unet_info:
                models["unet"] = unet_info["unet_name"][0]
    except Exception:
        pass

    # Check upscale models
    try:
        resp = requests.get(f"{base_url}/object_info/UpscaleModelLoader", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            up_info = data.get("UpscaleModelLoader", {}).get("input", {}).get("required", {})
            if "model_name" in up_info:
                models["upscale"] = up_info["model_name"][0]
    except Exception:
        pass

    # Check VAE models
    try:
        resp = requests.get(f"{base_url}/object_info/VAELoader", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            vae_info = data.get("VAELoader", {}).get("input", {}).get("required", {})
            if "vae_name" in vae_info:
                models["vae"] = vae_info["vae_name"][0]
    except Exception:
        pass

    # Check CLIP models
    try:
        resp = requests.get(f"{base_url}/object_info/CLIPLoader", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            clip_info = data.get("CLIPLoader", {}).get("input", {}).get("required", {})
            if "clip_name" in clip_info:
                models["clip"] = clip_info["clip_name"][0]
    except Exception:
        pass

    return models


def check_workflow_compatibility(nodes: dict, workflow_path: Path) -> dict:
    """Check if a workflow's required nodes are available."""
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Extract class_type from workflow nodes
    required_classes = set()
    for node in workflow.values():
        if isinstance(node, dict) and "class_type" in node:
            required_classes.add(node["class_type"])

    # Check availability
    available = set()
    missing = set()
    for cls in required_classes:
        if cls in nodes:
            available.add(cls)
        else:
            missing.add(cls)

    # Load metadata if exists
    meta_path = workflow_path.with_suffix(".meta.json")
    metadata = {}
    if meta_path.exists():
        with open(meta_path) as f:
            metadata = json.load(f)

    return {
        "name": metadata.get("name", workflow_path.stem),
        "description": metadata.get("description", ""),
        "required": required_classes,
        "available": available,
        "missing": missing,
        "compatible": len(missing) == 0,
        "vram_gb": metadata.get("vram_estimate_gb", "?"),
        "custom_nodes_needed": metadata.get("required_custom_nodes", []),
    }


def main():
    print("=" * 70)
    print("  ComfyUI Cinema Pipeline - Node Detection")
    print("=" * 70)
    print()

    # Get all nodes
    nodes = get_available_nodes(COMFYUI_URL)
    total_nodes = len(nodes)
    print(f"Found {total_nodes} nodes available in ComfyUI")
    print()

    # Get available models
    print("Scanning available models...")
    models = get_available_models(COMFYUI_URL)
    for category, model_list in models.items():
        if isinstance(model_list, list):
            print(f"  {category}: {len(model_list)} models")
            for m in model_list[:5]:
                print(f"    - {m}")
            if len(model_list) > 5:
                print(f"    ... and {len(model_list) - 5} more")
        else:
            print(f"  {category}: {model_list}")
    print()

    # Check cinema workflows
    print("=" * 70)
    print("  Workflow Compatibility Check")
    print("=" * 70)
    print()

    if not WORKFLOWS_DIR.exists():
        print(f"Workflows directory not found: {WORKFLOWS_DIR}")
        return

    compatible_count = 0
    total_count = 0

    for wf_path in sorted(WORKFLOWS_DIR.glob("*.json")):
        if wf_path.name.endswith(".meta.json"):
            continue
        total_count += 1
        result = check_workflow_compatibility(nodes, wf_path)

        status = "OK" if result["compatible"] else "MISSING NODES"
        icon = "[+]" if result["compatible"] else "[!]"

        print(f"{icon} {result['name']} ({wf_path.stem})")
        print(f"    Status: {status} | VRAM: ~{result['vram_gb']}GB")

        if result["compatible"]:
            compatible_count += 1
            print(f"    All {len(result['required'])} required nodes available")
        else:
            print(f"    Missing {len(result['missing'])} node(s):")
            for m in sorted(result["missing"]):
                print(f"      - {m}")
            if result["custom_nodes_needed"]:
                print(f"    Install these custom node packs:")
                for cn in result["custom_nodes_needed"]:
                    print(f"      - {cn}")
        print()

    print("=" * 70)
    print(f"  Summary: {compatible_count}/{total_count} workflows ready")
    print("=" * 70)

    # Cinema-relevant node detection
    print()
    print("=" * 70)
    print("  Cinema-Relevant Nodes Detected")
    print("=" * 70)
    print()

    cinema_categories = {
        "Video Generation": ["WanModel", "CogVideo", "AnimateDiff", "SVD", "Mochi", "HunyuanVideo"],
        "Video Processing": ["VHS_", "VideoHelper", "RIFE", "FilmGrain", "Deflicker"],
        "Upscaling": ["Upscale", "ESRGAN", "RealESR", "SwinIR", "HAT"],
        "Segmentation": ["SAM", "GroundingDINO", "Segment", "Mask"],
        "Depth": ["Depth", "MiDaS", "ZoeDepth"],
        "ControlNet": ["ControlNet", "T2IAdapter", "IPAdapter"],
        "Face": ["Face", "InsightFace", "ReActor", "IPAdapter"],
        "Style": ["Style", "NST", "EbSynth"],
        "Audio": ["Audio", "AceStep", "Sound"],
        "3D": ["3D", "TripoSR", "Mesh", "Point Cloud"],
    }

    for category, keywords in cinema_categories.items():
        matching = []
        for node_name in nodes:
            for kw in keywords:
                if kw.lower() in node_name.lower():
                    matching.append(node_name)
                    break
        if matching:
            print(f"  {category}: {len(matching)} nodes")
            for n in sorted(matching)[:8]:
                print(f"    - {n}")
            if len(matching) > 8:
                print(f"    ... and {len(matching) - 8} more")
        else:
            print(f"  {category}: none detected")
        print()

    # Save full report
    report = {
        "comfyui_url": COMFYUI_URL,
        "total_nodes": total_nodes,
        "models": {k: v if isinstance(v, list) else [v] for k, v in models.items()},
        "workflows_compatible": compatible_count,
        "workflows_total": total_count,
    }
    report_path = Path(__file__).parent.parent / "node-report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Full report saved to: {report_path}")


if __name__ == "__main__":
    main()
