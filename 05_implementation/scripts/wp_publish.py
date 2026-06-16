"""Publish/update Johnson Services landing pages via WP REST (WRITE).

Used ONLY with explicit user approval. Approved 2026-06-14: fill the empty
posts Entrümpelung Heidelberg (201) + Mannheim (256) and extend the Umzüge
page (266) WITHOUT removing its existing chatbot embed.

Tests auth first and ABORTS if the token is invalid. Voice: du/ihr. Prices are
Johnson's own published Festpreise (mirrored from /entruempelung/ruesselsheim/).

Usage:
    python3 wp_publish.py            # auth test + publish the 3 approved pages
    python3 wp_publish.py --check    # only test the WordPress token
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from wp_client import API, _auth_header, _base

UA = "JS-GrowthEngine/1.0"


def _req(method: str, path: str, payload: dict | None = None):
    url = _base() + API + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={**_auth_header(), "Content-Type": "application/json; charset=utf-8", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode())


def check_token() -> dict:
    """GET /users/me with edit context — proves the app password authenticates + can edit."""
    return _req("GET", "/users/me?context=edit")


LINKS = (
    '<p>Weitere Leistungen: '
    '<a href="https://johnson-services.de/entruempelung/">Entrümpelung</a>, '
    '<a href="https://johnson-services.de/haushaltsaufloesungen/">Haushaltsauflösung</a>, '
    '<a href="https://johnson-services.de/umzuege/">Umzüge</a>{extra}.</p>'
)

FESTPREIS_TABLE = (
    "<h2>Festpreis-Übersicht: Entrümpelung {city}</h2>"
    "<table><thead><tr><th>Objekt</th><th>Geschätzter Festpreis</th></tr></thead><tbody>"
    "<tr><td>Keller bis 20 m²</td><td>ab 590 €</td></tr>"
    "<tr><td>1-Zimmer-Wohnung</td><td>ab 890 €</td></tr>"
    "<tr><td>2-3-Zimmer-Wohnung</td><td>ab 1.490 €</td></tr>"
    "<tr><td>4+ Zimmer-Wohnung / Haus</td><td>auf Anfrage</td></tr>"
    "<tr><td>Messie-Wohnung</td><td>auf Anfrage</td></tr>"
    "</tbody></table>"
    "<p>Hinweis: Die Wertanrechnung verwertbarer Gegenstände kann den Festpreis deutlich reduzieren. "
    "Der Endpreis steht nach der kostenlosen Besichtigung fest.</p>"
)


def entr_html(city: str, districts: str, extra_link: str) -> str:
    return (
        f"<p><strong>Auf einen Blick:</strong> Entrümpelung von Wohnungen, Kellern, Häusern und Gewerbe in {city}. "
        "Festpreis nach kostenloser Besichtigung, keine Nachforderungen. Besenreine Übergabe, kurzfristige Termine. "
        "Johnson Services aus der Region, seit 2011.</p>"
        f"<h2>5 Gründe für Johnson Services bei deiner Entrümpelung in {city}</h2><ul>"
        "<li><strong>Festpreis</strong> nach kostenloser Besichtigung, keine versteckten Kosten.</li>"
        "<li><strong>Kurzfristige Termine</strong>, oft innerhalb weniger Tage.</li>"
        "<li><strong>Besenreine Übergabe</strong>, sodass die Räume sofort vermietbar oder nutzbar sind.</li>"
        "<li><strong>Sorgfältig und effizient</strong>, der Inhaber kommt aus dem Bau.</li>"
        "<li><strong>Wertanrechnung</strong>: Verwertbares rechnen wir gegen und senken so deinen Festpreis.</li></ul>"
        f"<h2>Entrümpelung in allen Stadtteilen von {city}</h2><p>{districts} und Umgebung.</p>"
        + FESTPREIS_TABLE.format(city=city) +
        f"<h2>Häufige Fragen zur Entrümpelung in {city}</h2>"
        f"<h3>Was kostet eine Entrümpelung in {city}?</h3>"
        "<p>Die Kosten richten sich nach Umfang, Müllmenge und Zugänglichkeit. Eine 2-3-Zimmer-Wohnung startet ab 1.490 €. "
        "Den verbindlichen Festpreis nennen wir nach kostenloser Besichtigung.</p>"
        f"<h3>Wie schnell könnt ihr entrümpeln?</h3><p>In der Regel innerhalb weniger Tage, bei Bedarf auch kurzfristig.</p>"
        f"<h3>Übernehmt ihr auch Messie-Wohnungen in {city}?</h3>"
        "<p>Ja, diskret und mit Erfahrung. Den Festpreis legen wir nach Besichtigung fest.</p>"
        "<h3>Was passiert mit verwertbaren Gegenständen?</h3>"
        "<p>Möbel, Elektronik und Wertgegenstände bewerten wir vor Ort und rechnen sie transparent gegen deinen Festpreis.</p>"
        f"<h2>Jetzt kostenloses Festpreis-Angebot für {city} anfordern</h2>"
        f"<p>Du planst eine Entrümpelung in {city}? Wir besichtigen kostenlos und erstellen ein verbindliches "
        "Festpreis-Angebot. <strong>WhatsApp/Telefon: +49 151 57731682</strong></p>"
        + LINKS.format(extra=extra_link)
    )


HEIDELBERG_HTML = entr_html(
    "Heidelberg",
    "Altstadt, Bergheim, Weststadt, Neuenheim, Handschuhsheim, Rohrbach, Kirchheim, Wieblingen, Pfaffengrund, Boxberg, Emmertsgrund, Ziegelhausen, Schlierbach",
    ', <a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>',
)
MANNHEIM_HTML = entr_html(
    "Mannheim",
    "Innenstadt und Quadrate, Neckarstadt, Lindenhof, Schwetzingerstadt, Oststadt, Feudenheim, Käfertal, Neckarau, Rheinau, Seckenheim, Friedrichsfeld, Waldhof, Sandhofen, Vogelstang, Schönau, Wallstadt",
    ', <a href="https://johnson-services.de/entruempelung/heidelberg/">Entrümpelung Heidelberg</a>',
)

UMZUG_HTML = (
    "<p><strong>Auf einen Blick:</strong> Privat- und Gewerbeumzüge in Mannheim, Ludwigshafen, Heidelberg und Umgebung. "
    "Festpreis nach kostenloser Besichtigung, alles aus einer Hand: Transport, Tragen, Ab- und Aufbau. Johnson Services, seit 2011.</p>"
    "<h2>5 Gründe für Johnson Services bei deinem Umzug</h2><ul>"
    "<li><strong>Festpreis</strong> nach kostenloser Besichtigung, keine Nachforderungen.</li>"
    "<li><strong>Alles aus einer Hand</strong>: Transport, Tragen, Ab- und Aufbau der Möbel.</li>"
    "<li><strong>Erfahren mit engen Treppenhäusern</strong> und alten Häusern, ohne Schäden.</li>"
    "<li><strong>Kurzfristige Termine</strong> möglich.</li>"
    "<li><strong>Auf Wunsch Entrümpelung und Reinigung</strong> der alten Wohnung gleich mit dazu.</li></ul>"
    "<h2>Unsere Umzugsleistungen</h2><ul>"
    "<li>Privatumzüge (Wohnung, Haus)</li><li>Gewerbe- und Büroumzüge</li><li>Möbeltransport und Einzelstücke</li>"
    "<li>Ab- und Aufbau von Möbeln</li><li>Verpackung und Tragehilfe</li>"
    "<li>Entrümpelung und besenreine Übergabe der alten Wohnung</li></ul>"
    "<h2>Umzug in der Region</h2><p>Mannheim, Ludwigshafen, Heidelberg, Viernheim, Weinheim, Schwetzingen, Speyer, Worms und Umgebung. Auf Anfrage auch Fernumzüge.</p>"
    "<h2>Richtpreise: Umzug zum Festpreis</h2>"
    "<table><thead><tr><th>Umfang</th><th>Richtwert</th></tr></thead><tbody>"
    "<tr><td>1-2-Zimmer-Wohnung</td><td>ab 900 €</td></tr>"
    "<tr><td>3-Zimmer-Wohnung</td><td>ab 1.300 €</td></tr>"
    "<tr><td>4+ Zimmer / Haus</td><td>ab 2.000 €</td></tr></tbody></table>"
    "<p>Hinweis: Richtwerte. Der verbindliche Festpreis hängt von Entfernung, Etage, Aufzug und Umfang ab und steht nach der kostenlosen Besichtigung fest.</p>"
    "<h2>Häufige Fragen zum Umzug</h2>"
    "<h3>Was kostet ein Umzug in Mannheim?</h3><p>Je nach Wohnungsgröße, Etage, Aufzug und Entfernung. Eine 3-Zimmer-Wohnung startet ab 1.300 €. Festpreis nach kostenloser Besichtigung.</p>"
    "<h3>Übernehmt ihr auch den Ab- und Aufbau der Möbel?</h3><p>Ja, auf Wunsch bauen wir Schränke, Betten und Küchen ab und am neuen Ort wieder auf.</p>"
    "<h3>Könnt ihr die alte Wohnung danach entrümpeln und reinigen?</h3><p>Ja, Umzug, Entrümpelung und Reinigung gibt es bei uns aus einer Hand, damit die Übergabe stressfrei klappt.</p>"
    "<h3>Wie schnell ist ein Termin möglich?</h3><p>Oft innerhalb weniger Tage, bei Bedarf kurzfristig.</p>"
    "<h2>Jetzt kostenloses Umzugs-Angebot anfordern</h2>"
    "<p>Du planst einen Umzug in der Region? Kostenlose Besichtigung, verbindlicher Festpreis. <strong>WhatsApp/Telefon: +49 151 57731682</strong></p>"
    '<p>Weitere Leistungen: <a href="https://johnson-services.de/entruempelung/">Entrümpelung</a>, '
    '<a href="https://johnson-services.de/entruempelung/mannheim/">Entrümpelung Mannheim</a>, '
    '<a href="https://johnson-services.de/haushaltsaufloesungen/">Haushaltsauflösung</a>.</p>'
    "<hr>"
)

META = {
    "heidelberg": "Entrümpelung in Heidelberg zum garantierten Festpreis: Wohnung, Keller, Haus, besenreine Übergabe. Kostenlose Besichtigung, kurzfristige Termine. Jetzt per WhatsApp anfragen.",
    "mannheim": "Entrümpelung in Mannheim zum garantierten Festpreis: Wohnung, Keller, Haus, besenreine Übergabe. Kostenlose Besichtigung, kurzfristige Termine. Jetzt per WhatsApp anfragen.",
    "umzug": "Umzug in Mannheim, Ludwigshafen, Heidelberg und Umgebung zum Festpreis. Möbeltransport, Ab- und Aufbau, alles aus einer Hand. Kostenlose Besichtigung.",
}


def main(argv: list[str]) -> int:
    try:
        me = check_token()
    except urllib.error.HTTPError as e:
        print(f"WORDPRESS-TOKEN UNGÜLTIG: HTTP {e.code} — {e.read().decode()[:160]}")
        return 1
    print(f"✅ WordPress-Token gültig. Angemeldet als: {me.get('name')} (id {me.get('id')}, roles {me.get('roles')})")
    if "--check" in argv:
        return 0

    # 1) Heidelberg (Post 201, war leer)
    r = _req("POST", "/posts/201", {"title": "Entrümpelung Heidelberg zum Festpreis", "content": HEIDELBERG_HTML, "excerpt": META["heidelberg"], "status": "publish"})
    print(f"Heidelberg (201): status={r.get('status')}  {r.get('link')}")

    # 2) Mannheim (Post 256, war leer)
    r = _req("POST", "/posts/256", {"title": "Entrümpelung Mannheim zum Festpreis", "content": MANNHEIM_HTML, "excerpt": META["mannheim"], "status": "publish"})
    print(f"Mannheim (256): status={r.get('status')}  {r.get('link')}")

    # 3) Umzüge (Page 266) — Chatbot ERHALTEN: neuen Content davor einfügen
    cur = _req("GET", "/pages/266?context=edit&_fields=content")
    raw = (cur.get("content") or {}).get("raw", "") or ""
    merged = UMZUG_HTML + "\n" + raw
    r = _req("POST", "/pages/266", {"content": merged, "excerpt": META["umzug"], "status": "publish"})
    print(f"Umzüge (266): status={r.get('status')}  {r.get('link')}  (Chatbot erhalten: {'ja' if 'VG_CONFIG' in merged else 'PRÜFEN'})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
