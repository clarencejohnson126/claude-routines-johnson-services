import sys
sys.path.insert(0, "/Users/clarence/Desktop/AUTOMATED ADS/Agentic Johnson Services/05_implementation/scripts")
import imaplib, email, re
from env_loader import require
c = require("IONOS_EMAIL","IONOS_EMAIL_PASSWORD","IONOS_IMAP_SERVER","IONOS_IMAP_PORT")
M=imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"],int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"],c["IONOS_EMAIL_PASSWORD"]); M.select("INBOX")
typ,data=M.search(None,'FROM "centralindex"')
ids=data[0].split()
link=None
for mid in ids[-2:]:
    typ,md=M.fetch(mid,"(RFC822)"); msg=email.message_from_bytes(md[0][1])
    body=""
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type() in ("text/plain","text/html"):
                try: body+=p.get_payload(decode=True).decode(errors="ignore")
                except: pass
    else:
        try: body=msg.get_payload(decode=True).decode(errors="ignore")
        except: pass
    m=re.findall(r'https?://admin\.hotfrog\.de/login/set-password\?token=[^\s"\'<>]+', body)
    if m: link=m[0]
M.logout()
if not link:
    print("KEIN LINK");
else:
    new_tab(link); wait_for_load()
    js("new Promise(function(r){setTimeout(r,1500);})")
    print("URL:", page_info().get("url"))
    print("FIELDS:", js("JSON.stringify(Array.from(document.querySelectorAll('input')).map(function(e){return {name:e.name||e.id,type:e.type,ph:e.placeholder};}).filter(function(e){return e.type!=='hidden';}))"))
    print("BUTTONS:", js("JSON.stringify(Array.from(document.querySelectorAll('button,input[type=submit]')).map(function(b){return (b.innerText||b.value||'').trim();}).filter(Boolean))"))
    print("SHOT:", capture_screenshot())