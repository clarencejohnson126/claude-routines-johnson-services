"""Tiny Telegram notifier for the Growth Engine recurring jobs.

Reads TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID from .env. No secrets printed.
"""
from __future__ import annotations

import os
import urllib.parse
import urllib.request

from env_loader import load_env


def send(msg: str) -> bool:
    load_env()
    tok = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not (tok and chat):
        return False
    data = urllib.parse.urlencode({"chat_id": chat, "text": msg[:4000], "disable_web_page_preview": "true"}).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data=data, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


if __name__ == "__main__":
    import sys
    ok = send(sys.argv[1] if len(sys.argv) > 1 else "Growth Engine notify test")
    print("sent" if ok else "failed (Telegram vars?)")
