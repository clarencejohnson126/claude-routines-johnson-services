"""Read-only WordPress REST client for johnson-services.de.

Pattern mirrors ../Graph-Growth-Agents/automation/johnson_autoblog/autoblog.py
(Basic-Auth via Application Password). This client is READ-ONLY by design:
it only issues GET requests. No create/update/delete. Publishing stays a
human approval gate (see 00_constitution/security_and_credentials.md).

Usage:
    python3 wp_client.py audit > ../../07_outputs/seo_reports/_wp_audit_raw.json
"""
from __future__ import annotations

import base64
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from env_loader import require

API = "/wp-json/wp/v2"
TIMEOUT = 30


def _auth_header() -> dict[str, str]:
    creds = require("WORDPRESS_USER", "WORDPRESS_APP_PASSWORD")
    raw = f"{creds['WORDPRESS_USER']}:{creds['WORDPRESS_APP_PASSWORD']}".encode()
    return {"Authorization": "Basic " + base64.b64encode(raw).decode()}


def _base() -> str:
    return require("WORDPRESS_SITE_URL")["WORDPRESS_SITE_URL"].rstrip("/")


def get(path: str, **params) -> list | dict:
    url = _base() + API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={**_auth_header(), "User-Agent": "JS-GrowthEngine/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode())


def list_all(path: str, **params) -> list:
    """Paginate a collection endpoint (posts/pages)."""
    out, page = [], 1
    params.setdefault("per_page", 50)
    while True:
        try:
            batch = get(path, page=page, **params)
        except urllib.error.HTTPError as e:
            if e.code == 400:  # past last page
                break
            raise
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < params["per_page"]:
            break
        page += 1
    return out


def audit() -> dict:
    """Crawl real public structure: pages, posts, categories. Returns JSON-able dict."""
    fields = "id,slug,link,title,excerpt,status,date,modified,parent,categories"
    pages = list_all("/pages", _fields=fields, status="publish")
    posts = list_all("/posts", _fields=fields, status="publish")
    cats = get("/categories", per_page=100, _fields="id,name,slug,count")

    def slim(items):
        return [
            {
                "id": it.get("id"),
                "slug": it.get("slug"),
                "link": it.get("link"),
                "title": (it.get("title") or {}).get("rendered", "").strip(),
                "has_excerpt": bool((it.get("excerpt") or {}).get("rendered", "").strip()),
                "modified": it.get("modified"),
            }
            for it in items
        ]

    return {
        "source": _base(),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "counts": {"pages": len(pages), "posts": len(posts), "categories": len(cats)},
        "pages": slim(pages),
        "posts": slim(posts),
        "categories": [
            {"id": c.get("id"), "name": c.get("name"), "slug": c.get("slug"), "count": c.get("count")}
            for c in (cats if isinstance(cats, list) else [])
        ],
    }


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "audit"
    if cmd == "audit":
        print(json.dumps(audit(), ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {cmd}. Use: audit", file=sys.stderr)
        sys.exit(1)
