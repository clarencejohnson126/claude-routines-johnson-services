# Ad-Analyse Johnson Services — warum die alten Anzeigen floppten

**Quelle:** Live Meta Marketing API (Johnson-Konto, letzte 90 Tage) + Memory/Kampagnen-Daten. Stand 2026-06-15.

## Echte Meta-Zahlen (90 Tage)
| Kampagne | Spend | Impr | Klicks | CTR | Conversions/Leads |
|----------|------:|-----:|------:|----:|------------------|
| JS Entrümpelung WA Begrüßung | €80,05 | 20.348 | 581 | 2,86% | **0** (4.021 Video-Views, 4.381 Post-Engagement) |
| JS Entrümpelung & Umzug WhatsApp | €23,67 | 8.787 | 88 | 1,00% | **0** |
| JS Top 2 Winners wa.me | €10,26 | 3.459 | 54 | 1,56% | **0** (25 Landing-Views) |
| JS WhatsApp Direct | €0,65 | 479 | 5 | 1,04% | **0** |
| **Summe** | **~€114,6** | **~33.000** | **~728** | **~1,9%** | **0 messbare Leads** |

## Diagnose (ehrlich)
1. **CTR war ok (1–2,9%)** — Creative/Targeting bekamen Aufmerksamkeit. Das war NICHT das Problem.
2. **Der Funnel NACH dem Klick ist kollabiert.** Beispiel große Kampagne: 338 Link-Klicks → nur **60 Landing-Page-Views** (82% gehen unterwegs verloren) → **0 Conversions**. Das ist ein kaputter/lahmer wa.me-Redirect oder Tracking-Loch.
3. **Keine Conversion-Messung.** wa.me-Links sind für Meta nicht trackbar (das Gespräch passiert off-platform auf WhatsApp). Ergebnis: Meta zeigt 0, du fliegst blind. Was man nicht misst, kann man nicht optimieren.
4. **Viel „Vanity-Engagement"** (4.021 Video-Views, 4.381 Post-Engagement) aber 0 Geschäft → die Anzeige wurde geschaut/geliked, nicht gekauft. Dazu **6× messaging_block** (Leute haben das Anschreiben blockiert) = Spam-Signal.
5. **Reale Folge:** „nur Job-Sucher-Anrufe" → Placement/Audience zog die falschen Leute (Jobsuchende, Engagement-Junkies), nicht zahlende Kunden.
6. **Google Search-Ads:** liefen Apr–Mai faktisch nicht — der `contains_eu_political_advertising`-Flag-Bug blockierte die Auslieferung still (Memory). Also „gefloppt", weil sie kaum ausgespielt wurden.

## Kernsatz
€115 ausgegeben, 0 messbare Leads — **nicht wegen Pech, sondern weil es keinen funktionierenden, messbaren Conversion-Weg gab.** Mehr Budget ohne Fix = mehr verbranntes Geld.

## Schlanker Neustart (nur mit Budget, klein + messbar)
1. **Tracking ZUERST fixen.** Optionen:
   - **Native Click-to-WhatsApp** (Objective WHATSAPP, `destination_type=WHATSAPP`) → Meta trackt die Gespräche. NIE wieder nackte wa.me-Links ohne Tracking.
   - ODER **Meta Lead-Formular** (Instant Form) → Lead bleibt auf Plattform, messbar.
2. **Google: Local Services Ads (LSA)** statt Search. Pay-per-Lead, Google-geprüft („Google Garantiert"), steht ganz oben bei lokalen Diensten. Viel besserer Fit + du zahlst nur für echte Leads. Falls doch Search: EU-Political-Flag korrekt setzen.
3. **Targeting verengen:** Objective „Leads", Jobsuchende ausschließen, enge Geo (Mannheim-Kern), Intent statt breite Reichweite.
4. **Kleiner Test** (€5–10/Tag, 1–2 Wochen). Bewertung NUR nach **Kosten pro Lead**, nicht nach Klicks/Engagement. Kein Lead → killen.
5. **Landing/Funnel prüfen:** der 82%-Drop Klick→Landing deutet auf langsame/kaputte Weiterleitung. Schnelle Ladezeit + ein einziger klarer CTA.

**Empfehlung bei knapper Kasse:** Erst Tracking + LSA-Setup, dann €5–10/Tag-Test. Bis dahin sind Outreach (läuft, kostenlos) + GBP/Reviews die sichereren Lead-Quellen.
