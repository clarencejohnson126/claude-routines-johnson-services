"""Submit URLs to the Google Indexing API (faster crawl of new pages).

CAVEAT (ehrlich): Die Indexing API ist offiziell nur für Seiten mit JobPosting-
oder BroadcastEvent-Markup vorgesehen. Für normale Service-Seiten ist sie NICHT
offiziell unterstützt; Google triggert oft trotzdem einen Crawl, garantiert aber
keine Indexierung. Der saubere Weg für diese Seiten ist die Rank-Math-Sitemap in
der Search Console + URL-Prüfung -> Indexierung beantragen.

Voraussetzungen: GOOGLE_GROWTH_REFRESH_TOKEN mit `indexing`-Scope (Re-Consent via
google_oauth_growth.py) + aktivierte Indexing API im Cloud-Projekt.

Usage:
    python3 index_submit.py            # submit die neuen lokalen Seiten
    python3 index_submit.py <url> ...  # eigene URLs
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from gsc_audit import _access_token

DEFAULT_URLS = [
    "https://johnson-services.de/entruempelung/heidelberg/",
    "https://johnson-services.de/entruempelung/mannheim/",
    "https://johnson-services.de/entruempelung/ludwigshafen/",
    "https://johnson-services.de/entruempelung/keller-entruempeln-mannheim/",
    "https://johnson-services.de/entruempelung/reinigung-nach-entruempelung-mannheim/",
]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def submit(token: str, url: str) -> tuple[int, str]:
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, "ok"
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:160]


def main(argv: list[str]) -> int:
    token = _access_token()
    if not token:
        print("PENDING — kein Token. Erst google_oauth_growth.py (mit indexing-Scope) ausführen.")
        return 0
    urls = argv or DEFAULT_URLS
    for u in urls:
        code, msg = submit(token, u)
        print(f"  [{code}] {u}  {'' if code == 200 else msg}")
    print("\nHinweis: 403 'permission'/'not enabled' -> Indexing API im Cloud-Projekt aktivieren + Scope re-consent.")
    print("Für Service-Seiten zusätzlich: Sitemap in GSC einreichen + URL-Prüfung -> Indexierung beantragen.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
