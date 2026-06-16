"""B2B Leadfinding via Google Maps for Johnson Services.

Primary path: Google Places API (Text Search + Details) using GOOGLE_API_KEY.
The provided key supports Places API, so we use it (API > browser per the
tool-selection doctrine). Fallback: browser-harness Google-Maps scrape
(CDP 9333) — see workflows/leadfinding_runbook.md.

Output CSV columns match Spec 002. Best-effort email enrichment reads the
lead's own website/Impressum (real data; field stays empty if none found).
No fabrication: every field is sourced from Places API or the lead's site.

Usage:
    python3 gmaps_scrape.py "Mannheim" 5
"""
from __future__ import annotations

import csv
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from env_loader import require

OUT = Path(__file__).resolve().parent.parent.parent / "07_outputs" / "lead_lists" / "test_leads_5.csv"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PLACEHOLDER_EMAILS = (
    "name@unternehmen", "mustermann", "muster@", "max.muster", "example.", "@example",
    "beispiel", "ihre-email", "ihremail", "vorname.nachname", "test@", "info@domain",
    "@domain.", "@firma.", "@ihredomain", "@deinedomain", "email@beispiel", "user@",
    "@thread.", "onmicrosoft.com", "skype", "sentry", "wixpress", "@2x", "@3x",
    "osmfoundation", "openstreetmap", "mapbox", "@sentry.", "@wordpress.org", "wpengine",
)
UA = {"User-Agent": "Mozilla/5.0 JS-GrowthEngine/1.0"}

# Target-group MIX (Nutzer-Entscheidung 2026-06-14)
QUERIES = [
    ("Hausverwaltung", 2),
    ("Immobilienmakler", 1),
    ("Nachlassverwalter Betreuungsbüro", 1),
    ("Seniorenheim Pflegeheim", 1),
]


def _key() -> str:
    return require("GOOGLE_API_KEY")["GOOGLE_API_KEY"]


def textsearch(query: str, region_city: str) -> list[dict]:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" + urllib.parse.urlencode(
        {"query": f"{query} {region_city}", "region": "de", "language": "de", "key": _key()}
    )
    with urllib.request.urlopen(url, timeout=20) as r:
        import json
        return json.load(r).get("results", [])


def details(place_id: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/place/details/json?" + urllib.parse.urlencode(
        {"place_id": place_id, "fields": "name,website,formatted_phone_number,formatted_address", "language": "de", "key": _key()}
    )
    with urllib.request.urlopen(url, timeout=20) as r:
        import json
        return json.load(r).get("result", {})


def best_effort_email(website: str) -> str:
    if not website:
        return ""
    base = website.rstrip("/")
    for path in ("", "/impressum", "/kontakt", "/impressum/"):
        try:
            req = urllib.request.Request(base + path, headers=UA)
            with urllib.request.urlopen(req, timeout=12) as r:
                html = r.read(400_000).decode("utf-8", "ignore")
            for m in EMAIL_RE.findall(html):
                low = m.lower()
                if low.endswith((".png", ".jpg", ".gif", ".webp")):
                    continue
                if any(p in low for p in PLACEHOLDER_EMAILS):
                    continue
                return m
        except Exception:
            continue
    return ""


def score(group: str, website: str, phone: str, email: str) -> tuple[int, str]:
    s = 50
    if website:
        s += 20
    if phone:
        s += 15
    if email:
        s += 10
    s += 5  # region match (query is region-scoped)
    high = group in ("Hausverwaltung", "Immobilienmakler", "Nachlassverwalter Betreuungsbüro")
    relevance = "hoch" if (high and website) else "mittel"
    return min(s, 100), relevance


GROUP_LABEL = {
    "Hausverwaltung": "Hausverwaltung",
    "Immobilienmakler": "Immobilienmakler",
    "Nachlassverwalter Betreuungsbüro": "Nachlass/Betreuer",
    "Seniorenheim Pflegeheim": "Seniorenheim/Pflege",
}


def main(city: str, total: int) -> int:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows, seen = [], set()
    for query, want in QUERIES:
        results = textsearch(query, city)
        picked = 0
        for res in results:
            if picked >= want:
                break
            name = res.get("name", "").strip()
            if not name or name.lower() in seen:
                continue
            det = details(res["place_id"]) if res.get("place_id") else {}
            website = det.get("website", "")
            phone = det.get("formatted_phone_number", "")
            email = best_effort_email(website)
            sc, rel = score(query, website, phone, email)
            rows.append({
                "firma": name,
                "zielgruppe": GROUP_LABEL[query],
                "region": city,
                "website": website,
                "email": email,
                "kontakt_telefon": phone,
                "ansprechpartner": "",
                "relevanz": rel,
                "lead_score": sc,
                "status": "qualified" if rel == "hoch" else "new",
                "quelle": "Google Places API (Text Search)",
                "gefunden_am": now,
            })
            seen.add(name.lower())
            picked += 1
            time.sleep(0.2)
    rows = rows[:total]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} leads -> {OUT}")
    for r in rows:
        print(f"  [{r['lead_score']}] {r['zielgruppe']:18} {r['firma'][:38]:38} {r['website'][:34]}")
    return 0


if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Mannheim"
    total = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    sys.exit(main(city, total))
