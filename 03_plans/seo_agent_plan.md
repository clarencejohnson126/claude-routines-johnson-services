# Plan — SEO Intelligence Agent

Basis: `../07_outputs/seo_reports/initial_seo_audit.md` (echter WP-Crawl 2026-06-14).

## Sofort (Quick Wins, Approval-Gate Live-WP)
1. Slug `entruempelungen-mannhein` → `entruempelung-mannheim` korrigieren (301-Redirect), Doppelseite mit `entruempelung` konsolidieren (Canonical).
2. Title/Meta/H1 der Top-Leistungsseiten prüfen + auf „<Leistung> Mannheim" schärfen.

## Kurzfristig
3. GSC/GA4 freischalten (`google_oauth_growth.py` + `GA4_PROPERTY_ID`), dann `gsc_audit.py` → echte Keywords + Position-5–30-Quick-Wins.
4. LocalBusiness- + FAQ-Schema auf Leistungsseiten ergänzen (Draft).
5. Interne Verlinkung Service ↔ Blog ↔ (geplante) lokale Money-Pages.

## Mittelfristig
6. Lokale Money-Pages priorisiert nach echter GSC-Nachfrage (→ `wordpress_plan.md`).
7. Content-Tiefe für Haushaltsauflösung (3 Posts) + Umzug (7) + Reinigung (0) ausbauen (→ `content_plan.md`).

## Tools
`wp_client.py` (read), `gsc_audit.py` (GSC), chrome-devtools MCP (Lighthouse). Outputs → `07_outputs/seo_reports/`, Tasks → `04_tasks/task_backlog.md`.
