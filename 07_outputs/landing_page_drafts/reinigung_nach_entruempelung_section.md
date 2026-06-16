# Draft: Abschnitt „Reinigung nach Entrümpelung oder Umzug"

**Status:** Entwurf. Keine Live-Veröffentlichung ohne Freigabe (Approval-Gate).
**Platzierung (Nutzer 2026-06-14):** Startseite + relevante Leistungsseiten (`entruempelung`, `haushaltsaufloesungen`, `umzuege`). **Kein** eigener Navigations-Reiter.
**Ton:** du/ihr (Website-Design-System). Keine erfundenen Zahlen/Jahre, keine Em-Dashes.
**Ziel:** Johnson Services nicht nur als Entrümpler, sondern als Dienstleister positionieren, der Räume wieder übergabefähig, vermietbar und nutzbar macht.

---

## Variante A — kurz (für die Startseite)

> ### Reinigung nach Entrümpelung oder Umzug
>
> Nach einer Entrümpelung bleibt oft mehr zurück als nur leerer Raum. Staub, Laufspuren, Klebereste oder Kellerdreck lassen eine Wohnung unfertig wirken. Auf Wunsch reinigen wir im Anschluss, damit deine Räume wieder übergabefähig, vermietbar oder nutzbar sind.
>
> Besonders sinnvoll für Vermieter, Hausverwaltungen, Makler, Airbnb-Hosts und Angehörige nach einer Haushaltsauflösung.
>
> **[Kostenlose Besichtigung anfragen]** · WhatsApp +49 151 57731682

---

## Variante B — ausführlich (für Leistungsseiten)

> ### Reinigung nach Entrümpelung oder Umzug
>
> Nach einer Entrümpelung bleibt oft mehr zurück als nur leerer Raum. Staub, Laufspuren, Klebereste, Kellerdreck oder Rückstände aus jahrelanger Nutzung können eine Wohnung, ein Büro oder ein Airbnb weiterhin unfertig wirken lassen.
>
> Johnson Services unterstützt dich auf Wunsch auch mit einer anschließenden Reinigung, damit die Räume wieder übergabefähig, vermietbar oder nutzbar sind.
>
> **Für wen sich das besonders lohnt:** Vermieter, Hausverwaltungen, Makler, Airbnb-Hosts, Ferienwohnungsbetreiber, Gewerbekunden sowie Angehörige nach einer Haushaltsauflösung oder Wohnungsräumung.
>
> **So läuft es ab:** kostenlose Besichtigung, feste Preiszusage vorab, Entrümpelung und Reinigung aus einer Hand, besenreine oder gereinigte Übergabe.
>
> **[Jetzt kostenlose Besichtigung anfragen]** · WhatsApp +49 151 57731682

### FAQ (für FAQ-Schema)

**Bietet ihr Reinigung auch ohne Entrümpelung an?**
Der Schwerpunkt liegt auf Reinigung im Anschluss an eine Entrümpelung, Haushaltsauflösung oder einen Umzug, damit die Räume sofort übergabefähig sind. Sprich uns für deinen Fall einfach an.

**Was kostet die Reinigung nach einer Entrümpelung?**
Das hängt von Größe und Zustand der Räume ab. Du bekommst nach einer kostenlosen Besichtigung eine feste Preiszusage, ohne Nachforderungen.

**In welchem Gebiet seid ihr aktiv?**
In Mannheim und Umgebung, dazu Heidelberg, Ludwigshafen und die Rhein-Neckar-Region.

### Interne Links (Vorschlag)
→ Entrümpelung · Haushaltsauflösung · Umzüge · (geplant) Reinigung nach Entrümpelung Mannheim

### Schema-Markup (JSON-LD, Vorschlag für die Service-Seite)
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Reinigung nach Entrümpelung oder Umzug",
  "provider": {"@type": "LocalBusiness", "name": "Johnson Services", "areaServed": "Mannheim, Heidelberg, Ludwigshafen, Rhein-Neckar"},
  "areaServed": ["Mannheim", "Heidelberg", "Ludwigshafen"],
  "description": "Reinigung im Anschluss an Entrümpelung, Haushaltsauflösung oder Umzug, damit Räume wieder übergabefähig, vermietbar oder nutzbar sind."
}
```

---

## Umsetzungs-Hinweis (für Agent 003)

Einpflegen als Draft via WP REST (read/Draft-Pattern aus `autoblog.py`). Auf der Startseite Variante A als Abschnitt; auf `entruempelung` / `haushaltsaufloesungen` / `umzuege` Variante B inkl. FAQ-Schema. Vor Live-Schaltung Freigabe einholen.
