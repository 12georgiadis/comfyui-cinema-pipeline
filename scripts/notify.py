#!/usr/bin/env python3
"""Notification helper for the cinema pipeline.

Sends notifications via Telegram and/or local system notification.
Used by the MCP server and Claude Code commands to signal completion.

Usage:
    # As module
    from notify import send_notification
    send_notification("Generation complete", image_path="/path/to/preview.png")

    # As CLI
    python notify.py "Your video is ready"
    python notify.py "Upscale complete" --image /path/to/result.png
"""

import os
import subprocess
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


def load_env():
    """Load .env file from project root."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                value = value.strip().strip("'\"")
                if key.strip() not in os.environ:
                    os.environ[key.strip()] = value


def send_telegram(message: str, image_path: str = None) -> bool:
    """Send notification via Telegram bot.

    Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env or environment.
    """
    if not requests:
        return False

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id or token == "your_bot_token_here":
        return False

    base_url = f"https://api.telegram.org/bot{token}"

    try:
        if image_path and Path(image_path).exists():
            # Send photo with caption
            with open(image_path, "rb") as photo:
                resp = requests.post(
                    f"{base_url}/sendPhoto",
                    data={"chat_id": chat_id, "caption": message},
                    files={"photo": photo},
                    timeout=30,
                )
        else:
            # Send text message
            resp = requests.post(
                f"{base_url}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                },
                timeout=15,
            )

        return resp.status_code == 200
    except Exception:
        return False


def send_system_notification(message: str) -> bool:
    """Send macOS system notification + Zelda sound via notify.sh."""
    notify_script = Path.home() / ".claude" / "scripts" / "notify.sh"
    if notify_script.exists():
        try:
            subprocess.run(
                [str(notify_script), message],
                timeout=10,
                capture_output=True,
            )
            return True
        except Exception:
            pass

    # Fallback: osascript notification
    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display notification "{message}" with title "ComfyUI Cinema"',
            ],
            timeout=5,
            capture_output=True,
        )
        return True
    except Exception:
        return False


def send_notification(
    message: str,
    image_path: str = None,
    telegram: bool = True,
    system: bool = True,
) -> dict:
    """Send notification via all configured channels.

    Args:
        message: Notification text
        image_path: Optional path to image/preview to attach
        telegram: Whether to try Telegram
        system: Whether to try system notification

    Returns:
        dict with status of each channel
    """
    load_env()
    results = {}

    if telegram:
        results["telegram"] = send_telegram(message, image_path)

    if system:
        results["system"] = send_system_notification(message)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Send notification")
    parser.add_argument("message", help="Notification message")
    parser.add_argument("--image", help="Path to image to attach", default=None)
    parser.add_argument("--no-telegram", action="store_true", help="Skip Telegram")
    parser.add_argument("--no-system", action="store_true", help="Skip system notification")
    args = parser.parse_args()

    results = send_notification(
        args.message,
        image_path=args.image,
        telegram=not args.no_telegram,
        system=not args.no_system,
    )

    for channel, success in results.items():
        status = "OK" if success else "SKIPPED"
        print(f"  {channel}: {status}")
