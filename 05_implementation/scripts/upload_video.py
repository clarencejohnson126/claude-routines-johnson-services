import base64, json, sys, urllib.request, urllib.error
from env_loader import require

c = require("WORDPRESS_SITE_URL", "WORDPRESS_USER", "WORDPRESS_APP_PASSWORD")
SRC = "/Users/clarence/Desktop/download (8).mp4"
FILENAME = "entruempelung-mannheim-johnson-services.mp4"

data = open(SRC, "rb").read()
tok = base64.b64encode((c["WORDPRESS_USER"] + ":" + c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
req = urllib.request.Request(
    c["WORDPRESS_SITE_URL"].rstrip("/") + "/wp-json/wp/v2/media",
    data=data, method="POST",
    headers={
        "Authorization": "Basic " + tok,
        "Content-Disposition": 'attachment; filename="' + FILENAME + '"',
        "Content-Type": "video/mp4",
        "User-Agent": "JS-GrowthEngine/1.0",
    },
)
try:
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    print("OK — hochgeladen")
    print("ID:", d.get("id"))
    print("URL:", d.get("source_url"))
    print("Titel:", (d.get("title") or {}).get("rendered"))
except urllib.error.HTTPError as e:
    print("FEHLER", e.code, e.read().decode()[:300])
