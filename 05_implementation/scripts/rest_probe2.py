import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r), r.status

# Alle Post-Types + REST-base
types,_=get("/wp-json/wp/v2/types")
print("POST-TYPES (rest_base):")
for k,v in types.items():
    rb=v.get("rest_base")
    print(f"  {k} -> {rb}")

# Elementor-Templates durchsuchen (header/footer/global)
print("\n--- Suche Nummer in elementor_library ---")
for pt_base in ("elementor_library","template","elementor-library"):
    try:
        items,_=get(f"/wp-json/wp/v2/{pt_base}?per_page=50&context=edit&_fields=id,slug,title,meta")
        print(f"[{pt_base}] {len(items)} Templates")
        for it in items:
            blob=json.dumps(it.get("meta",{}))
            if "1811123" in blob or "1811 123" in blob:
                print(f"   >>> NUMMER in template id={it['id']} slug={it.get('slug')}")
        break
    except urllib.error.HTTPError as e:
        print(f"[{pt_base}] HTTP {e.code}")