import imaplib, email
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from env_loader import require
c = require("IONOS_EMAIL","IONOS_EMAIL_PASSWORD","IONOS_IMAP_SERVER","IONOS_IMAP_PORT")
M=imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"],int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"],c["IONOS_EMAIL_PASSWORD"]); M.select("INBOX")
typ,data=M.search(None,'FROM "mannheim.de"')
ids=data[0].split()
rows=[]
for mid in ids:
    typ,md=M.fetch(mid,"(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    msg=email.message_from_bytes(md[0][1])
    subj=str(make_header(decode_header(msg.get("Subject",""))))
    frm=str(make_header(decode_header(msg.get("From",""))))
    try: dt=parsedate_to_datetime(msg.get("Date","")); ds=dt.strftime("%Y-%m-%d")
    except: ds="?"
    rows.append((ds, frm, subj))
rows.sort(key=lambda r:r[0])
for ds,frm,subj in rows:
    print(f"{ds} | {frm[:38]:38} | {subj[:60]}")
M.logout()