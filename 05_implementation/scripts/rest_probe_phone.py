import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r), r.status

# 1) REST-Namespaces (gibt es rankmath / oxygen?)
data,st=get("/wp-json/")
ns=data.get("namespaces",[])
print("NAMESPACES:", [n for n in ns if any(k in n.lower() for k in ("rank","oxygen","ct","seo"))] or "keine rank/oxygen")

# 2) Frontpage finden
pages,_=get("/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,link,title")
front=[p for p in pages if p["link"].rstrip("/")==BASE]
print("FRONTPAGE:", [(p["id"],p["slug"]) for p in front] or "nicht eindeutig — alle:", [(p["id"],p["slug"]) for p in pages][:10])

# 3) Oxygen-Postmeta lesbar? (ct_builder_shortcodes)
if front:
    fid=front[0]["id"]
    try:
        pg,_=get(f"/wp-json/wp/v2/pages/{fid}?context=edit")
        meta=pg.get("meta",{})
        print("META-KEYS:", list(meta.keys())[:25])
        # nach der Nummer in meta suchen
        blob=json.dumps(meta)
        print("NUMMER in page-meta?", "1811123" in blob or "1811 123" in blob)
    except urllib.error.HTTPError as e:
        print("page context=edit:", e.code, e.read().decode()[:120])

# 4) ct_template (Oxygen header/footer) als Posttype erreichbar?
for pt in ("ct_template","oxy_user_library","ct_content"):
    try:
        d,_=get(f"/wp-json/wp/v2/{pt}?per_page=3&_fields=id,slug")
        print(f"POSTTYPE {pt}:", d if isinstance(d,list) else "ok")
    except urllib.error.HTTPError as e:
        print(f"POSTTYPE {pt}: HTTP {e.code}")