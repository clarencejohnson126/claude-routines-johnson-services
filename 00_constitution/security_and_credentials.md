# Security & Credentials

## Sicherheitsregeln

- Secrets niemals anzeigen.
- Passwörter niemals in Klartext dokumentieren.
- `.env` verwenden (chmod 600, gitignored).
- `.env.example` nur mit Platzhaltern.
- Zugangsdaten nicht in Markdown-Dateien speichern.
- Keine API-Keys in Logs ausgeben.
- Keine Credentials in Commits übernehmen.
- Bei unklarem Zugriff den Nutzer fragen.

## Approval Gates — vor diesen Aktionen IMMER den Nutzer fragen

- Veröffentlichung einer WordPress-Seite
- Änderung der Startseite oder Haupt-Landingpage
- Versand von Outreach-E-Mails
- Aktivieren eines wiederkehrenden E-Mail-Versands (nur mit `APPROVED_TO_SEND_OUTREACH=true` oder ausdrücklicher Bestätigung)
- Nutzung neuer externer Tools
- Änderung bestehender Automationen
- Löschen oder Überschreiben bestehender Inhalte
- Massenexport von Leads
- Veröffentlichung von TikTok / Social Content

## Credential-Speicherorte (nur Verweise, keine Werte)

| Speicherort | Inhalt |
|-------------|--------|
| `Agentic Johnson Services/.env` (chmod 600) | Aktive Credentials dieses Projekts |
| `../Graph-Growth-Agents/.env` | WordPress, Gemini, Perplexity, Brave, Google Ads, Meta (Rebelz) |
| `../Johnson-Services/.env` | IONOS Mail, Telegram, Meta (Johnson) |
| `../env Automated Ads.pdf` | Tresor: generischer Google API Key, OAuth-Client, Apify-Token, OpenAI |
| `../Graph-Growth-Agents/config/google_ads.yaml` | Google-Ads-OAuth-Konfiguration |

## Status (Stand 2026-06-14) — Werte ausgeblendet

Vollständige Matrix: [`../02_clarifications/access_checklist.md`](../02_clarifications/access_checklist.md)
Lücken + Beschaffung: [`../02_clarifications/missing_credentials.md`](../02_clarifications/missing_credentials.md)

- ✅ Sofort nutzbar: WordPress REST, IONOS SMTP+IMAP, Gemini, Perplexity, Brave, Telegram, Meta (Johnson), browser-harness (CDP 9333).
- ⚠️ Teilweise: Google OAuth-Client-ID + API-Key vorhanden; **Client-Secret + scoped Refresh-Token + GA4-Property-ID + API-Enablement fehlen** → blockiert Live-Search-Console/GA4/GBP.
- ❌ Fehlt: Google Maps/Places-API-Enablement (Workaround: browser-harness), Google Indexing API.

OAuth-Login für Google-Scopes: `johnson.services.rheinneckar@gmail.com` (siehe `GOOGLE_OAUTH_LOGIN_EMAIL`).
