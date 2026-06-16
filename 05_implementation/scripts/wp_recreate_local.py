"""Recreate Heidelberg + Mannheim as CLASSIC posts so they render (Elementor
ignored post_content on the old empty posts). Approved 2026-06-15.

Deletes the empty Elementor posts (force) and creates classic posts with the
SAME slug + category -> same URL, GSC equity preserved. Content rendered via
post_content (verified working for Ludwigshafen/Keller/Reinigung).
"""
from __future__ import annotations

import sys
import urllib.error

from wp_client import get
from wp_publish import HEIDELBERG_HTML, MANNHEIM_HTML, META, _req, check_token

TARGETS = [
    ("heidelberg", "Entrümpelung Heidelberg zum Festpreis", HEIDELBERG_HTML, META["heidelberg"]),
    ("mannheim", "Entrümpelung Mannheim zum Festpreis", MANNHEIM_HTML, META["mannheim"]),
]


def main() -> int:
    try:
        me = check_token()
    except urllib.error.HTTPError as e:
        print(f"AUTH FEHLER {e.code}: {e.read().decode()[:140]}")
        return 1
    print(f"✅ Auth OK: {me.get('name')}")
    cat = get("/categories", slug="entruempelung", _fields="id")[0]["id"]

    for slug, title, html, meta in TARGETS:
        old = get("/posts", slug=slug, status="publish,draft,pending,future,private", _fields="id")
        if old:
            oid = old[0]["id"]
            _req("DELETE", f"/posts/{oid}?force=true")
            print(f"  alt geloescht: post {oid} (slug {slug})")
        r = _req("POST", "/posts", {
            "title": title, "slug": slug, "content": html, "excerpt": meta,
            "status": "publish", "categories": [cat],
        })
        print(f"  neu erstellt: {slug} -> id {r.get('id')}  {r.get('link')}  status={r.get('status')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
