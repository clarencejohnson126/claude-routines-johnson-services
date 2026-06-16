# Agentic Johnson Services — Growth Engine

Spec-getriebene Wachstums-Engine für **Johnson Services** (Entrümpelung, Haushaltsauflösung, Umzug, Reinigung; Region Rhein-Neckar, Mannheim, gegründet 2011).

**Prime Directives:** Keine Fake-Daten. Niemals dieselbe Adresse doppelt anschreiben. B2B-Outreach im **Sie-Ton**. Kundenkommunikation/Antworten macht der Inhaber selbst, der Agent macht **nur Outreach (Kaltakquise)**. Secrets nur über Umgebungsvariablen, niemals committen.

## Projektstruktur (relevant für Routinen)
- `05_implementation/scripts/` — ausführbare Python-Skripte (nur Standard-Library, keine pip-Installs nötig)
  - `leadfinding_batch.py` — **Haupt-Einstieg Outreach**: findet ~20 neue B2B-Leads via Google Places API, dedupliziert, sendet (wenn freigegeben)
  - `send_outreach_batch.py` — Versand via IONOS SMTP + Dedup-Logik (lokale Logs **und** IONOS-Sent-Ordner)
  - `gmaps_scrape.py` — Google-Places-Helfer (Textsuche, Detail, E-Mail-Extraktion, Junk-Filter)
  - `env_loader.py` — lädt `.env` (lokal) bzw. nutzt vorhandene Umgebungsvariablen (Cloud)
- `05_implementation/data/contacts.csv` — 50 Bestands-Leads (Dedup-Quelle, im Repo, **Repo muss privat sein**)
- `07_outputs/lead_lists/` — Lauf-Logs (gitignored, PII; in der stateless Cloud nicht persistent → Dedup läuft dort über den IONOS-Sent-Ordner)

---

### Cloud Routine: B2B Outreach (Johnson Services)

**Was die Routine tut:** Findet neue B2B-Leads (Hausverwaltungen, Immobilienmakler, Seniorenheime/Pflege, Nachlass/Erbrecht, Facility Management, Wohnungsbau) in 18 Rhein-Neckar-Regionen via Google Places API, dedupliziert gegen Bestand + alle bereits kontaktierten Adressen, und verschickt personalisierte deutsche Kaltakquise-Mails (Sie-Form) über IONOS SMTP. Jede Mail ist Multipart (Text + HTML) mit einem gebrandeten **Mehrwert-Block** (rotierender Praxis-Tipp + **10% Rabatt auf jedes Angebot**, Johnson-Blau #0066CC) als HTML, **kein Bild-Anhang** (B2B-Zustellbarkeit).

**Cadence:** Dienstag + Donnerstag, 09:00 Uhr Europe/Berlin.

**Genau ein Befehl (kein weiterer Input nötig):**
```bash
cd 05_implementation/scripts && python3 leadfinding_batch.py
```

**Erfolg sieht so aus:** Ausgabe endet mit `Versand: ECHT ok=N fail=0` mit N ≥ 1. Die Routine meldet: Anzahl gefundener Leads, Anzahl gesendeter Mails, Empfänger.

**Dedup (stateless-sicher, KRITISCH):** `already_sent_emails()` in `send_outreach_batch.py` liest (1) lokale Versand-Logs falls vorhanden **und** (2) den **IONOS-Sent-Ordner** ("Gesendete Objekte", Betreff-Suche "besenreine"). In der stateless Cloud gibt es keine lokalen Logs → der Sent-Ordner ist die persistente Wahrheit. Plus `05_implementation/data/contacts.csv` (50 Bestands-Leads). **So wird niemand doppelt angeschrieben, auch ohne lokalen Speicher.**

**Fehlerbehandlung (autonom, ohne Rückfrage):**
- Netz-/Places-API-Fehler (`urlopen error`): Das Skript wartet beim Start bis zu 10 Min auf Netz (`wait_for_network`). Findet es 0 Leads, bricht es sauber ab mit "Keine neuen Leads gefunden" → 0 Mails, **kein Crash, kein Teilversand**.
- IMAP-Dedup nicht erreichbar: `already_sent_via_imap()` gibt leere Menge zurück und fällt auf contacts.csv + lokale Logs zurück. Wenn unsicher, lieber **nicht senden** als doppelt senden.
- SMTP-Einzelfehler: andere Empfänger werden trotzdem bedient, ok/fail wird gezählt und gemeldet.

**Harte Regeln:**
- Niemals eine Adresse aus contacts.csv oder dem Sent-Ordner erneut anschreiben.
- Keine erfundenen Firmen/Leads, keine Platzhalter-/Junk-Adressen (Filter in `gmaps_scrape.py`).
- Sie-Form, Opt-out-Zeile (im Template enthalten), Absender `info@johnson-services.de`.
- Der Agent **antwortet nicht** auf eingehende Leads, er macht nur den Versand.

**Benötigte Umgebungsvariablen** (im Routines-Dashboard setzen, NICHT committen): `GOOGLE_API_KEY`, `IONOS_EMAIL`, `IONOS_EMAIL_PASSWORD`, `IONOS_SMTP_SERVER`, `IONOS_SMTP_PORT`, `IONOS_IMAP_SERVER`, `IONOS_IMAP_PORT`, `APPROVED_TO_SEND_OUTREACH=true`. Optional für Benachrichtigung: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
