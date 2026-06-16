# Recurring Tasks (Spec-Kapitel 10)

> Status: Recurring-Automation seit 2026-06-15 als launchd-Jobs aktiv (nach Freigabe).
> - `com.johnson.growth.seoreport` — **Mo 07:00**, `weekly_seo_report.py` (GSC+GA4 → Report + Telegram).
> - `com.johnson.growth.outreach` — **Di + Do 09:00**, `leadfinding_batch.py 20` (20 neue Leads + Drafts + Telegram; Versand bleibt manuell/Gate).
> Bestehende FB/IG-Routine (`../../Graph-Growth-Agents/automation/johnson_*`) unberührt.

## Wöchentlich
- SEO-Report aktualisieren (`gsc_audit.py`, sobald freigeschaltet).
- 2 Outreach-Läufe vorbereiten oder (nach Freigabe) durchführen.
- 40 neue B2B-Leads qualifizieren (20/Lauf).
- WordPress-Chancen prüfen (neue Slugs/Seiten).
- 1 Blogartikel als Draft vorbereiten.
- 1 Videoidee aus der Pipeline bereitstellen.

## Alle 4 Tage
- Bestehende Facebook/Instagram-Routine (`../../Graph-Growth-Agents/automation/johnson_*`) weiterlaufen lassen. **Nicht verändern**, nur beobachten (Healthcheck `com.johnson.healthcheck`).

## Monatlich
- Rankingentwicklung prüfen.
- Top-Keywords prüfen.
- Beste Content-Pieces identifizieren.
- Outreach-Antwortrate prüfen.
- Landingpage-Performance prüfen.
- Nächste Prioritäten ableiten.
