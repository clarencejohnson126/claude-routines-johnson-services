# Spec 003 — WordPress Local Landing Page Agent

## Intent

Bestehende WordPress-Seite analysieren und lokale Money-Pages sowie relevante Leistungsabschnitte als Drafts vorbereiten.

## Wichtig

**Keine separate neue Reinigungsdienste-Navigation als eigener Reiter.** Reinigung wird in die bestehende Landingpage (Startseite) und relevante Leistungsseiten integriert (Nutzer-Entscheidung 2026-06-14: Startseite + Service-Seiten).

## Scope (prüfen)

Bestehende Seiten/Unterseiten · WordPress-Menüs · Leistungen · CTA · Kontaktformulare · interne Links · Local-SEO-Struktur · Meta-Daten · FAQ-Bereiche · Schema-Markup.

## Tool-Status (real)

WP REST `https://johnson-services.de/wp-json/wp/v2/` (Basic-Auth `WORDPRESS_*`) ist nutzbar. Read-only-Client nach Vorbild `../Graph-Growth-Agents/automation/johnson_autoblog/autoblog.py` (`wp_post`) und `update_ratgeber.py` (`wp`). Kategorien-IDs dort: 3=Entrümpelung, 4=Haushaltsauflösung, 5=Umzug.

## Neue Inhaltsanforderung: Reinigung nach Entrümpelung

Abschnitt „Reinigung nach Entrümpelung oder Umzug" ergänzen. Ziel: Johnson Services nicht nur als Entrümpler, sondern als Dienstleister positionieren, der Räume wieder übergabefähig, vermietbar oder nutzbar macht.

**Zielgruppen Reinigung:** Airbnb-Hosts · Ferienwohnungsbetreiber · Vermieter · Hausverwaltungen · Immobilienmakler · Erben nach Haushaltsauflösung · Menschen nach Umzug · Gewerbekunden · Eigentümer nach Wohnungsräumung.

## Local Landing Page Matrix (prüfen, nicht automatisch alle erstellen)

`/entruempelung-mannheim` · `/haushaltsaufloesung-mannheim` · `/wohnungsaufloesung-mannheim` · `/umzug-mannheim` · `/keller-entruempeln-mannheim` · `/reinigung-nach-entruempelung-mannheim` · `/entruempelung-heidelberg` · `/haushaltsaufloesung-heidelberg` · `/entruempelung-ludwigshafen` · `/entruempelung-darmstadt` · `/entruempelung-karlsruhe`

Reihenfolge: 1. Audit → 2. Matrix → 3. Priorisierung → 4. Drafts → 5. Freigabe → 6. Veröffentlichung.

## Acceptance Criteria

Lokale Suchintention · klare Dienstleistung · starke Headline · schnelle Kontaktmöglichkeit · Preis-/Ablaufhinweis · FAQ · interne Links · Trust-Elemente · lokale Keywords · sauberes Schema-Markup · mobile Lesbarkeit.

## Output

`07_outputs/landing_page_drafts/` · `03_plans/wordpress_plan.md` · `04_tasks/task_backlog.md`

## Approval Gates

Veröffentlichung · Änderung der Startseite · Änderung der Hauptnavigation · Löschen bestehender Seiten · Überschreiben bestehender Inhalte. Alle WordPress-Änderungen zuerst als Draft.
