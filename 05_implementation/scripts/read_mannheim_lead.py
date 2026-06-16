import imaplib, email
from email.header import decode_header, make_header
from env_loader import require
c = require("IONOS_EMAIL","IONOS_EMAIL_PASSWORD","IONOS_IMAP_SERVER","IONOS_IMAP_PORT")
M=imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"],int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"],c["IONOS_EMAIL_PASSWORD"]); M.select("INBOX")
typ,data=M.search(None,'FROM "mannheim.de"')
ids=data[0].split()
print("Anfragen von mannheim.de:", len(ids))
for mid in ids[-3:]:
    typ,md=M.fetch(mid,"(RFC822)"); msg=email.message_from_bytes(md[0][1])
    subj=str(make_header(decode_header(msg.get("Subject",""))))
    frm=str(make_header(decode_header(msg.get("From",""))))
    date=msg.get("Date","")
    body=""
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type()=="text/plain":
                try: body+=p.get_payload(decode=True).decode(errors="ignore")
                except: pass
    else:
        try: body=msg.get_payload(decode=True).decode(errors="ignore")
        except: pass
    print("\n===== LEAD =====")
    print("VON:", frm)
    print("DATUM:", date)
    print("BETREFF:", subj)
    print("TEXT:\n", body.strip()[:1500])
M.logout()