# Initial SEO Audit — Johnson Services

**Quellen:**
- **Live Google Search Console** (sc-domain:johnson-services.de, letzte 28 Tage) via `05_implementation/scripts/gsc_audit.py` — Rohdaten: `_gsc_raw_28d.txt`
- **Live WordPress REST Crawl** (`wp_client.py audit`) — Rohdaten: `_wp_audit_raw.json`
- **Wettbewerbs-/Keyword-Recherche** `../../Johnson-Services/research/`

**Zeitstempel:** 2026-06-14 (GSC 28-Tage-Fenster, WP-Crawl 20:02Z). **Konto mit GSC-Zugriff:** `thaliajadedeyes@gmail.com` (Properties: `sc-domain:johnson-services.de`, `https://johnson-services.de/`, `sc-domain:rebelzai.com`).
**Datenstatus:** GSC + WP = ECHT. GA4 = pending (Property-ID fehlt; API + Token bereit).

---

## 1. Aktuelle Sichtbarkeit (echte GSC-Zahlen, 28 Tage)

Die Domain ist sichtbar (Hunderte Impressionen auf relevante lokale Keywords), aber **Klicks sind sehr niedrig** — die meisten guten Keywords stehen auf **Seite 2–4**. Klar-Bild: viel latente Nachfrage, schwache Positionen + schwache CTR.

**Top-Seiten nach Impressionen (real):**

| Seite | Impr | Position | Klicks | CTR | Lesart |
|-------|-----:|:--------:|:------:|----:|--------|
| `/umzuege/` | 456 | 44.7 | 0 | 0% | meiste Nachfrage, schlechteste Position → größtes Potenzial |
| `/` (Startseite) | 352 | 9.7 | 6 | 1.7% | Haupt-Traffic; CTR ausbaufähig |
| `/haushaltsaufloesungen/` | 289 | 46.3 | 0 | 0% | viel Nachfrage, Seite 4–5 |
| `/entruempelung/` | 220 | 47.3 | 0 | 0% | Hub-Seite schlecht positioniert |
| `/entruempelung/heidelberg/` | 218 | 18.9 | 0 | 0% | **Quick-Win**: Seite 2, viel Nachfrage |
| `/entruempelung/mannheim/` | 163 | 21.1 | 0 | 0% | **Quick-Win**: Seite 2 |
| `/haushaltsaufloesung/haushaltsauf…` | 119 | 35.5 | 0 | 0% | Dublette zu `/haushaltsaufloesungen/`? |
| `/entruempelung/entruempelung-mann…` | 108 | 7.6 | 1 | 0.9% | rankt gut, CTR schwach |
| `/entruempelung/beste-entruempelun…` | 60 | 22.8 | 1 | 1.7% | Blog-/Ratgeber-Seite |

**Top-Suchanfragen (real, Auswahl):**

| Query | Impr | Position | Lesart |
|-------|-----:|:--------:|--------|
| entrümpelung heidelberg | 103 | 19.4 | starke Nachfrage, Seite 2 |
| entrümpelung in heidelberg | 29 | 24.8 | dito |
| entrümpelung mannheim kosten | 14 | 8.4 | rankt gut, **Preis-Intent** (CTR 7.1%) |
| entrümpelung heidelberg mannheim | 11 | 7.2 | rankt gut |
| entrümpelung heidelberg walldorf | 11 | 15.3 | Seite 2 |
| entrümpelung einer messiewohnung mannheim | 7 | 12.6 | Messie-Nische, lokal |

## 2. Technische SEO-Probleme

| Problem | Beleg (real) | Priorität |
|---------|--------------|:---------:|
| **Keyword-Kannibalisierung Mannheim** | Mehrere überlappende URLs zu „Entrümpelung Mannheim": `/entruempelung/mannheim/` (Pos 21.1) **und** `/entruempelung/entruempelung-mann…` (Pos 7.6) **plus** Top-Level-Tippfehler-Slug `entruempelungen-mannhein` (WP-Crawl) | 🔴 hoch |
| **Mögliche Haushaltsauflösung-Dublette** | `/haushaltsaufloesungen/` (Pos 46.3, 289 Impr) **und** `/haushaltsaufloesung/haushaltsauf…` (Pos 35.5, 119 Impr) | 🔴 hoch |
| **Tippfehler-Slug** | Top-Level-Seite `entruempelungen-mannhein` (statt „mannheim") | 🟡 mittel |
| **Schwache Positionen trotz Nachfrage** | `/umzuege/` (456 Impr @ 44.7), `/haushaltsaufloesungen/` (289 @ 46.3), `/entruempelung/` (220 @ 47.3) | 🔴 hoch |
| **Geografisches Rauschen** | Rankings für weit entfernte Orte (Niedersachsen: Affinghausen, Balje, Heeslingen, Herzlake…) — Content zu breit gestreut, Region verwässert | 🟢 niedrig |

> Korrektur zum ersten Entwurf: Lokale Seiten **existieren** (verschachtelt unter `/entruempelung/`: Heidelberg, Mannheim, Rüsselsheim). Der erste WP-REST-Lauf erfasste nur Top-Level-Seiten und übersah sie. Die echte Lücke ist also nicht „keine lokalen Seiten", sondern „lokale Seiten hängen auf Seite 2–4 fest".

## 3. Quick Wins (Position 5–20, viel Nachfrage)

1. 🔴 **`/entruempelung/heidelberg/`** (Pos 18.9, 218 Impr) auf Seite 1 bringen — größter Hebel. Query „entrümpelung heidelberg" allein: 103 Impr.
2. 🔴 **`/entruempelung/mannheim/`** (Pos 21.1, 163 Impr) — Kannibalisierung mit den anderen Mannheim-URLs auflösen, Signale bündeln.
3. 🟡 **Startseite-CTR** (Pos 9.7, nur 1.7% CTR) — Title/Meta auf Klick optimieren.
4. 🟡 **„entrümpelung mannheim kosten"** (Pos 8.4, Preis-Intent) — Preis-/Festpreis-Snippet + FAQ schärfen.

## 4. Schwache Seiten mit hoher Nachfrage (Content/Optimierung nötig)

- `/umzuege/` (456 Impr, Pos 44.7) — meiste Impressionen, Seite 4–5: Content-Tiefe, lokale Keywords, interne Links.
- `/haushaltsaufloesungen/` (289 Impr, Pos 46.3) — plus Dubletten-Klärung.
- `/entruempelung/` (220 Impr, Pos 47.3) — Hub-Seite stärken.

## 5. Lokale Chancen

- Mannheim-URLs konsolidieren (eine starke Seite, 301 + Canonical) → Quick-Win.
- Heidelberg-Seite optimieren (Title/H1/Content/interne Links) → Seite-1-Kandidat.
- Reinigung-nach-Entrümpelung als Cross-Sell-Abschnitt (Draft: `../landing_page_drafts/`).
- Geo-Fokus auf Rhein-Neckar schärfen, irrelevante Fernorte nicht weiter ausbauen.

## 6. GA4 — live (Property 536903926 = johnson-services.de, verifiziert via hostName)

Echte Zahlen (28 Tage): **10 Sitzungen, 6 Nutzer, alle Kanal „Direct" — 0 Organic-Search-Sitzungen.**
Das deckt sich exakt mit GSC: viele Impressionen, kaum Klicks, Positionen auf Seite 2–4. **Organisch ist die Seite faktisch unsichtbar.** Genau die Quick-Wins (Heidelberg, Umzug, Mannheim-Konsolidierung) sollen Organic von ~0 auf echten Traffic heben.
Hinweis: sehr kleine Fallzahlen + GA4/GSC-Kanal-Differenz (GSC zeigt Such-Klicks, GA4 zeigt 0 Organic) deuten auf mögliche Consent-/Cookie-Banner-Lücken im Tracking — bei Gelegenheit prüfen. Business Profile (GBP) optional via `business.manage`-Scope.

## 7. Priorisierte Maßnahmen

1. 🔴 Mannheim-URLs + Haushaltsauflösung-Dubletten konsolidieren (301/Canonical). *(Approval: Live-WP)*
2. 🔴 `/entruempelung/heidelberg/` + `/entruempelung/mannheim/` on-page optimieren (Title/H1/Content/interne Links).
3. 🔴 `/umzuege/` + `/haushaltsaufloesungen/` Content-Tiefe ausbauen.
4. 🟡 Startseiten-Title/Meta für CTR; Preis-Intent „… kosten" bedienen.
5. 🟡 Reinigung-Abschnitt als Draft einpflegen.
6. 🟢 GA4-Property-ID nachreichen → Conversions ergänzen.

→ Tasks gespiegelt in `../../04_tasks/task_backlog.md`.
