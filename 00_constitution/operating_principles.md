# Operating Principles

## Spec-driven, factory-first

Diese Growth Engine ist eine **Fabrik aus Agenten + Code**, nicht eine Sammlung von Einzel-Tasks. Jeder Agent hat eine Spec (`01_specs/`), einen Plan (`03_plans/`), Tasks (`04_tasks/`), Validierung (`06_validation/`) und Outputs (`07_outputs/`). Die Reihenfolge ist immer: Spec → Plan → Task → (Freigabe) → Umsetzung → Validierung.

## Extensible by design

- Offen für Erweiterung, geschlossen für Modifikation.
- Keine hardcodierten Model-IDs, keine brüchigen Selektoren, keine monolithische Glue-Logik.
- Konfiguration über `.env`; Tools/Agenten austauschbar.

## Reuse vor Neubau

Vor jedem neuen Skript prüfen, ob es im Schwester-Projekt bereits existiert:

| Zweck | Bestehende Quelle (read-only Vorbild) |
|-------|----------------------------------------|
| WordPress REST (Basic-Auth, posts/pages) | `../Graph-Growth-Agents/automation/johnson_autoblog/autoblog.py` |
| Ratgeber-/Seitenübersicht aktualisieren | `../Graph-Growth-Agents/automation/johnson_autoblog/update_ratgeber.py` |
| IONOS-SMTP-Versand | `../Johnson-Services/outreach/outreach_sender.py` |
| IMAP-Inbox-Monitoring | `../Johnson-Services/outreach/inbox_monitor.py` |
| Lead-Tracking (SQLite) | `../Johnson-Services/outreach/db.py` |
| OAuth-Refresh-Token-Flow | `../Graph-Growth-Agents/scripts/generate_google_refresh_token.py` |
| Telegram-Notify | `../Graph-Growth-Agents/automation/johnson_entruempelung/notify_hermes.py` |

## Tool-Reihenfolge (für Web/Scraping/Daten)

1. **API vorhanden** (WordPress REST, Google APIs, IONOS, Meta) → API, nie Browser.
2. **Statische HTML-Seite** → `curl` / HTTP-GET.
3. **Wiederholbarer Flow** → Playwright MCP.
4. **Exploratives/messy Scraping ohne API** (Google Maps Leads) → browser-harness (CDP 9333).

## Always-on nur nach Tokconomics

Erst Wert nachweisen (Sichtbarkeit, echte Leads), dann erst Automationen auf einen Zeitplan setzen. Sprint 01 ist bewusst **manuell + Draft** — keine Cron/launchd-Jobs aus diesem Projekt, bis das Fundament steht und der Nutzer freigibt.

## Anti-Halluzinations-Regeln

- Reale Daten immer mit **Quelle + Zeitstempel** dokumentieren.
- Wenn nur simuliert werden kann: klar „SIMULIERT" kennzeichnen.
- Keine erfundenen Kundenzahlen, Statistiken, Sterne, Prozente, Testimonials (UWG- + Steuerprüfungs-Risiko).
- Keine Em-Dashes „—" oder „ - " in Copy/Captions (wirkt wie KI); Kommas/Punkte/Doppelpunkte verwenden.
