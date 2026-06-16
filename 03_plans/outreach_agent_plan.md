# Plan — B2B Leadfinding & Outreach Agent

Basis: 5 echte Test-Leads (`../07_outputs/lead_lists/test_leads_5.csv`) + Templates (`../07_outputs/email_drafts/initial_b2b_outreach_templates.md`).

## Leadfinding
1. Primär: Google Places API (Text Search + Details) via `gmaps_scrape.py` — funktioniert mit dem gelieferten Key. Fallback: browser-harness (`workflows/leadfinding_runbook.md`).
2. Pro Lauf 20 Leads, 2 Läufe/Woche, Zielgruppen-Mix + Region rotieren.
3. E-Mail-Enrichment best-effort aus Impressum (real; leer lassen wenn nicht gefunden).
4. Dedupe gegen bestehende `../../Johnson-Services/outreach/contacts.csv` (51 Leads) + Do-not-contact.

## Outreach (Approval-Gate)
5. Drafts personalisieren (Firmenname/Ansprechpartner/Bezug).
6. Pre-Send-Check (IONOS, Versandlimit, Signatur) — siehe access_checklist.
7. Erst Testmail an `info@johnson-services.de` (nach Freigabe Frage 11), dann echter Versand nur mit `APPROVED_TO_SEND_OUTREACH=true`.
8. Reuse Versand: `../../Johnson-Services/outreach/outreach_sender.py` (IONOS SMTP); Tracking: `db.py`; Antworten: `inbox_monitor.py`.

## Status-Lifecycle
`new → qualified → email_drafted → approved_to_send → sent → followup_due → followup_sent → replied` (+ `not_relevant`, `do_not_contact`).
