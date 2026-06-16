import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    req=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(req,timeout=40) as r: return json.load(r), r.status

IDS=[444,443,441,412,411,410,409,408,407,406,405,403,404,353]
def count(s,sub): return s.count(sub)
print(f"{'ID':>4} | {'typ':4} | in content.raw | in _elementor_data(meta) | builder")
for pid in IDS:
    for typ,base in (("page","pages"),("post","posts")):
        try:
            d,_=get(f"/wp-json/wp/v2/{base}/{pid}?context=edit")
            raw=(d.get("content") or {}).get("raw","") or ""
            meta=d.get("meta",{})
            metablob=json.dumps(meta)
            el = "_elementor_data" in metablob or "_elementor_edit_mode" in metablob
            n_raw = count(raw,"1811123")+count(raw,"1811 123")
            n_meta = count(metablob,"1811123")+count(metablob,"1811 123")
            print(f"{pid:>4} | {typ:4} | {n_raw:>13} | {n_meta:>22} | {'elementor' if el else 'klassisch/andere'}")
            break
        except urllib.error.HTTPError as e:
            if e.code!=404: print(f"{pid}: HTTP {e.code}")