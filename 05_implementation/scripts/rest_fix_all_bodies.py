import base64, json, urllib.request, urllib.error
from env_loader import require
c = require("WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APP_PASSWORD")
BASE=c["WORDPRESS_SITE_URL"].rstrip("/")
tok=base64.b64encode((c["WORDPRESS_USER"]+":"+c["WORDPRESS_APP_PASSWORD"]).encode()).decode()
def req(path, method="GET", body=None):
    r=urllib.request.Request(BASE+path, method=method, headers={"Authorization":"Basic "+tok,"User-Agent":"JS/1.0","Content-Type":"application/json"}, data=(json.dumps(body).encode() if body else None))
    with urllib.request.urlopen(r,timeout=60) as resp: return json.load(resp), resp.status

REPL=[("+491621811123","+4915157731682"),("+49 162 1811 123","+49 151 57731682"),
      ("01621811123","015157731682"),("0162 1811 123","0151 57731682"),("0162 1811123","0151 57731682")]
IDS=[(443,"posts"),(441,"pages"),(412,"posts"),(411,"posts"),(410,"posts"),(409,"posts"),
     (408,"posts"),(407,"posts"),(406,"posts"),(405,"posts"),(403,"posts"),(404,"posts"),(353,"pages")]
fixed=0
for pid,base in IDS:
    try:
        d,_=req(f"/wp-json/wp/v2/{base}/{pid}?context=edit&_fields=id,content")
        raw=d["content"]["raw"]; new=raw
        for a,b in REPL: new=new.replace(a,b)
        before=raw.count("1811123")+raw.count("1811 123")
        after=new.count("1811123")+new.count("1811 123")
        if new!=raw:
            _,st=req(f"/wp-json/wp/v2/{base}/{pid}","POST",{"content":new})
            print(f"  {pid}: content {before}->{after}  PUT {st}")
            fixed+=1
        else:
            print(f"  {pid}: keine Änderung (Treffer nur in geschützten Daten)")
    except urllib.error.HTTPError as e:
        print(f"  {pid}: HTTP {e.code}")
print("Seiten-Inhalte korrigiert:", fixed)