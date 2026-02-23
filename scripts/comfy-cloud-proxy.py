#!/usr/bin/env python3
"""Comfy Cloud API proxy helper.

Translates local ComfyUI API calls to Comfy Cloud API format.
Comfy Cloud uses the same workflow JSON format but different endpoints and auth.

Usage:
    # As a module
    from comfy_cloud_proxy import ComfyCloudClient
    client = ComfyCloudClient(api_key="your-key")
    result = client.queue_prompt(workflow_json)

    # As a standalone test
    python comfy-cloud-proxy.py
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests required. pip install requests")
    sys.exit(1)

# Comfy Cloud API endpoints
COMFY_CLOUD_API_URL = "https://api.comfy.org/api"
COMFY_CLOUD_RUN_URL = f"{COMFY_CLOUD_API_URL}/run"


class ComfyCloudClient:
    """Client for Comfy Cloud API.

    The Comfy Cloud API is compatible with the local ComfyUI API
    but requires an API key and uses different endpoints.

    Docs: https://docs.comfy.org/comfy-cloud/overview
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("COMFY_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Comfy Cloud API key required. "
                "Set COMFY_CLOUD_API_KEY env var or pass api_key parameter."
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def queue_prompt(self, workflow: dict, webhook_url: str = None) -> dict:
        """Submit a workflow to Comfy Cloud.

        Args:
            workflow: ComfyUI API format workflow JSON
            webhook_url: Optional webhook URL for completion notification

        Returns:
            dict with run_id and status
        """
        payload = {
            "prompt": workflow,
        }
        if webhook_url:
            payload["webhook"] = webhook_url

        resp = self.session.post(COMFY_CLOUD_RUN_URL, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_run_status(self, run_id: str) -> dict:
        """Check the status of a cloud run.

        Args:
            run_id: The run ID from queue_prompt response

        Returns:
            dict with status and outputs (if complete)
        """
        resp = self.session.get(f"{COMFY_CLOUD_RUN_URL}/{run_id}", timeout=15)
        resp.raise_for_status()
        return resp.json()

    def wait_for_completion(self, run_id: str, timeout: int = 600, poll_interval: int = 5) -> dict:
        """Wait for a cloud run to complete.

        Args:
            run_id: The run ID
            timeout: Max wait time in seconds (default 10 min)
            poll_interval: Seconds between status checks

        Returns:
            dict with final status and outputs
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_run_status(run_id)
            state = status.get("status", "unknown")

            if state in ("completed", "success"):
                return status
            elif state in ("failed", "error", "cancelled"):
                raise RuntimeError(f"Cloud run {run_id} failed: {status}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Cloud run {run_id} timed out after {timeout}s")

    def list_runs(self, limit: int = 10) -> list:
        """List recent cloud runs.

        Args:
            limit: Max number of runs to return

        Returns:
            list of recent run summaries
        """
        resp = self.session.get(
            COMFY_CLOUD_RUN_URL,
            params={"limit": limit},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()


def test_connection():
    """Test Comfy Cloud API connection."""
    api_key = os.getenv("COMFY_CLOUD_API_KEY")
    if not api_key:
        # Try loading from .env
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("COMFY_CLOUD_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip("'\"")
                    break

    if not api_key or api_key == "your_api_key_here":
        print("ERROR: No valid Comfy Cloud API key found.")
        print("Set COMFY_CLOUD_API_KEY in your .env file or environment.")
        print("Get your key at: https://platform.comfy.org/profile/api-keys")
        return False

    print("Testing Comfy Cloud connection...")
    try:
        client = ComfyCloudClient(api_key=api_key)
        runs = client.list_runs(limit=1)
        print("[+] Comfy Cloud connection successful!")
        print(f"    Recent runs: {len(runs)} found")
        return True
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            print("[X] Invalid API key. Check your COMFY_CLOUD_API_KEY.")
        elif e.response.status_code == 403:
            print("[X] API key doesn't have required permissions.")
        else:
            print(f"[X] HTTP error: {e}")
        return False
    except Exception as e:
        print(f"[X] Connection failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("  Comfy Cloud API - Connection Test")
    print("=" * 50)
    print()
    test_connection()
