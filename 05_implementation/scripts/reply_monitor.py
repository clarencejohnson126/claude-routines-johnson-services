"""Outreach reply monitor. Prüft den IONOS-Posteingang auf Antworten von
kontaktierten B2B-Leads und alarmiert per Telegram. Dedupliziert über
Message-IDs. Freemail-Domains (gmail etc.) nur per exakter Adresse, nicht
per Domain (sonst Falschtreffer).

Usage: python3 reply_monitor.py
"""
from __future__ import annotations

import csv
import email
import imaplib
import json
import sys
from datetime import datetime, timezone
from email.header import decode_header, make_header
from email.utils import parseaddr
from pathlib import Path

import notify
from env_loader import require

LD = Path(__file__).resolve().parents[2] / "07_outputs" / "lead_lists"
STATE = LD / ".replies_seen.json"
FREEMAIL = {"gmail.com", "outlook.de", "outlook.com", "web.de", "gmx.de", "gmx.net",
            "yahoo.com", "yahoo.de", "t-online.de", "hotmail.com", "hotmail.de", "icloud.com"}


def sent_targets() -> tuple[set, set, str]:
    emails, domains, dates = set(), set(), []
    for p in sorted(LD.glob("outreach_sent_log_*.csv")):
        try:
            for r in csv.DictReader(p.open(encoding="utf-8")):
                if r.get("status") == "sent" and r.get("email"):
                    e = r["email"].strip().lower()
                    emails.add(e)
                    dom = e.split("@")[-1]
                    if dom not in FREEMAIL:
                        domains.add(dom)
                    if r.get("sent_at"):
                        dates.append(r["sent_at"][:10])
        except Exception:
            continue
    since = min(dates) if dates else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        since_imap = datetime.strptime(since, "%Y-%m-%d").strftime("%d-%b-%Y")
    except Exception:
        since_imap = datetime.now(timezone.utc).strftime("%d-%b-%Y")
    return emails, domains, since_imap


def main() -> int:
    emails, domains, since = sent_targets()
    if not emails:
        print("Keine gesendeten Leads im Log.")
        return 0
    seen = set(json.loads(STATE.read_text())) if STATE.exists() else set()
    c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_IMAP_SERVER", "IONOS_IMAP_PORT")
    M = imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"], int(c["IONOS_IMAP_PORT"]))
    M.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
    M.select("INBOX")
    typ, d = M.search(None, "SINCE", since)
    ids = d[0].split() if d and d[0] else []
    new = []
    for num in ids[-400:]:
        typ, data = M.fetch(num, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT MESSAGE-ID)])")
        if not data or not data[0]:
            continue
        hdr = email.message_from_bytes(data[0][1])
        frm = parseaddr(hdr.get("From", ""))[1].lower()
        mid = hdr.get("Message-ID", "").strip()
        if not frm or not mid or mid in seen:
            continue
        dom = frm.split("@")[-1]
        if frm in emails or dom in domains:
            subj = str(make_header(decode_header(hdr.get("Subject", "")))).strip()
            new.append((frm, subj))
            seen.add(mid)
    M.logout()
    STATE.write_text(json.dumps(sorted(seen)))

    if new:
        body = f"📩 Outreach-Antwort(en) von kontaktierten Leads ({len(new)}):\n" + \
               "\n".join(f"- {f}: {s[:70]}" for f, s in new) + \
               "\n→ bitte persönlich antworten (info@johnson-services.de)."
        notify.send(body)
        print(body)
    else:
        print(f"Keine neuen Antworten (geprüft seit {since}, {len(ids)} Inbox-Mails gescannt).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
