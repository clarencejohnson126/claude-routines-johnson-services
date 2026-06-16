import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def get(path):
    r=urllib.request.Request(BASE+path, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0"})
    with urllib.request.urlopen(r,timeout=40) as resp: return json.load(resp), resp.status
def live(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"}),timeout=40).read().decode(errors="ignore")

print("=== Verbleibende alte Nummer LIVE (nach Body-Fix) ===")
for url in ["https://johnson-services.de/","https://johnson-services.de/entruempelung/messie-wohnung-heidelberg/"]:
    h=live(url)
    print(f"  {url}\n    '1811 123': {h.count('1811 123')}  tel:+491621811123: {h.count('+491621811123')}  neu 57731682: {h.count('57731682')}")

print("\n=== Schema-Telefon live ===")
h=live("https://johnson-services.de/")
import re
m=re.search(r'"telephone":"([^"]*)"', h)
print("  telephone im Schema:", m.group(1) if m else "?")

print("\n=== elementor_library Templates: Nummer im REST-editierbaren content.raw? ===")
items,_=get("/wp-json/wp/v2/elementor_library?per_page=50&context=edit&_fields=id,slug,title,content,meta")
for it in items:
    raw=(it.get("content") or {}).get("raw","") or ""
    metablob=json.dumps(it.get("meta",{}))
    print(f"  id={it['id']} slug={it.get('slug')}: content.raw#={raw.count('1811123')+raw.count('1811 123')}  meta#={metablob.count('1811123')+metablob.count('1811 123')}")