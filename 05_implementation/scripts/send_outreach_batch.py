"""B2B Outreach-Versand via IONOS (info@johnson-services.de).

Stellt `send_leads()` bereit (von leadfinding_batch.py für Auto-Versand genutzt)
und kann eigenständig den neuesten Lead-Batch senden. Sie-Form, Opt-out-Zeile,
5 Sek Abstand. Dedupliziert gegen alle bisherigen Versand-Logs (kein Doppelversand).

Versand nur mit --send ODER APPROVED_TO_SEND_OUTREACH=true. Sonst Dry-Run.

Usage:
    python3 send_outreach_batch.py            # Dry-Run auf neuesten Batch
    python3 send_outreach_batch.py --send      # echter Versand des neuesten Batch
    python3 send_outreach_batch.py <file.csv> --send
"""
from __future__ import annotations

import csv
import imaplib
import os
import smtplib
import ssl
import sys
import time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path

SENT_FOLDER = "Gesendete Objekte"  # IONOS Sent folder (\Sent)

from env_loader import load_env, require
from leadfinding_batch import PITCH

PROOT = Path(__file__).resolve().parents[2]
LEAD_DIR = PROOT / "07_outputs" / "lead_lists"
DELAY_S = 5
SUBJECT = "Zuverlässiger Partner für Räumung und besenreine Übergabe in {region}"
BODY = """Sehr geehrte Damen und Herren,

Johnson Services unterstützt Unternehmen wie {firma} in {region} und Umgebung: {pitch}. Feste Preiszusage nach kostenloser Besichtigung, kurzfristige Termine, besenreine Übergabe.

Dürfen wir Ihnen bei Ihrem nächsten Fall ein unverbindliches Festpreis-Angebot machen? Eine kurze Rückmeldung genügt.

Mit freundlichen Grüßen
Clarence Johnson
Johnson Services, Mannheim (seit 2011)
Tel/WhatsApp: +49 151 57731682
info@johnson-services.de  johnson-services.de

Falls dieses Angebot für Sie nicht relevant ist, genügt eine kurze Antwort und wir melden uns nicht erneut.
"""
DEFAULT_PITCH = "bei Entrümpelung, Räumung und besenreiner Übergabe unterstützen wir Sie zuverlässig"


def latest_batch_file() -> Path | None:
    files = sorted(LEAD_DIR.glob("leads_batch_*.csv"))
    return files[-1] if files else None


def already_sent_via_imap() -> set:
    """Empfaenger frueherer Outreach-Mails aus dem IONOS Sent-Ordner.
    STATELESS-SICHER: funktioniert auch im frisch geklonten Cloud-Container, in dem
    keine lokalen Logs existieren. 'besenreine' (aus dem Betreff) ist ASCII -> IMAP-SEARCH-safe."""
    import email as _email
    from email.utils import getaddresses
    out = set()
    try:
        c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_IMAP_SERVER", "IONOS_IMAP_PORT")
    except SystemExit:
        return out
    try:
        M = imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"], int(c["IONOS_IMAP_PORT"]))
        M.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
        if M.select(f'"{SENT_FOLDER}"')[0] != "OK":
            M.select("Sent")
        typ, data = M.search(None, 'HEADER SUBJECT "besenreine"')
        ids = data[0].split() if (data and data[0]) else []
        for mid in ids:
            t, md = M.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (TO)])")
            if md and md[0]:
                msg = _email.message_from_bytes(md[0][1])
                for _, addr in getaddresses([msg.get("To", "")]):
                    if "@" in addr:
                        out.add(addr.strip().lower())
        M.logout()
    except Exception:
        pass
    return out


def already_sent_emails() -> set:
    """Alle bereits kontaktierten E-Mails. Quelle 1: lokale Versand-Logs (persistente
    Server/lokal). Quelle 2: IONOS Sent-Ordner (ueberlebt stateless Cloud-Container)."""
    out = set()
    for p in sorted(LEAD_DIR.glob("outreach_sent_log_*.csv")):
        try:
            for r in csv.DictReader(p.open(encoding="utf-8")):
                if r.get("status") == "sent" and r.get("email"):
                    out.add(r["email"].strip().lower())
        except Exception:
            continue
    out |= already_sent_via_imap()
    return out


def new_log_path() -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    return LEAD_DIR / f"outreach_sent_log_{ts}.csv"


def build_msg(r: dict, sender: str) -> MIMEText:
    pitch = PITCH.get(r.get("zielgruppe", ""), DEFAULT_PITCH)
    msg = MIMEText(BODY.format(firma=r.get("firma", ""), region=r.get("region", ""), pitch=pitch), "plain", "utf-8")
    msg["Subject"] = SUBJECT.format(region=r.get("region", ""))
    msg["From"] = formataddr(("Johnson Services", sender))
    msg["To"] = r["email"]
    msg["Reply-To"] = sender
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="johnson-services.de")
    return msg


def send_leads(leads: list[dict], log_path: Path, do_send: bool) -> tuple[int, int]:
    """Sendet (oder Dry-Run) personalisierte Mails via SMTP UND legt eine Kopie im
    IONOS-Sent-Ordner ab (sonst tauchen sie nicht in 'Gesendete Objekte' auf).
    Schreibt log_path. Gibt (ok, fail)."""
    server = imap = None
    sender = "info@johnson-services.de"
    if do_send:
        c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_SMTP_SERVER", "IONOS_SMTP_PORT",
                    "IONOS_IMAP_SERVER", "IONOS_IMAP_PORT")
        sender = c["IONOS_EMAIL"]
        server = smtplib.SMTP(c["IONOS_SMTP_SERVER"], int(c["IONOS_SMTP_PORT"]), timeout=30)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
        try:
            imap = imaplib.IMAP4_SSL(c["IONOS_IMAP_SERVER"], int(c["IONOS_IMAP_PORT"]))
            imap.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
        except Exception:
            imap = None
    rows, ok, fail = [], 0, 0
    for i, r in enumerate(leads, 1):
        status = "dry-run"
        if do_send:
            msg = build_msg(r, sender)
            try:
                server.send_message(msg)
                status = "sent"
                ok += 1
                if imap:
                    try:
                        imap.append(f'"{SENT_FOLDER}"', "\\Seen", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
                    except Exception:
                        pass
            except Exception as e:
                status = f"error:{type(e).__name__}"
                fail += 1
        rows.append({"firma": r.get("firma", ""), "email": r["email"], "zielgruppe": r.get("zielgruppe", ""),
                     "region": r.get("region", ""), "subject": SUBJECT.format(region=r.get("region", "")),
                     "status": status, "sent_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        if do_send and i < len(leads):
            time.sleep(DELAY_S)
    if server:
        server.quit()
    if imap:
        try:
            imap.logout()
        except Exception:
            pass
    if rows:
        with log_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    return ok, fail


def main(argv: list[str]) -> int:
    load_env()
    do_send = "--send" in argv or os.environ.get("APPROVED_TO_SEND_OUTREACH") == "true"
    files = [a for a in argv if a.endswith(".csv")]
    src = Path(files[0]) if files else latest_batch_file()
    if not src or not src.exists():
        print("Keine Batch-Datei gefunden.")
        return 1
    leads = [r for r in csv.DictReader(src.open(encoding="utf-8")) if (r.get("email") or "").strip()]
    sent = already_sent_emails()
    leads = [l for l in leads if l["email"].strip().lower() not in sent]
    print(f"Quelle: {src.name} | {len(leads)} neue Leads mit E-Mail | Modus: {'ECHTER VERSAND' if do_send else 'DRY-RUN'}")
    if not leads:
        print("Nichts zu senden (alle bereits gesendet oder keine E-Mail).")
        return 0
    ok, fail = send_leads(leads, new_log_path(), do_send)
    for l in leads:
        print(f"  {'sent' if do_send and fail == 0 else ('dry-run' if not do_send else '?')}  {l['email']}")
    print(f"\n{'Gesendet' if do_send else 'Dry-Run'}: {ok} | Fehler: {fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
