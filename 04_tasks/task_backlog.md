# Task Backlog (priorisiert)

Aggregiert aus SEO-Audit, Leadtest und Specs. 🔴 hoch · 🟡 mittel · 🟢 niedrig.

## SEO / WordPress (datengetrieben, GSC live 2026-06-14)
- 🔴 Mannheim-URLs + Haushaltsauflösung-Dubletten konsolidieren (301/Canonical). *(Approval: Live-WP)*
- ✅ **LIVE (2026-06-14, Freigabe)**: `/entruempelung/heidelberg/` (277 W) + `/entruempelung/mannheim/` (282 W) befüllt (waren leer); `/umzuege/` (551 W, Chatbot erhalten) ausgebaut. → Positionen in GSC über die nächsten Wochen beobachten.
- ✅ **LIVE (2026-06-15)**: `/haushaltsaufloesungen/` 79→435 Wörter (inkl. Reinigungs-Abschnitt), WhatsApp-Button erhalten.
- ✅ **LIVE**: Startseite verlinkt auf `/entruempelung/mannheim/` (Konsolidierung), Chatbot erhalten.
- ✅ **LIVE (2026-06-15)**: Neue Money-Pages `/entruempelung/ludwigshafen/` (277 W) + `/entruempelung/keller-entruempeln-mannheim/` (228 W), von Startseite intern verlinkt. (`wp_publish_round3.py`)
- 🟡 Startseiten-Title/Meta für CTR (Pos 9.7, nur 1.7%); Preis-Intent „entrümpelung mannheim kosten" bedienen.
- ✅ **LIVE**: Reinigung-Abschnitt auf Startseite + Entrümpelung-Hub (441) + Haushaltsauflösung (252).
- 🟡 Bestehende „Sie"-Seiten (Rüsselsheim id 409 etc.) auf **du/ihr** umschreiben für Section-Konsistenz (Live-Edit, Freigabe nötig). Entscheidung Nutzer 2026-06-14: Website alles du/ihr.
- ✅ Drafts erstellt UND live veröffentlicht: Heidelberg (201) + Mannheim (256) + Umzüge (266), du/ihr. Publisher: `05_implementation/scripts/wp_publish.py`.
- 🟢 GA4-Property-ID nachreichen → Conversions; GBP-Scope nachrüsten; Title/Meta/Schema-Audit Top-Seiten.

## Outreach
- ✅ 20-Lead-Batch (`leadfinding_batch.py` → `leads_batch_2026-06-14.csv`), dedupliziert gegen 50 Bestands-Leads, 5 neue Zielgruppen (Makler/Pflege/Nachlass/Facility/Wohnungsbau), 15/20 mit echter E-Mail.
- ✅ 20 personalisierte Outreach-Drafts (`outreach_batch_2026-06-14.md`), Sie-Form.
- ✅ Testmail an info@johnson-services.de gesendet (2026-06-15, `send_test_mail.py`).
- ✅ **Erster Versand ERLEDIGT 2026-06-15 12:57** (13/13 gesendet, 0 Fehler, Beleg `outreach_sent_log_2026-06-15.csv` mit Zeitstempeln). Hinweis: der geplante 08:00-launchd-Job war FEHLGESCHLAGEN (macOS TCC: `/bin/bash` durfte das Desktop-Skript nicht lesen, Exit 126) → Job entfernt, manuell im Vordergrund nachgeholt. Lehre: launchd nie über bash-Wrapper auf dem Desktop, immer `/usr/local/bin/python3` direkt (siehe Memory [[feedback_no_bluffing_verify_execution]]).
- 🟢 Do-not-contact-Liste + Opt-out-Satz finalisieren.
- ℹ️ Bestehende `contacts.csv`: 50 Leads, CSV-Status „pending" (DB-Status kann abweichen).

## Content / Video
- ✅ Content-Paket „Wohnungsauflösung nach Todesfall" als Draft (`blog_wohnungsaufloesung_todesfall.md` + Social). Nächste Themen: „Entrümpelung für Makler", „Wohnung übergabefähig machen".
- 🟢 Video Woche 1 produzieren (Assets + Charlotte-VO).

## Daten / Klärung
- ✅ Gründungsjahr geklärt: **2011** (bestätigt 2026-06-14). „seit 2011" in Copy erlaubt.
- ✅ Ton-Regel bestätigt: B2B-Outreach **Sie**, Website/Social **du/ihr**.
