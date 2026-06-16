# WordPress Drafts

Aktive Inhalts-Drafts: `../../07_outputs/landing_page_drafts/` und `../../07_outputs/blog_drafts/`.

## Reuse (NICHT neu bauen)
- WP-REST Lesen: `../scripts/wp_client.py` (read-only)
- WP-REST Schreiben (Draft/Publish-Pattern, Basic-Auth): `../../../Graph-Growth-Agents/automation/johnson_autoblog/autoblog.py` (`wp_post`)
- Übersichtsseiten aktualisieren: `../../../Graph-Growth-Agents/automation/johnson_autoblog/update_ratgeber.py`
- Kategorien: 3=Entrümpelung, 4=Haushaltsauflösung, 5=Umzug

## Gate
Alles zuerst als `status=draft`. Live-`publish`, Startseiten- oder Navigationsänderung nur nach Freigabe.
