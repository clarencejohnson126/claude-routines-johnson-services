# Spec 002 — B2B Leadfinding & Outreach Agent

## Intent

Zweimal pro Woche jeweils 20 qualifizierte B2B-Leads finden und personalisierte Outreach-E-Mails vorbereiten oder nach Freigabe versenden.

## Priorität

Sehr hoch. Priorität 2 nach SEO.

## Zielgruppen

Hausverwaltungen · Immobilienmakler · Nachlassverwalter · Erbrechtsanwälte · Seniorenheime · Pflegeeinrichtungen · betreutes Wohnen · Facility-Management-Firmen · Wohnungsbaugesellschaften · Airbnb-Hosts · Ferienwohnungsbetreiber · Vermieter möblierter Wohnungen · kleinere Bauunternehmen · Handwerker-Netzwerke.

## Regionen

Mannheim · Heidelberg · Ludwigshafen · Viernheim · Weinheim · Schwetzingen · Speyer · Worms · Darmstadt · Karlsruhe.

## Tools & Status (real, Stand 2026-06-14)

| Tool | Status |
|------|--------|
| browser-harness (Google-Maps-Scrape, CDP 9333) | ✅ nutzbar — **vom Nutzer für Sprint 01 freigegeben** |
| Google Maps/Places API | ⚠️ Key vorhanden, API-Enablement offen |
| Apify (Google-Maps-Actor) | ⚠️ Token im Tresor-PDF, nicht in `.env` |
| IONOS-SMTP-Versand | ✅ konfiguriert (`IONOS_*`) + bestehendes Skript `../Johnson-Services/outreach/outreach_sender.py` |
| IMAP-Antwort-Monitoring | ✅ `../Johnson-Services/outreach/inbox_monitor.py` |
| Lead-DB (SQLite) | ✅ `../Johnson-Services/outreach/db.py` + bestehende `contacts.csv` (51 echte Leads) |

## Workflow

1. Zielgruppe für aktuellen Lauf bestimmen
2. Region bestimmen
3. Leads über Google Maps (browser-harness) finden
4. Firmenname speichern
5. Website speichern
6. E-Mail oder Kontaktformular speichern
7. Ansprechpartner prüfen, wenn möglich
8. Relevanz bewerten
9. Lead-Score vergeben
10. Personalisierte E-Mail erstellen
11. Follow-up vorbereiten
12. CRM / CSV / Markdown-Leadliste aktualisieren

## Frequenz

Zweimal pro Woche: 20 Leads pro Lauf, 40 Leads pro Woche.

## Lead Status

`new` · `qualified` · `email_drafted` · `approved_to_send` · `sent` · `followup_due` · `followup_sent` · `replied` · `not_relevant` · `do_not_contact`

## E-Mail-Versand über IONOS — Pre-Send-Check

IONOS-Zugang vorhanden? · SMTP-Daten vorhanden? · IMAP-Passwort vorhanden? · sichere `.env`? · Testmail möglich? · Versandlimit bekannt? · Absenderadresse korrekt? · Signatur korrekt? Alle ✅ bis auf Versandlimit (beim Nutzer erfragen) — siehe access_checklist.

## Compliance

Nur seriöse B2B-Outreach: kein aggressiver Spam · keine Privatpersonen · nur relevante Geschäftsadressen · Bezug zur Zielgruppe · kurze Mail · klare Leistung · einfache Antwortmöglichkeit · Opt-out respektieren · Do-not-contact-Liste pflegen · bei rechtlicher Unsicherheit Nutzer fragen.

## Output

`07_outputs/lead_lists/` · `07_outputs/email_drafts/` · `05_implementation/outreach_templates/`

## Human Approval Gates

Vor dem ersten echten Versand immer Nutzer fragen. Wiederkehrender Versand nur mit ausdrücklicher Bestätigung oder `APPROVED_TO_SEND_OUTREACH=true`.

## Beispiel-Positionierung

„Johnson Services unterstützt Hausverwaltungen, Makler und Immobilienverwalter bei kurzfristigen Entrümpelungen, Wohnungsauflösungen, Übergaben und optionaler Reinigung in Mannheim und Umgebung."
