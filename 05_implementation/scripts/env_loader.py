"""Minimal .env loader for the Growth Engine. No external deps.

Reads the project .env (chmod 600, gitignored) into os.environ without
overwriting already-set vars. NEVER prints values.
"""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"


def load_env(path: Path = ENV_PATH) -> int:
    """Load KEY=VALUE lines from .env. Returns count of keys loaded."""
    if not path.exists():
        return 0
    n = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val
            n += 1
    return n


def require(*keys: str) -> dict[str, str]:
    """Return the requested env vars; raise if any is missing/empty. Values not printed."""
    load_env()
    out, missing = {}, []
    for k in keys:
        v = os.environ.get(k, "")
        if not v:
            missing.append(k)
        else:
            out[k] = v
    if missing:
        raise SystemExit(f"Missing/empty env vars: {', '.join(missing)} (set them in .env)")
    return out


if __name__ == "__main__":
    count = load_env()
    print(f"Loaded {count} env keys from {ENV_PATH} (values hidden).")
