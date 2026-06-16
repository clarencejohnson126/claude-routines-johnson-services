import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r), r.status
try:
    plugins,_=get("/wp-json/wp/v2/plugins")
    print("Installierte Plugins:", len(plugins))
    for p in plugins:
        name=p.get("name","")
        status=p.get("status","")
        flag=""
        low=(name+" "+p.get("plugin","")).lower()
        if any(k in low for k in ("search","replace","snippet","code","header","footer","elementor","rank","wp-cli")):
            flag=" <<<"
        print(f"  [{status:8}] {name}{flag}")
except urllib.error.HTTPError as e:
    print("plugins endpoint:", e.code, e.read().decode()[:150])