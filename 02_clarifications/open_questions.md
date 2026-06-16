# Open Questions (Stand 2026-06-14)

## Die 12 Spec-Fragen — Status

| # | Frage | Antwort / Status |
|---|-------|------------------|
| 1 | Welche exakte WordPress-URL? | ✅ `https://johnson-services.de` |
| 2 | Welche WordPress-Rechte? | ✅ Application Password, REST API; posts/pages create/update möglich (Autoblog nutzt es) |
| 3 | Wo liegt die Social-Media-Automation? | ✅ `../Graph-Growth-Agents/automation/johnson_{entruempelung,innenausbau,autoblog}/` |
| 4 | Welche IONOS-Adresse für Outreach? | ✅ `info@johnson-services.de` |
| 5 | SMTP oder nur IMAP? | ✅ beide vorhanden (`smtp.ionos.de:587`, `imap.ionos.de:993`) |
| 6 | Outreach zunächst nur als Draft? | ✅ Ja — Sprint 01 nur Drafts; echter Versand ist Approval-Gate |
| 7 | Welche Region hat höchste Priorität? | ✅ Mannheim (Nutzer-Default) |
| 8 | Welche Zielgruppe höchste Priorität? | ✅ Mix (Hausverwaltungen + Makler + Nachlass/Betreuer + Seniorenheime/Pflege) — Nutzer 2026-06-14 |
| 9 | Darf Google Maps API für Leadfinding genutzt werden? | ⚠️ Maps-API-Enablement offen; Nutzer hat **browser-harness Google-Maps-Scrape** freigegeben |
| 10 | Browser Hannes MCP / Browser Use Scale verfügbar? | ✅ browser-harness (CDP 9333) lokal; Browser-Use-Scale-Key nicht nötig |
| 11 | Darf eine Testmail an die eigene Adresse gesendet werden? | ⬜ offen — bitte bestätigen (Vorschlag: Test an `info@johnson-services.de`) |
| 12 | Reinigung auf Startseite oder nur Leistungsseiten? | ✅ Startseite + relevante Service-Seiten (Nutzer 2026-06-14) |

## ✅ Geklärte Datenfestlegungen (2026-06-14)

### A) Gründungsjahr: **2011** (bestätigt)
„seit 2011" ist korrekt und darf in Copy verwendet werden. Die „2016"-Angabe im alten Outreach-Material ist falsch und wird nicht mehr verwendet.

### B) Ton: **B2B = Sie, Website/Social = du/ihr** (bestätigt)
B2B-Outreach an Hausverwaltungen, Makler, Institutionen und Behörden in „Sie" (professioneller Auftritt). Konsumentenseitige Website-/Social-/Landing-Copy in „du/ihr".

## Offene Google-Frage

Zum Freischalten von Live-Search-Console/GA4/GBP: bitte **OAuth Client-Secret** (zur Client-ID `1092230382228-…`) + **GA4 Property-ID** liefern und bestätigen, dass die APIs im Cloud-Projekt aktiviert und `johnson-services.de` in der Search Console verifiziert ist. Siehe `missing_credentials.md`.

## Weitere Frage

Versandlimit der IONOS-Adresse (E-Mails/Stunde bzw. /Tag) für sicheren Outreach-Takt?
