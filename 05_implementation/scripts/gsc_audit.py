"""Pull real Google Search Console data for johnson-services.de.

Uses GOOGLE_OAUTH_CLIENT_ID/SECRET + GOOGLE_GROWTH_REFRESH_TOKEN to mint an
access token (no extra deps; raw OAuth token exchange), then queries the
Search Console Search Analytics API.

Gracefully degrades: if credentials are not yet set, prints a clear PENDING
message instead of failing or fabricating data (Constitution: no fake results).

Usage:
    python3 gsc_audit.py            # last 28 days, top queries + pages
"""
from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

from env_loader import load_env
import os

TOKEN_URL = "https://oauth2.googleapis.com/token"


def _access_token() -> str | None:
    load_env()
    cid = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "")
    secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "")
    refresh = os.environ.get("GOOGLE_GROWTH_REFRESH_TOKEN", "")
    if not (cid and secret and refresh):
        return None
    data = urllib.parse.urlencode({
        "client_id": cid, "client_secret": secret,
        "refresh_token": refresh, "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen(TOKEN_URL, data=data, timeout=20) as r:
        return json.load(r).get("access_token")


def query(token: str, prop: str, dimension: str, days: int = 28, limit: int = 25) -> list:
    end = date.today()
    start = end - timedelta(days=days)
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(prop, safe='')}/searchAnalytics/query"
    body = json.dumps({
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions": [dimension], "rowLimit": limit,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("rows", [])


def list_sites(token: str) -> list:
    req = urllib.request.Request(
        "https://www.googleapis.com/webmasters/v3/sites",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r).get("siteEntry", [])


def main() -> int:
    token = _access_token()
    if not token:
        print("PENDING — Google OAuth not yet complete.")
        print("Set GOOGLE_OAUTH_CLIENT_SECRET + GOOGLE_GROWTH_REFRESH_TOKEN in .env")
        print("(run google_oauth_growth.py first). No data fetched, nothing fabricated.")
        return 0
    try:
        sites = list_sites(token)
    except urllib.error.HTTPError as e:
        print(f"sites.list Fehler {e.code}: {e.read().decode()[:200]}")
        return 0
    if not sites:
        print("Keine GSC-Property für dieses Konto. johnson-services.de muss in der")
        print("Search Console dieses Kontos verifiziert oder als Nutzer freigegeben sein.")
        return 0
    urls = [s.get("siteUrl") for s in sites]
    env_prop = os.environ.get("GSC_PROPERTY", "")
    prop = env_prop if env_prop in urls else next((u for u in urls if "johnson-services.de" in (u or "")), urls[0])
    print(f"Property: {prop}  (verfügbar: {', '.join(urls)})")
    for dim in ("query", "page"):
        print(f"\n=== Top {dim}s (28d) — {prop} ===")
        try:
            rows = query(token, prop, dim)
        except urllib.error.HTTPError as e:
            print(f"  API error {e.code}: {e.read().decode()[:160]}")
            continue
        if not rows:
            print("  (no rows — property may be new or not verified)")
        for row in rows:
            k = row.get("keys", ["?"])[0]
            print(f"  pos {row.get('position', 0):5.1f} | clicks {int(row.get('clicks', 0)):4d} "
                  f"| impr {int(row.get('impressions', 0)):6d} | ctr {row.get('ctr', 0) * 100:4.1f}% | {k[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
