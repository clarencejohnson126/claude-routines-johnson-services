"""Create a VISIBLE dedicated Reinigung page as a classic post (no Elementor).

The site is Elementor-based; Elementor pages ignore post_content. Classic posts
(like /entruempelung/ruesselsheim/, ludwigshafen, keller) DO render post_content,
so the cleaning content goes here as a real, findable page. du/ihr.
URL: /entruempelung/reinigung-nach-entruempelung-mannheim/
"""
from __future__ import annotations

import sys
import urllib.error

from wp_client import get
from wp_publish import _req, check_token

SLUG = "reinigung-nach-entruempelung-mannheim"
TITLE = "Reinigung nach Entrümpelung in Mannheim"
META = ("Reinigung nach Entrümpelung oder Umzug in Mannheim und Umgebung: damit Räume wieder übergabefähig, "
        "vermietbar oder nutzbar sind. Festpreis, kostenlose Besichtigung. Jetzt anfragen.")
HTML = (
    "<p><strong>Auf einen Blick:</strong> Reinigung im Anschluss an Entrümpelung, Haushaltsauflösung oder Umzug in "
    "Mannheim und Umgebung. Damit deine Räume wieder übergabefähig, vermietbar oder nutzbar sind. Festpreis nach "
    "kostenloser Besichtigung. Johnson Services, seit 2011.</p>"
    "<h2>Warum Reinigung nach der Entrümpelung?</h2>"
    "<p>Nach einer Entrümpelung bleibt oft mehr zurück als nur leerer Raum. Staub, Laufspuren, Klebereste, Kellerdreck "
    "oder Rückstände aus jahrelanger Nutzung lassen eine Wohnung, ein Büro oder ein Airbnb weiterhin unfertig wirken. "
    "Erst die Reinigung macht die Räume wirklich fertig.</p>"
    "<h2>Was wir übernehmen</h2><ul>"
    "<li>Grundreinigung der leeren Räume, Böden und Oberflächen</li>"
    "<li>Entfernen von Klebe- und Teppichresten, soweit möglich</li>"
    "<li>Fenster, Fensterbänke und Sanitärbereiche</li>"
    "<li>Keller, Dachboden und Nebenräume auf Wunsch</li></ul>"
    "<h2>Für wen sich das besonders lohnt</h2>"
    "<p>Vermieter, Hausverwaltungen, Makler, Airbnb-Hosts, Ferienwohnungsbetreiber, Gewerbekunden sowie Angehörige "
    "nach einer Haushaltsauflösung oder Wohnungsräumung.</p>"
    "<h2>So läuft es ab</h2>"
    "<p>Kostenlose Besichtigung, feste Preiszusage vorab, Entrümpelung und Reinigung aus einer Hand, besenreine oder "
    "gereinigte Übergabe. Du sagst, was du brauchst, wir kümmern uns um den Rest.</p>"
    "<h2>Häufige Fragen</h2>"
    "<h3>Bietet ihr Reinigung auch ohne Entrümpelung an?</h3>"
    "<p>Der Schwerpunkt liegt auf Reinigung im Anschluss an eine Entrümpelung, Haushaltsauflösung oder einen Umzug. "
    "Sprich uns für deinen Fall einfach an.</p>"
    "<h3>Was kostet die Reinigung nach einer Entrümpelung?</h3>"
    "<p>Das hängt von Größe und Zustand der Räume ab. Du bekommst nach einer kostenlosen Besichtigung eine feste "
    "Preiszusage, ohne Nachforderungen.</p>"
    "<h3>In welchem Gebiet seid ihr aktiv?</h3>"
    "<p>In Mannheim und Umgebung, dazu Heidelberg, Ludwigshafen und die Rhein-Neckar-Region.</p>"
    "<h2>Jetzt kostenlose Besichtigung anfragen</h2>"
    "<p>Du willst Räume nach einer Entrümpelung oder einem Umzug wieder übergabefertig machen? "
    "<strong>WhatsApp/Telefon: +49 151 57731682</strong></p>"
    '<p>Weitere Leistungen: <a href="https://johnson-services.de/entruempelung/">Entrümpelung</a>, '
    '<a href="https://johnson-services.de/haushaltsaufloesungen/">Haushaltsauflösung</a>, '
    '<a href="https://johnson-services.de/umzuege/">Umzüge</a>.</p>'
)


def main() -> int:
    try:
        me = check_token()
    except urllib.error.HTTPError as e:
        print(f"AUTH FEHLER {e.code}: {e.read().decode()[:140]}")
        return 1
    print(f"✅ Auth OK: {me.get('name')}")
    cat = get("/categories", slug="entruempelung", _fields="id")[0]["id"]
    existing = get("/posts", slug=SLUG, status="publish,draft,pending,future,private", _fields="id")
    payload = {"title": TITLE, "content": HTML, "excerpt": META, "status": "publish", "categories": [cat], "slug": SLUG}
    if existing:
        r = _req("POST", f"/posts/{existing[0]['id']}", payload)
        print("aktualisiert:", r.get("link"), r.get("status"))
    else:
        r = _req("POST", "/posts", payload)
        print("erstellt:", r.get("link"), r.get("status"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
