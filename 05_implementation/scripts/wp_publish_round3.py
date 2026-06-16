"""WP publish round 3 — neue lokale Money-Pages (Landing-Page-Matrix, Agent 003).

Erstellt /entruempelung/ludwigshafen/ und /entruempelung/keller-entruempeln-mannheim/
als Posts in Kategorie 'entruempelung' (Permalink /%category%/%postname%/).
Idempotent: existiert der Slug, wird aktualisiert statt doppelt angelegt.
du/ihr, echte Festpreise. Tests auth first.
"""
from __future__ import annotations

import sys
import urllib.error

from wp_client import get
from wp_publish import _req, check_token, entr_html

LU_HTML = entr_html(
    "Ludwigshafen",
    "Mitte, Süd, Nord, Hemshof, Friesenheim, Oggersheim, Oppau, Edigheim, Gartenstadt, Mundenheim, Rheingönheim, Maudach, Ruchheim",
    ', <a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>',
)
LU_META = "Entrümpelung in Ludwigshafen zum garantierten Festpreis: Wohnung, Keller, Haus, besenreine Übergabe. Kostenlose Besichtigung, kurzfristige Termine. Jetzt per WhatsApp anfragen."

KELLER_HTML = (
    "<p><strong>Auf einen Blick:</strong> Keller, Dachboden und Garage entrümpeln in Mannheim und Umgebung. "
    "Festpreis nach kostenloser Besichtigung, schnelle Termine, besenreine Übergabe. Johnson Services, seit 2011.</p>"
    "<h2>5 Gründe für Johnson Services beim Keller entrümpeln in Mannheim</h2><ul>"
    "<li><strong>Festpreis</strong> nach kostenloser Besichtigung, keine versteckten Kosten.</li>"
    "<li><strong>Schnell</strong>, oft innerhalb weniger Tage.</li>"
    "<li><strong>Besenreine Übergabe</strong>, der Keller ist sofort wieder nutzbar.</li>"
    "<li><strong>Fachgerechte Entsorgung</strong> von Sperrmüll, Elektroschrott und Sondermüll.</li>"
    "<li><strong>Diskret</strong>, ideal für Vermieter und Hausverwaltungen.</li></ul>"
    "<h2>Was wir aus Keller und Dachboden räumen</h2><ul>"
    "<li>Alte Möbel, Kartons und Gerümpel</li><li>Sperrmüll und Hausrat</li>"
    "<li>Elektroschrott und Altgeräte</li><li>Farben, Lacke und Sondermüll (fachgerecht)</li>"
    "<li>Bauschutt nach Absprache</li></ul>"
    "<h2>Festpreis-Übersicht: Keller entrümpeln Mannheim</h2>"
    "<table><thead><tr><th>Objekt</th><th>Geschätzter Festpreis</th></tr></thead><tbody>"
    "<tr><td>Keller bis 20 m²</td><td>ab 590 €</td></tr>"
    "<tr><td>Keller / Dachboden größer</td><td>auf Anfrage</td></tr>"
    "<tr><td>Garage / Lager</td><td>auf Anfrage</td></tr></tbody></table>"
    "<p>Hinweis: Die Wertanrechnung verwertbarer Gegenstände kann den Festpreis reduzieren. Endpreis nach kostenloser Besichtigung.</p>"
    "<h2>Häufige Fragen zum Keller entrümpeln in Mannheim</h2>"
    "<h3>Was kostet es, einen Keller zu entrümpeln?</h3><p>Ein Keller bis 20 m² startet ab 590 €. Den Festpreis nennen wir nach kostenloser Besichtigung.</p>"
    "<h3>Wie schnell geht das?</h3><p>In der Regel innerhalb weniger Tage, bei Bedarf kurzfristig.</p>"
    "<h3>Entsorgt ihr auch Sondermüll und Elektroschrott?</h3><p>Ja, fachgerecht und getrennt.</p>"
    "<h3>Räumt ihr auch Dachboden und Garage?</h3><p>Ja, Keller, Dachboden, Garage und Lager.</p>"
    "<h2>Jetzt kostenloses Festpreis-Angebot anfordern</h2>"
    "<p>Du willst deinen Keller in Mannheim entrümpeln lassen? Kostenlose Besichtigung, verbindlicher Festpreis. <strong>WhatsApp/Telefon: +49 151 57731682</strong></p>"
    '<p>Weitere Leistungen: <a href="https://johnson-services.de/entruempelung/">Entrümpelung</a>, '
    '<a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>, '
    '<a href="https://johnson-services.de/haushaltsaufloesungen/">Haushaltsauflösung</a>.</p>'
)
KELLER_META = "Keller entrümpeln in Mannheim zum Festpreis: Keller, Dachboden, Garage. Fachgerechte Entsorgung, besenreine Übergabe, kostenlose Besichtigung. Jetzt anfragen."

PAGES = [
    ("ludwigshafen", "Entrümpelung Ludwigshafen zum Festpreis", LU_HTML, LU_META),
    ("keller-entruempeln-mannheim", "Keller entrümpeln in Mannheim zum Festpreis", KELLER_HTML, KELLER_META),
]


def main() -> int:
    try:
        me = check_token()
    except urllib.error.HTTPError as e:
        print(f"AUTH FEHLER {e.code}: {e.read().decode()[:140]}")
        return 1
    print(f"✅ Auth OK: {me.get('name')}")
    cat = get("/categories", slug="entruempelung", _fields="id")[0]["id"]

    for slug, title, content, meta in PAGES:
        existing = get("/posts", slug=slug, status="publish,draft,pending,future,private", _fields="id")
        payload = {"title": title, "content": content, "excerpt": meta, "status": "publish", "categories": [cat], "slug": slug}
        if existing:
            r = _req("POST", f"/posts/{existing[0]['id']}", payload)
            action = "aktualisiert"
        else:
            r = _req("POST", "/posts", payload)
            action = "erstellt"
        print(f"{slug}: {action}  status={r.get('status')}  {r.get('link')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
