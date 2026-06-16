import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r), r.status

NEEDLE_VARIANTS=["1811123","1811 123"]
def has_num(s):
    s=json.dumps(s) if not isinstance(s,str) else s
    return any(n in s for n in NEEDLE_VARIANTS)

# 1) Globale REST-Suche
print("=== /wp/v2/search?search=1811123 ===")
try:
    res,_=get("/wp-json/wp/v2/search?search=1811123&per_page=20")
    print("Treffer:", len(res))
    for r in res: print("  ", r.get("type"), r.get("subtype"), r.get("id"), "-", (r.get("title") or "")[:40])
except urllib.error.HTTPError as e: print("  HTTP", e.code)

# 2) Front page (6) + elementor_library: post_content (REST-editierbar) prüfen
print("\n=== post_content (REST-editierbar) enthält Nummer? ===")
for path in ["/wp-json/wp/v2/pages/6?context=edit&_fields=id,content,meta",
             "/wp-json/wp/v2/elementor_library?per_page=50&context=edit&_fields=id,slug,content,meta"]:
    try:
        d,_=get(path)
        items=d if isinstance(d,list) else [d]
        for it in items:
            cont=(it.get("content") or {}).get("raw") or (it.get("content") or {}).get("rendered") or ""
            inmeta=has_num(it.get("meta",{}))
            incont=has_num(cont)
            if incont or inmeta:
                print(f"  id={it.get('id')} slug={it.get('slug','?')}: in_content={incont} in_REST-meta={inmeta}")
    except urllib.error.HTTPError as e: print("  HTTP", e.code, path.split('?')[0])

# 3) Rank Math Routen
print("\n=== rankmath/v1 Routen ===")
try:
    d,_=get("/wp-json/rankmath/v1")
    routes=list((d.get("routes") or {}).keys())
    print("  ", routes[:20] or "keine")
except urllib.error.HTTPError as e: print("  HTTP", e.code)

# 4) Settings-Endpoint: ist Telefon dort?
print("\n=== /wp/v2/settings (Telefon dort?) ===")
try:
    d,_=get("/wp-json/wp/v2/settings")
    print("  Keys:", [k for k in d.keys()][:30])
except urllib.error.HTTPError as e: print("  HTTP", e.code)