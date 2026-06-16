import imaplib, email
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from env_loader import require
c = require("IONOS_EMAIL","IONOS_EMAIL_PASSWORD","IONOS_IMAP_SERVER","IONOS_IMAP_PORT")
M=imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"],int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"],c["IONOS_EMAIL_PASSWORD"]); M.select("INBOX")
typ,data=M.search(None,'(SINCE 25-May-2026)')
ids=data[0].split()
# Marketing/Auto/System-Absender ausschließen
SKIP=("provenexpert","golocal","hotfrog","centralindex","noreply","no-reply","newsletter","mailer","notifications","facebook","google","linkedin","instagram","info@johnson","mailchimp","sendgrid","newfold","locafy")
print(f"Mails seit 25-Mai: {len(ids)} — mögliche Leads (Marketing/System gefiltert):\n")
rows=[]
for mid in ids:
    typ,md=M.fetch(mid,"(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
    msg=email.message_from_bytes(md[0][1])
    frm=str(make_header(decode_header(msg.get("From",""))))
    subj=str(make_header(decode_header(msg.get("Subject",""))))
    if any(s in frm.lower() for s in SKIP): continue
    try: ds=parsedate_to_datetime(msg.get("Date","")).strftime("%Y-%m-%d")
    except: ds="?"
    rows.append((ds,frm,subj))
rows.sort(key=lambda r:r[0], reverse=True)
for ds,frm,subj in rows[:25]:
    print(f"{ds} | {frm[:40]:40} | {subj[:55]}")
M.logout()