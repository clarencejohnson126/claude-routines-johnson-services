# Telefonnummer site-weit tauschen — Better Search Replace

**Problem (geprüft 2026-06-15):** Falsche/private Nummer **+49 162 1811 123** statt Kundennummer +49 151 57731682. Schadet lokalem SEO (NAP-Inkonsistenz), legt die Privatnummer offen, schickt Anrufer auf die falsche Nummer.

## Stand 2026-06-15
- **✅ ERLEDIGT per REST-API (Token):** 14 Standortseiten-Inhalte korrigiert (Anruf-Buttons im Body) — IDs 444, 443, 441, 412, 411, 410, 409, 408, 407, 406, 405, 404, 403, 353. Live verifiziert.
- **❌ OFFEN (braucht wp-admin / BSR):** globaler Header/Footer (Oxygen-Vorlage, ~4× sichtbar + 2-3× `tel:` auf JEDER Seite) + Rank-Math-Schema (`telephone`). Beide per REST nicht beschreibbar. BSR fängt beides (und prüft die Bodies gleich mit).

**Warum nicht automatisch:** wp-admin ist mit HTTP-Basic-Auth geschützt, der Automations-Browser kommt nicht rein; die Nummer liegt in geschützten Elementor-/Oxygen-Daten + Rank-Math-Optionen, die die REST-API nicht schreiben kann. „Better Search Replace" ist aber installiert und erledigt das DB-weit in 2 Minuten.

## Schritte (in deinem normalen Browser, wo du eingeloggt bist)

1. wp-admin → **Werkzeuge → Better Search Replace**.
2. Reiter **„Suchen/Ersetzen"**.
3. Bei **„Tabellen auswählen"**: ALLE Tabellen markieren (Strg/Cmd+A in der Liste).
4. **Erst Probelauf:** Häkchen bei **„Als Probelauf ausführen?"** lassen → „Suchen/Ersetzen ausführen" → zeigt, wie viele Treffer ersetzt würden.
5. Dann **Häkchen entfernen** und für jedes Paar real ausführen:

| Suchen nach | Ersetzen durch |
|---|---|
| `+491621811123` | `+4915157731682` |
| `+49 162 1811 123` | `+49 151 57731682` |
| `01621811123` | `015157731682` |

6. **Cache leeren**, sonst zeigt die Live-Seite die alte Nummer:
   - Elementor → **Werkzeuge → „CSS & Daten neu generieren"**
   - Raidboxes-Cache leeren (Raidboxes-Leiste oben oder im Dashboard)

7. Sag mir Bescheid → ich prüfe live per curl, dass die alte Nummer 0× und die neue überall steht (inkl. `tel:`-Links + Schema).

## Hinweis: WhatsApp-Button-Plugin
Das eigene Plugin „Johnson Services WhatsApp Button" nutzt bereits die richtige Nummer (+4915157731682). Falls der doppelte WhatsApp-Button stört: dessen Einstellungen liegen unter wp-admin (eigener Menüpunkt) — sag Bescheid, dann sehe ich mir das an, sobald wp-admin erreichbar ist.
