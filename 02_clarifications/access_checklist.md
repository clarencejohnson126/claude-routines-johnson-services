# Access Checklist (Stand 2026-06-14, aktualisiert nach Google-Freischaltung)

Geprüft per Discovery + Live-Tests. **Werte ausgeblendet** — nur Vorhandensein/Nutzbarkeit.

## Sofort nutzbar ✅

| Zugang | Status | Detail |
|--------|--------|--------|
| WordPress REST | ✅ live getestet | 14 Seiten/24 Posts gecrawlt |
| IONOS SMTP (Versand) | ✅ | `smtp.ionos.de:587`, `info@johnson-services.de` |
| IONOS IMAP (Lesen) | ✅ | `imap.ionos.de:993` |
| **Google Search Console API** | ✅ **live** | Konto `thaliajadedeyes@gmail.com`, Property `sc-domain:johnson-services.de`; echte 28-Tage-Daten gezogen |
| Google OAuth (Growth) | ✅ | Client-ID + Secret + scoped Refresh-Token in `.env` (`webmasters.readonly`, `analytics.readonly`) |
| Google Places API | ✅ live | Leadfinding läuft mit `GOOGLE_API_KEY` |
| Gemini / Perplexity / Brave | ✅ | in `.env` |
| Telegram | ✅ | Bot + Chat-ID |
| Meta (Johnson Page) | ✅ | Page `333849409814429` |
| browser-harness | ✅ | CDP 9333 (Lead-Fallback) |
| ElevenLabs (VO) | ✅ | Graph-`.env` |

## Teilweise / Setup nötig ⚠️

| Zugang | Status | Was fehlt |
|--------|--------|-----------|
| Google Analytics (GA4) | ✅ **live** | Property `536903926` (johnson-services.de), echte Daten gezogen (10 Sessions/28T, alle Direct) |
| Google Business Profile | ⚠️ | zusätzlicher `business.manage`-Scope (Re-Auth) + API-Enablement |
| Apify | ⚠️ | Token im Tresor-PDF, nicht in `.env` (optional) |

## Fehlt ❌

| Zugang | Status |
|--------|--------|
| Google Indexing API | ❌ Service-Account fehlt (optional) |

## Pre-Send-Check IONOS (Agent 002)

✅ Zugang · ✅ SMTP · ✅ IMAP · ✅ sichere `.env` · ✅ Absender · ⬜ Versandlimit (erfragen) · ⬜ erster Versand (Approval-Gate).
