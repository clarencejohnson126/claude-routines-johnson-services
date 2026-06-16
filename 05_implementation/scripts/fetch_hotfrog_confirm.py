import imaplib, email, re
from email.header import decode_header
from env_loader import require

c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_IMAP_SERVER", "IONOS_IMAP_PORT")
print("Postfach:", c["IONOS_EMAIL"])

M = imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"], int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
M.select("INBOX")

# Suche nach jüngsten Mails von hotfrog/locafy/newfold
typ, data = M.search(None, 'OR OR FROM "hotfrog" FROM "locafy" FROM "newfold"')
ids = data[0].split()
print("Treffer:", len(ids))
if not ids:
    # Fallback: letzte 10 Mails durchsehen
    typ, data = M.search(None, "ALL")
    ids = data[0].split()[-10:]
    print("Fallback letzte:", len(ids))

links = []
for mid in ids[-5:]:
    typ, md = M.fetch(mid, "(RFC822)")
    msg = email.message_from_bytes(md[0][1])
    subj = msg.get("Subject", "")
    frm = msg.get("From", "")
    body = ""
    if msg.is_multipart():
        for p in msg.walk():
            if p.get_content_type() in ("text/plain", "text/html"):
                try: body += p.get_payload(decode=True).decode(errors="ignore")
                except: pass
    else:
        try: body = msg.get_payload(decode=True).decode(errors="ignore")
        except: pass
    found = re.findall(r'https?://[^\s"\'<>]*(?:hotfrog|locafy|confirm|verif|activ|token)[^\s"\'<>]*', body, re.I)
    print("---")
    print("FROM:", frm[:60], "| SUBJ:", subj[:60])
    for l in found[:5]:
        print("LINK:", l)
        links.append(l)
M.logout()