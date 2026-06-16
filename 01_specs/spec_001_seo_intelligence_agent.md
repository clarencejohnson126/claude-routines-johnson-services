# Spec 001 — SEO Intelligence Agent

## Intent

Herausfinden, warum Johnson Services organisch bei Google nicht stark genug sichtbar ist, und konkrete SEO-Aktionen ableiten.

## Priorität

Priorität 1.

## Scope (prüfen)

Google Search Console · Google Analytics · Google Business Profile (falls verfügbar) · WordPress-Seitenstruktur · indexierte/nicht indexierte Seiten · Keywords · Impressionen · Klicks · CTR · Rankingpositionen · lokale Wettbewerber · technische SEO-Probleme · interne Verlinkung · Titles · Meta Descriptions · Überschriftenstruktur · LocalBusiness-Schema · FAQ-Schema · Ladezeit (falls Daten verfügbar).

## Out of Scope

Keine Ads-Optimierung · keine neuen Seiten veröffentlichen · keine bestehenden Hauptseiten live ändern · keine Rankingversprechen.

## Inputs & Tool-/Credential-Status (real, Stand 2026-06-14)

| Input | Status | Quelle |
|-------|--------|--------|
| WordPress-Seitenstruktur | ✅ nutzbar | WP REST `https://johnson-services.de/wp-json/wp/v2/` (Basic-Auth, `WORDPRESS_*`) |
| Wettbewerbs-/Keyword-Recherche | ✅ vorhanden | `../Johnson-Services/research/competitor_ad_research_2026-03-26.md`, `research/data/competitor_intel_entruempelung_umzug_20260326.md` |
| Google Search Console | ⚠️ pending | OAuth-Client-ID + API-Key da; Client-Secret + scoped Refresh-Token + GSC-Verifikation fehlen |
| Google Analytics (GA4) | ⚠️ pending | `GA4_PROPERTY_ID` leer, Service-Account-JSON fehlt |
| Google Business Profile | ⚠️ pending | benötigt `business.manage`-Scope |
| Ladezeit/Lighthouse | ✅ optional | chrome-devtools MCP / Lighthouse lokal |

## Workflow

1. Projektstruktur prüfen
2. Credentials prüfen (`02_clarifications/access_checklist.md`)
3. Website auslesen (WP REST: pages, posts, slugs, titles, excerpt/meta, categories, interne Links)
4. WordPress-Seitenstruktur analysieren
5. Search-Console-Daten abrufen (sobald freigeschaltet)
6. Top-Keywords identifizieren
7. Keywords mit Position 5–30 markieren (Quick-Win-Kandidaten)
8. Keywords ohne passende Landingpage markieren (→ Landing-Page-Matrix, Agent 003)
9. Lokale Wettbewerber identifizieren
10. Technische SEO-Probleme dokumentieren
11. Konkrete Taskliste erstellen

## Outputs

- `07_outputs/seo_reports/` (z. B. `initial_seo_audit.md`)
- `04_tasks/task_backlog.md`
- `03_plans/seo_agent_plan.md`

## Acceptance Criteria

Aktuelle Sichtbarkeit · wichtigste Keywords · fehlende Seiten · schwache Seiten · technische Probleme · lokale Chancen · priorisierte Maßnahmen · klare nächste Schritte. Reale Daten mit Quelle + Zeitstempel; pending-Abschnitte klar gekennzeichnet.

## Human Approval Gates

Live-Änderung an WordPress · Indexing Request · Änderung der Startseite · Änderung wichtiger Leistungsseiten.
