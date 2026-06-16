import base64, json, urllib.request, urllib.error, re
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def req(path, method="GET", body=None):
    r=urllib.request.Request(BASE+path, method=method, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0","Content-Type":"application/json"}, data=(json.dumps(body).encode() if body else None))
    with urllib.request.urlopen(r,timeout=60) as resp: return json.load(resp), resp.status

d,_=req("/wp-json/wp/v2/posts/444?context=edit&_fields=id,link,content")
raw=(d["content"]["raw"])
link=d["link"]
print("LINK:", link)
# Zeige die Telefonnummer-Kontexte im content.raw
for m in re.finditer(r'.{30}(1811123|1811 123).{15}', raw):
    print("KONTEXT:", repr(m.group(0)))
print("\nRoh-Vorkommen 1811123:", raw.count("1811123"), "| 1811 123:", raw.count("1811 123"))