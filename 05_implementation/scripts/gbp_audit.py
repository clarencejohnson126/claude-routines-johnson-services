"""Google Business Profile audit (Spec Agent 001 scope: GBP falls verfügbar).

Listet GBP-Konten + Standorte über die aktuellen APIs:
  - Account Management: mybusinessaccountmanagement.googleapis.com/v1/accounts
  - Business Information: mybusinessbusinessinformation.googleapis.com/v1/{account}/locations

CAVEAT (ehrlich): Bewertungen + Insights laufen über die ALTE/eingeschränkte
GBP-API (mybusiness v4) und brauchen eine separate Google-Freischaltung
(Allowlisting). Ohne diese liefert nur Konten/Standorte ein Ergebnis.

Voraussetzungen: GOOGLE_GROWTH_REFRESH_TOKEN mit `business.manage`-Scope
(Re-Consent) + aktivierte Business-Profile-APIs im Cloud-Projekt.

Usage: python3 gbp_audit.py
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from gsc_audit import _access_token


def api(token: str, url: str):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> int:
    token = _access_token()
    if not token:
        print("PENDING — kein Token. Erst google_oauth_growth.py (mit business.manage-Scope) ausführen.")
        return 0
    try:
        accts = api(token, "https://mybusinessaccountmanagement.googleapis.com/v1/accounts").get("accounts", [])
    except urllib.error.HTTPError as e:
        print(f"Account-API Fehler {e.code}: {e.read().decode()[:180]}")
        print("-> Business Profile API im Cloud-Projekt aktivieren + business.manage-Scope re-consent.")
        return 0
    if not accts:
        print("Keine GBP-Konten für dieses Google-Konto sichtbar.")
        return 0
    for a in accts:
        print(f"Konto: {a.get('accountName')}  ({a.get('name')})  Typ={a.get('type')}")
        try:
            locs = api(token, f"https://mybusinessbusinessinformation.googleapis.com/v1/{a['name']}/locations?readMask=name,title,storefrontAddress,websiteUri,phoneNumbers&pageSize=100").get("locations", [])
            for loc in locs:
                addr = (loc.get("storefrontAddress") or {})
                city = ", ".join(addr.get("addressLines", []) + [addr.get("locality", "")]).strip(", ")
                print(f"   - {loc.get('title')}  | {city}  | {loc.get('websiteUri','')}")
        except urllib.error.HTTPError as e:
            print(f"   Standort-API Fehler {e.code}: {e.read().decode()[:140]}")
    print("\nHinweis: Bewertungen/Insights brauchen GBP-API-Allowlisting (separater Google-Antrag).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
