# Plan — WordPress Local Landing Page Agent

Basis: echter WP-Crawl (14 Seiten/24 Posts) + `../07_outputs/landing_page_drafts/reinigung_nach_entruempelung_section.md`.

## Audit-Ergebnis → Matrix (korrigiert mit echten WP+GSC-Daten 2026-06-14)
| Seite | Realer Stand | Aktion | Draft |
|-------|-------------|--------|-------|
| `/entruempelung/heidelberg/` (id 201) | existiert, **LEER** (Pos 18.9, 218 Impr) | befüllen | ✅ `../07_outputs/landing_page_drafts/draft_entruempelung_heidelberg.md` |
| `/entruempelung/mannheim/` (id 256) | existiert, **LEER** (Pos 21.1, 163 Impr) | befüllen + konsolidieren | ✅ `draft_entruempelung_mannheim.md` |
| `/umzuege/` (id 266) | dünn, nur Chatbot (Pos 44.7, 456 Impr) | Content ausbauen | ✅ `draft_umzuege.md` |
| `/entruempelung/ruesselsheim/` (id 409) | gut (520 W, 5 H2, Festpreis) | **Vorlage/Template** | — |
| `/haushaltsaufloesungen/` (id 252) | dünn (79 W, keine Meta) | später ausbauen | — |
| Startseite (id 6, Slug `entruempelungen-mannhein`) | = Startseite, **kein** Duplikat | intern auf id 256 verlinken | — |
| keller / reinigung / ludwigshafen / darmstadt / karlsruhe | existieren nicht | später nach GSC-Nachfrage | reinigung: Abschnitt vorhanden |

**Template:** Neue lokale Seiten folgen der funktionierenden Rüsselsheim-Struktur (TL;DR → 5 Gründe → Stadtteile → Festpreis-Übersicht → FAQ → CTA). Echte Festpreise: Keller bis 20 m² ab 590 €, 1-Zi ab 890 €, 2-3-Zi ab 1.490 €.
**Offene Stilfrage:** Rüsselsheim nutzt „Sie", die Drafts sind in „du/ihr" (Website-Regel) — Nutzer entscheidet über Section-Konsistenz.

## Reihenfolge (Spec)
1. Audit ✅ → 2. Matrix ✅ → 3. Priorisierung → 4. Drafts → 5. Freigabe → 6. Veröffentlichung.

## Reinigung (Nutzer: Startseite + Service-Seiten)
Variante A auf Startseite, Variante B + FAQ-Schema auf `entruempelung`/`haushaltsaufloesungen`/`umzuege`. Alles als Draft via WP REST (Pattern aus `autoblog.py`).

## Approval-Gates
Veröffentlichung, Startseiten-/Navigationsänderung, Löschen/Überschreiben. Immer zuerst Draft.
