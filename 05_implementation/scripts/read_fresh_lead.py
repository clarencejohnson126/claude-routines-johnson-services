import imaplib, email
from email.header import decode_header, make_header
from env_loader import require
c = require("IONOS_EMAIL","IONOS_EMAIL_PASSWORD","IONOS_IMAP_SERVER","IONOS_IMAP_PORT")
M=imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"],int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"],c["IONOS_EMAIL_PASSWORD"]); M.select("INBOX")
# Die heutige Anfrage von Toni Prasse
typ,data=M.search(None,'(FROM "Toni.Prasse" SUBJECT "Kostenvoranschlag Wohnungsr")')
ids=data[0].split()
print("Treffer:", len(ids))
for mid in ids:
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
    print("VON:", frm); print("DATUM:", date); print("BETREFF:", subj)
    print("TEXT:\n", body.strip()[:2000])
M.logout()