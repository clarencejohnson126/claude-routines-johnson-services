# Spec 004 — Content Authority Agent

## Intent

Bestehende Facebook / Instagram Automation erweitern und Content so planen, dass SEO, Trust und lokale Sichtbarkeit unterstützt werden.

## Existing Context — NICHT beschädigen

Es existiert bereits Automation, die Content für Johnson Services erstellt/postet:

| Modul | Pfad | Zeitplan |
|-------|------|----------|
| FB-Poster Entrümpelung | `../Graph-Growth-Agents/automation/johnson_entruempelung/poster.py` | launchd `com.johnson.entruempelung.poster`, tgl. 10:00 |
| FB-Poster Innenausbau | `../Graph-Growth-Agents/automation/johnson_innenausbau/poster.py` | launchd `com.johnson.innenausbau.poster`, tgl. 10:00 |
| WordPress Autoblog | `../Graph-Growth-Agents/automation/johnson_autoblog/autoblog.py` | launchd `com.johnson.autoblog`, Mo 09:00 |

**Diese Module, ihre `queue.json`/`topics.json` und alle `com.johnson.*` launchd-Jobs werden NICHT verändert.** Der Content-Agent liefert nur zusätzliche Drafts in `07_outputs/`.

## Scope — aus einem Thema erzeugen

Blogartikel · Facebook Post · Instagram Post · Google-Business-Profile-Post (falls Zugriff) · TikTok/Short-Video-Idee · interne Linkvorschläge · FAQ-Snippets · CTA-Varianten.

## Themencluster

Entrümpelung Mannheim · Haushaltsauflösung Mannheim · Wohnungsauflösung nach Todesfall · Keller entrümpeln · Umzug Mannheim · Entrümpelung für Hausverwaltungen · Entrümpelung für Makler · Reinigung nach Entrümpelung · Reinigung für Airbnb-Hosts · Wohnung übergabefähig machen.

## Workflow

1. SEO-Agent liefert Thema oder Keyword
2. Content-Agent erstellt Content-Paket
3. WordPress-Draft vorbereiten
4. Social-Posts speichern
5. Google-Business-Profile-Post vorbereiten
6. Interne Links vorschlagen
7. Nutzerfreigabe einholen, falls Veröffentlichung geplant

## Output

`07_outputs/blog_drafts/` · `07_outputs/social_posts/` · `05_implementation/content_generators/`

## Quality Rules

Kein generischer KI-Text · lokal schreiben · klare Dienstleistung · klare Zielgruppe · keine übertriebenen Versprechen · seriöser Ton · menschlich, direkt, vertrauenswürdig. Ton: Website/Social „du/ihr" (Design-System). Keine erfundenen Zahlen/Testimonials. Keine Em-Dashes.
