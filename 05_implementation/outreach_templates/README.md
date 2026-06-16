# Outreach Templates

Aktive Draft-Templates: `../../07_outputs/email_drafts/initial_b2b_outreach_templates.md` (Mix-Zielgruppen, B2B-Sie).

## Reuse (NICHT neu bauen)
- Versand (IONOS SMTP): `../../../Johnson-Services/outreach/outreach_sender.py`
- Antwort-Monitoring (IMAP): `../../../Johnson-Services/outreach/inbox_monitor.py`
- Lead-Tracking (SQLite): `../../../Johnson-Services/outreach/db.py` + `data/outreach.db`
- Bewährte Anschreiben/Telefonskript: `../../../Johnson-Services-Hausverwaltung-Anschreiben.md`

## Gate
Kein Versand ohne Freigabe (`APPROVED_TO_SEND_OUTREACH=true` oder ausdrücklich). Erst Testmail an `info@johnson-services.de`.
