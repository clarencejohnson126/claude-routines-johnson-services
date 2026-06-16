# Missing Credentials — Beschaffungsliste

Stand 2026-06-14 (aktualisiert nach Google-Freischaltung). **Keine Werte hier** — nur in `.env`.

## ✅ Erledigt
- Google OAuth (Client-ID + Secret + scoped Refresh-Token) in `.env`.
- Search Console API aktiviert + Zugriff über `thaliajadedeyes@gmail.com` → **echte GSC-Daten fließen**.
- Analytics Data API + Admin API aktiviert; **GA4 live**: Property `536903926` (johnson-services.de, verifiziert), echte Daten.
- Places API funktioniert mit `GOOGLE_API_KEY` (Leadfinding).

## 🟡 Noch offen
1. **Google Business Profile** (optional): Re-Auth mit zusätzlichem Scope `https://www.googleapis.com/auth/business.manage` (in `GOOGLE_OAUTH_SCOPES` ergänzen, `google_oauth_growth.py` erneut laufen lassen) + Business Profile API aktivieren.

## 🟢 Optional / später
- **Apify-Token** (`APIFY_API_TOKEN`) aus dem Tresor — API-Alternative zum Maps-Scrape.
- **Google Indexing API** Service-Account — schnelleres (Re-)Indexing.

## Hinweis zu den Konten
GSC + GA4 + Business Profile liegen unter `thaliajadedeyes@gmail.com` (nicht unter dem dedizierten `johnson.services.rheinneckar@gmail.com`). Der OAuth-Login erfolgt daher mit `thaliajadedeyes@gmail.com` (`GOOGLE_OAUTH_LOGIN_EMAIL`).
