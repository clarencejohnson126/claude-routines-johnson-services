# Agentic Johnson Services — Growth Engine

Spec-driven AI Growth Engine für **Johnson Services** (lokaler Entrümpelungs-, Haushaltsauflösungs-, Umzugs- und Reinigungs-Dienstleister, Region Rhein-Neckar: Mannheim, Heidelberg, Ludwigshafen u. a.).

**Ziel:** nicht mehr Content, sondern systematisch **qualifizierte lokale Nachfrage** — über organische SEO, lokale Landingpages, B2B-Outreach, Content-Authority und eine manuelle TikTok/Motion-Video-Pipeline.

Quelle: `Johnson Services Growth Engine Spec.pdf` (23 Seiten). Angelegt 2026-06-14.

## Struktur

| Ordner | Inhalt |
|--------|--------|
| `00_constitution/` | Arbeitsprinzipien, Sicherheitsregeln, Approval-Gates, belegte Geschäftsfakten |
| `01_specs/` | 5 Agent-Specs (SEO, B2B-Outreach, WordPress-Landingpages, Content-Authority, TikTok/Motion) |
| `02_clarifications/` | Offene Fragen, fehlende Credentials, Zugriffs-Checkliste |
| `03_plans/` | Umsetzungspläne je Agent |
| `04_tasks/` | Backlog, Sprint-Tasks, wiederkehrende Aufgaben |
| `05_implementation/` | Skripte, Workflows, WordPress-Drafts, Outreach-Templates, Content-Generatoren |
| `06_validation/` | Acceptance Criteria + Validierungs-Checklisten |
| `07_outputs/` | Reports, Lead-Listen, E-Mail-Drafts, Landingpage-Drafts, Blog/Social-Drafts, Video-Pläne |

## Die 5 Agenten

1. **SEO Intelligence Agent** — warum Johnson organisch unsichtbar ist + konkrete SEO-Aktionen.
2. **B2B Leadfinding & Outreach Agent** — 2×/Woche je 20 qualifizierte B2B-Leads + personalisierte Outreach-Mails (nach Freigabe).
3. **WordPress Local Landing Page Agent** — lokale Money-Pages + „Reinigung nach Entrümpelung"-Abschnitt als Drafts.
4. **Content Authority Agent** — aus einem Thema: Blog + Social + GBP + interne Links (bestehende FB/IG-Automation NICHT beschädigen).
5. **TikTok / Motion Video Pipeline Agent** — 10-Wochen-Pipeline für manuell umsetzbare Short Videos.

## Sicherheit & Grenzen (Kurzfassung)

- Secrets nur in `.env` (chmod 600, gitignored) — nie in Markdown/Logs/Git.
- Nichts auf WordPress veröffentlichen und keine E-Mail senden ohne Freigabe.
- Bestehende Automation in `../Graph-Growth-Agents/automation/johnson_*` und alle `com.johnson.*` launchd-Jobs bleiben unangetastet.
- Keine erfundenen Daten. Reale Analysen mit Quelle + Zeitstempel. Wenn etwas nur simuliert ist, wird es als simuliert gekennzeichnet.

Details: `00_constitution/`. Aktueller Stand & nächste Schritte: `04_tasks/sprint_01_tasks.md`.
