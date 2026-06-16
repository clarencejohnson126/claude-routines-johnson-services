# Runbook — B2B Leadfinding

## Primärweg: Google Places API (empfohlen)
Der gelieferte `GOOGLE_API_KEY` unterstützt die Places API (verifiziert 2026-06-14).

```bash
cd "05_implementation/scripts"
python3 gmaps_scrape.py "Mannheim" 5      # Test: 5 Leads im Zielgruppen-Mix
python3 gmaps_scrape.py "Heidelberg" 20   # produktiv: 20/Lauf
```
Output: `07_outputs/lead_lists/`. Felder: Firma, Zielgruppe, Region, Website, E-Mail (best-effort aus Impressum), Telefon, Relevanz, Lead-Score, Status.

## Fallback: browser-harness (falls API limitiert/deaktiviert)
Voraussetzung: Automation-Chrome auf Port 9333 (`~/Developer/browser-harness/start-automation-chrome.sh`).

```bash
browser-harness -c '
new_tab("https://www.google.com/maps/search/Hausverwaltung+Mannheim")
wait_for_load()
capture_screenshot()
# Treffer-Panel scrollen, Firmennamen + Website per js() extrahieren
'
```
Danach Ergebnisse in dasselbe CSV-Schema überführen. browser-harness nur nutzen, wenn die API nicht reicht (Tool-Doktrin: API vor Browser).

## Qualität & Compliance
- Dedupe gegen `../../Johnson-Services/outreach/contacts.csv` (51 Bestands-Leads).
- Nur Geschäftsadressen. Do-not-contact respektieren.
- Keine erfundenen Kontaktdaten. Leeres E-Mail-Feld ist erlaubt.
