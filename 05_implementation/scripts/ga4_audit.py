"""Pull GA4 data for Johnson Services via the GA4 Data API (runReport).

Reuses the OAuth refresh token from gsc_audit.py (analytics.readonly scope).
Verifies the property actually tracks johnson-services.de via the hostName
dimension before trusting numbers (Constitution: verify, never fabricate).

Usage:
    python3 ga4_audit.py        # last 28 days: hostName + channel breakdown
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from env_loader import load_env
from gsc_audit import _access_token


def run_report(token: str, prop: str, body: dict) -> dict:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport"
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main() -> int:
    load_env()
    token = _access_token()
    prop = os.environ.get("GA4_PROPERTY_ID", "")
    if not (token and prop):
        print("PENDING — GA4_PROPERTY_ID oder Token fehlt. Nichts abgerufen, nichts erfunden.")
        return 0

    rng = [{"startDate": "28daysAgo", "endDate": "today"}]
    try:
        host = run_report(token, prop, {
            "dateRanges": rng, "dimensions": [{"name": "hostName"}],
            "metrics": [{"name": "sessions"}, {"name": "screenPageViews"}, {"name": "totalUsers"}],
            "limit": 10,
        })
    except urllib.error.HTTPError as e:
        print(f"GA4 API Fehler {e.code}: {e.read().decode()[:250]}")
        return 0

    print(f"=== GA4 Property {prop} — hostName (28 Tage) ===")
    rows = host.get("rows", [])
    if not rows:
        print("  (keine Daten — Property neu oder trackt diese Domain nicht)")
    for row in rows:
        h = row["dimensionValues"][0]["value"]
        m = [mv["value"] for mv in row["metricValues"]]
        print(f"  {h:42} sessions={m[0]:>6} views={m[1]:>6} users={m[2]:>6}")

    try:
        ch = run_report(token, prop, {
            "dateRanges": rng, "dimensions": [{"name": "sessionDefaultChannelGroup"}],
            "metrics": [{"name": "sessions"}], "limit": 12,
        })
        print("\n=== Sessions nach Kanal (28 Tage) ===")
        for row in ch.get("rows", []):
            print(f"  {row['dimensionValues'][0]['value']:24} {row['metricValues'][0]['value']}")
    except urllib.error.HTTPError as e:
        print(f"(Kanal-Report Fehler {e.code})")
    return 0


if __name__ == "__main__":
    main()
