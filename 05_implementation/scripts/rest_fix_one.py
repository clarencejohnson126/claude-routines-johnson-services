import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def req(path, method="GET", body=None):
    r=urllib.request.Request(BASE+path, method=method, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0","Content-Type":"application/json"}, data=(json.dumps(body).encode() if body else None))
    with urllib.request.urlopen(r,timeout=60) as resp: return json.load(resp), resp.status

REPL=[("+491621811123","+4915157731682"),("+49 162 1811 123","+49 151 57731682"),("01621811123","015157731682")]
d,_=req("/wp-json/wp/v2/posts/444?context=edit&_fields=id,link,content")
raw=d["content"]["raw"]; link=d["link"]
new=raw
for a,b in REPL: new=new.replace(a,b)
print("Änderungen im content:", raw.count("1811123")+raw.count("1811 123"), "->", new.count("1811123")+new.count("1811 123"))
if new!=raw:
    res,st=req("/wp-json/wp/v2/posts/444", "POST", {"content":new})
    print("PUT status:", st)
# Live prüfen
import urllib.request as u
html=u.urlopen(u.Request(link, headers={"User-Agent":"Mozilla/5.0"}),timeout=40).read().decode(errors="ignore")
print("LIVE alte Nummer (1811 123):", html.count("1811 123"), "| tel:+491621811123:", html.count("+491621811123"))
print("LIVE neue Nummer (57731682):", html.count("57731682"))