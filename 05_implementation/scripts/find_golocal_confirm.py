import imaplib, email, re
from email.header import make_header, decode_header
from env_loader import require

c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_IMAP_SERVER", "IONOS_IMAP_PORT")
M = imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"], int(c["IONOS_IMAP_PORT"]))
M.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
M.select("INBOX")
typ, d = M.search(None, "SINCE", "15-Jun-2026", "FROM", "golocal")
ids = d[0].split() if d and d[0] else []
print("golocal-Mails heute:", len(ids))
links = []
for num in ids[-3:]:
    typ, data = M.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])
    subj = str(make_header(decode_header(msg.get("Subject", ""))))
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/html", "text/plain"):
                try:
                    body += part.get_payload(decode=True).decode("utf-8", "ignore")
                except Exception:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode("utf-8", "ignore")
        except Exception:
            body = ""
    print("SUBJECT:", subj)
    found = re.findall(r"https?://[^\s\"'<>]*golocal[^\s\"'<>]*", body)
    conf = [u for u in found if re.search(r"confirm|bestaet|best%C3|verif|activate|token|aktivier|register|emailbest", u, re.I)]
    links += (conf or found)
M.logout()
print("KONFIRM-LINKS:")
for u in dict.fromkeys(links):
    print(u)
