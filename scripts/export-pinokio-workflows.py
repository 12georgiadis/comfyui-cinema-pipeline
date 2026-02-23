#!/usr/bin/env python3
"""
Export ComfyUI workflows from Pinokio to API format.

This script:
1. Finds ComfyUI workflow files in the Pinokio directory
2. Converts them from UI format to API format (if needed)
3. Copies them to the workflows/ directory with MCP-compatible placeholders

Usage:
    python export-pinokio-workflows.py [COMFYUI_URL] [OUTPUT_DIR]

Default:
    COMFYUI_URL = http://127.0.0.1:8188
    OUTPUT_DIR = ./workflows/
"""

import json
import sys
import os
import shutil
from pathlib import Path

# Default Pinokio ComfyUI paths on Windows
PINOKIO_PATHS = [
    Path.home() / "pinokio" / "api" / "comfyui.git" / "app",
    Path.home() / "pinokio" / "api" / "comfyui.default" / "app",
    Path.home() / "pinokio" / "api" / "comfyui",
]

# Common workflow locations within ComfyUI
WORKFLOW_SUBDIRS = [
    "user" / Path("default") / "workflows",
    "custom_nodes",
    Path("output"),
    Path("input"),
]


def find_comfyui_dir():
    """Find the ComfyUI installation directory."""
    for path in PINOKIO_PATHS:
        if path.exists():
            print(f"Found ComfyUI at: {path}")
            return path
    print("ERROR: Could not find ComfyUI in Pinokio.")
    print("Searched:")
    for p in PINOKIO_PATHS:
        print(f"  {p}")
    print("\nPlease provide the path manually or check your Pinokio installation.")
    return None


def find_workflow_files(comfyui_dir):
    """Find all .json workflow files."""
    workflows = []
    for subdir in WORKFLOW_SUBDIRS:
        search_dir = comfyui_dir / subdir
        if search_dir.exists():
            for f in search_dir.rglob("*.json"):
                # Skip non-workflow JSON files
                if f.name.startswith(".") or "node_modules" in str(f):
                    continue
                try:
                    with open(f, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                    # Check if it looks like a ComfyUI workflow
                    if isinstance(data, dict) and (
                        "nodes" in data  # UI format
                        or any(
                            isinstance(v, dict) and "class_type" in v
                            for v in data.values()
                        )  # API format
                    ):
                        workflows.append(f)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
    return workflows


def is_api_format(data):
    """Check if workflow is already in API format."""
    if not isinstance(data, dict):
        return False
    # API format: keys are node IDs (strings of numbers), values have 'class_type'
    for key, value in data.items():
        if isinstance(value, dict) and "class_type" in value:
            return True
    return False


def add_placeholders(data):
    """Add MCP-compatible placeholders to known node types."""
    for node_id, node in data.items():
        if not isinstance(node, dict):
            continue
        class_type = node.get("class_type", "")
        inputs = node.get("inputs", {})

        # Text prompts
        if class_type in ("CLIPTextEncode", "CLIPTextEncodeFlux"):
            if "text" in inputs and isinstance(inputs["text"], str):
                if "negative" not in inputs.get("_meta", {}).get("title", "").lower():
                    inputs["text"] = "PARAM_PROMPT"

        # KSampler parameters
        if "KSampler" in class_type:
            if "steps" in inputs:
                inputs["steps"] = "PARAM_INT_STEPS"
            if "cfg" in inputs:
                inputs["cfg"] = "PARAM_FLOAT_CFG"
            if "seed" in inputs:
                inputs["seed"] = "PARAM_INT_SEED"

        # Image dimensions
        if class_type in ("EmptyLatentImage", "EmptySD3LatentImage"):
            if "width" in inputs:
                inputs["width"] = "PARAM_INT_WIDTH"
            if "height" in inputs:
                inputs["height"] = "PARAM_INT_HEIGHT"

    return data


def main():
    comfyui_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8188"
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./workflows")

    output_dir.mkdir(parents=True, exist_ok=True)

    comfyui_dir = find_comfyui_dir()
    if not comfyui_dir:
        print("\nAlternative: export workflows manually from ComfyUI:")
        print("  1. Open ComfyUI in your browser")
        print("  2. Load the workflow")
        print("  3. Enable Dev Mode in Settings")
        print("  4. Click 'Save (API Format)'")
        print(f"  5. Save to {output_dir}/")
        sys.exit(1)

    workflows = find_workflow_files(comfyui_dir)
    print(f"\nFound {len(workflows)} workflow files:")

    for wf in workflows:
        rel_path = wf.relative_to(comfyui_dir)
        print(f"  {rel_path}")

    if not workflows:
        print("No workflows found. Export them manually from ComfyUI.")
        sys.exit(0)

    print(f"\nExporting to {output_dir}/...")
    exported = 0
    for wf in workflows:
        try:
            with open(wf, "r", encoding="utf-8") as f:
                data = json.load(f)

            if is_api_format(data):
                # Already API format, add placeholders
                data = add_placeholders(data)
                out_name = wf.stem + ".json"
                out_path = output_dir / out_name
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"  Exported (API): {out_name}")
                exported += 1
            else:
                # UI format - need to convert via ComfyUI API
                # For now, just copy and flag for manual conversion
                out_name = wf.stem + "_ui.json"
                out_path = output_dir / out_name
                shutil.copy2(wf, out_path)
                print(f"  Copied (UI format, needs conversion): {out_name}")
                exported += 1

        except Exception as e:
            print(f"  SKIP {wf.name}: {e}")

    print(f"\n{exported} workflows exported to {output_dir}/")
    print("\nUI-format workflows need manual conversion:")
    print("  1. Open ComfyUI, load the workflow")
    print("  2. Settings > Enable Dev Mode")
    print("  3. Click 'Save (API Format)'")
    print(f"  4. Save to {output_dir}/ replacing the _ui.json file")


if __name__ == "__main__":
    main()
