"""WP publish round 2 (approved 2026-06-15): Haushaltsauflösung content,
Reinigung-Abschnitt auf Service-Seiten, Startseite (Reinigung + Mannheim-Link).

Preserves all existing content (chatbot, WhatsApp button): new HTML is prepended
or appended, never replacing. Tests auth first. Voice du/ihr.
"""
from __future__ import annotations

import sys
import urllib.error

from wp_publish import _req, check_token

REINIGUNG_HTML = (
    "<h2>Reinigung nach Entrümpelung oder Umzug</h2>"
    "<p>Nach einer Entrümpelung bleibt oft mehr zurück als nur leerer Raum. Staub, Laufspuren, Klebereste, "
    "Kellerdreck oder Rückstände aus jahrelanger Nutzung können eine Wohnung, ein Büro oder ein Airbnb weiterhin unfertig wirken lassen.</p>"
    "<p>Johnson Services unterstützt dich auf Wunsch auch mit einer anschließenden Reinigung, damit die Räume wieder "
    "übergabefähig, vermietbar oder nutzbar sind.</p>"
    "<p><strong>Für wen sich das besonders lohnt:</strong> Vermieter, Hausverwaltungen, Makler, Airbnb-Hosts, "
    "Ferienwohnungsbetreiber, Gewerbekunden sowie Angehörige nach einer Haushaltsauflösung oder Wohnungsräumung.</p>"
    "<p><strong>So läuft es ab:</strong> kostenlose Besichtigung, feste Preiszusage vorab, Entrümpelung und Reinigung "
    "aus einer Hand, besenreine oder gereinigte Übergabe.</p>"
    "<p><strong>Jetzt kostenlose Besichtigung anfragen.</strong> WhatsApp/Telefon: +49 151 57731682</p>"
)

HOME_ADDON_HTML = REINIGUNG_HTML + (
    "<h2>Entrümpelung in deiner Stadt</h2>"
    "<p>Lokale Festpreis-Entrümpelung in deiner Region: "
    '<a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>, '
    '<a href="https://johnson-services.de/entruempelung/heidelberg/">Entrümpelung Heidelberg</a>. '
    'Mehr Leistungen: <a href="https://johnson-services.de/haushaltsaufloesungen/">Haushaltsauflösung</a> und '
    '<a href="https://johnson-services.de/umzuege/">Umzüge</a>.</p>'
)

HAUSHALT_HTML = (
    "<p><strong>Auf einen Blick:</strong> Haushaltsauflösung und Wohnungsauflösung in Mannheim, Heidelberg, "
    "Ludwigshafen und Umgebung. Einfühlsam, diskret und zum Festpreis nach kostenloser Besichtigung. Besenreine "
    "Übergabe, auf Wunsch inklusive Reinigung. Johnson Services, seit 2011.</p>"
    "<h2>5 Gründe für Johnson Services bei deiner Haushaltsauflösung</h2><ul>"
    "<li><strong>Einfühlsam und diskret</strong>, gerade bei Auflösungen im Trauerfall.</li>"
    "<li><strong>Festpreis</strong> nach kostenloser Besichtigung, keine Nachforderungen.</li>"
    "<li><strong>Wertanrechnung</strong>: Möbel, Schmuck und Antiquitäten bewerten wir und rechnen sie gegen.</li>"
    "<li><strong>Besenreine Übergabe</strong>, sofort vermietbar oder verkaufsbereit.</li>"
    "<li><strong>Alles aus einer Hand</strong>, auf Wunsch mit anschließender Reinigung.</li></ul>"
    "<h2>Was wir bei der Haushaltsauflösung übernehmen</h2><ul>"
    "<li>Komplette Räumung von Wohnung, Haus oder Gewerbe</li><li>Fachgerechte Entsorgung und Trennung</li>"
    "<li>Wertanrechnung verwertbarer Gegenstände</li><li>Besenreine Übergabe</li>"
    "<li>Auf Wunsch Reinigung der leeren Räume</li></ul>"
    "<h2>Festpreis-Übersicht: Haushaltsauflösung</h2>"
    "<table><thead><tr><th>Objekt</th><th>Geschätzter Festpreis</th></tr></thead><tbody>"
    "<tr><td>Keller bis 20 m²</td><td>ab 590 €</td></tr>"
    "<tr><td>1-Zimmer-Wohnung</td><td>ab 890 €</td></tr>"
    "<tr><td>2-3-Zimmer-Wohnung</td><td>ab 1.490 €</td></tr>"
    "<tr><td>4+ Zimmer-Wohnung / Haus</td><td>auf Anfrage</td></tr></tbody></table>"
    "<p>Hinweis: Die Wertanrechnung kann den Festpreis deutlich reduzieren. Der Endpreis steht nach der kostenlosen Besichtigung fest.</p>"
    + REINIGUNG_HTML +
    "<h2>Häufige Fragen zur Haushaltsauflösung</h2>"
    "<h3>Was kostet eine Haushaltsauflösung?</h3><p>Je nach Umfang und Wertanrechnung. Eine 2-3-Zimmer-Wohnung startet ab 1.490 €. Festpreis nach kostenloser Besichtigung.</p>"
    "<h3>Geht ihr bei einem Trauerfall einfühlsam vor?</h3><p>Ja, wir arbeiten ruhig, diskret und mit Respekt vor persönlichen Gegenständen.</p>"
    "<h3>Rechnet ihr Wertgegenstände an?</h3><p>Ja, Möbel, Elektronik, Schmuck und Antiquitäten bewerten wir vor Ort und rechnen sie transparent gegen.</p>"
    "<h3>Reinigt ihr die Räume danach?</h3><p>Auf Wunsch ja, damit die Übergabe stressfrei klappt.</p>"
    "<h2>Jetzt kostenloses Festpreis-Angebot anfordern</h2>"
    "<p>Du planst eine Haushaltsauflösung in der Region? Kostenlose Besichtigung, verbindlicher Festpreis. <strong>WhatsApp/Telefon: +49 151 57731682</strong></p>"
    '<p>Weitere Leistungen: <a href="https://johnson-services.de/entruempelung/">Entrümpelung</a>, '
    '<a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>, '
    '<a href="https://johnson-services.de/umzuege/">Umzüge</a>.</p><hr>'
)

HAUSHALT_META = "Haushaltsauflösung in Mannheim, Heidelberg, Ludwigshafen und Umgebung: einfühlsam, diskret, zum Festpreis. Besenreine Übergabe, auf Wunsch mit Reinigung. Jetzt anfragen."


def get_raw(kind: str, pid: int) -> str:
    cur = _req("GET", f"/{kind}/{pid}?context=edit&_fields=content")
    return (cur.get("content") or {}).get("raw", "") or ""


def main() -> int:
    try:
        me = check_token()
    except urllib.error.HTTPError as e:
        print(f"AUTH FEHLER {e.code}: {e.read().decode()[:140]}")
        return 1
    print(f"✅ Auth OK: {me.get('name')}")

    # 1) Haushaltsauflösung (page 252): neuen Content davor, Bestand (WhatsApp-Button) erhalten
    raw = get_raw("pages", 252)
    r = _req("POST", "/pages/252", {"content": HAUSHALT_HTML + "\n" + raw, "excerpt": HAUSHALT_META, "status": "publish"})
    print(f"Haushaltsauflösung (252): {r.get('status')}  {r.get('link')}")

    # 2) Reinigung-Abschnitt auf Entrümpelung-Hub (page 441) anhängen
    raw = get_raw("pages", 441)
    add = "" if "Reinigung nach Entrümpelung oder Umzug" in raw else "\n" + REINIGUNG_HTML
    r = _req("POST", "/pages/441", {"content": raw + add, "status": "publish"})
    print(f"Entrümpelung-Hub (441): {r.get('status')}  Reinigung {'ergänzt' if add else 'schon vorhanden'}")

    # 3) Startseite (page 6): Reinigung + lokale Links anhängen, Bestand (Chatbot) erhalten
    raw = get_raw("pages", 6)
    add = "" if "Entrümpelung in deiner Stadt" in raw else "\n" + HOME_ADDON_HTML
    r = _req("POST", "/pages/6", {"content": raw + add, "status": "publish"})
    print(f"Startseite (6): {r.get('status')}  {'ergänzt' if add else 'schon vorhanden'}  (Chatbot erhalten: {'ja' if 'VG_CONFIG' in raw else 'pruefen'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
