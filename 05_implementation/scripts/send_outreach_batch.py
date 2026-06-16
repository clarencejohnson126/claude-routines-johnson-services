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
from email.message import EmailMessage
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


# Rotierende Praxis-Tipps (B2B, Sie-Form, KEINE erfundenen Zahlen). Pro Lauf rotiert.
TIPS = [
    "Vor der Räumung Zählerstände notieren und Schlüssel sowie wichtige Dokumente separat sichern, dann läuft die Übergabe reibungslos.",
    "Bei Nachlass- und Sterbefällen Wertgegenstände und persönliche Unterlagen vor der Entrümpelung getrennt sammeln.",
    "Eine besenreine Übergabe spart vor der Neuvermietung die separate Endreinigung.",
    "Sperrige Möbel vorab kurz fotografieren, so lässt sich der Räumungsaufwand schon vor dem Termin verlässlich einschätzen.",
    "Bei leerstehenden Einheiten gilt: je früher die Räumung terminiert ist, desto kürzer der Mietausfall.",
    "Messie- und Verwahrlosungsfälle planen wir diskret, ohne Aufsehen und mit fester Preiszusage.",
]
DISCOUNT_LINE = "10% Rabatt auf jedes Angebot"  # vom Inhaber freigegeben (2026-06-16)


def _pick_tip() -> str:
    return TIPS[datetime.now().timetuple().tm_yday % len(TIPS)]


def value_block_html(tip: str) -> str:
    """Gebrandeter Mehrwert-Block (Johnson-Blau #0066CC, Inline-CSS fuer E-Mail-Clients)."""
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:22px 0;">'
        '<tr><td style="background:#E6F0FA;border-radius:4px;padding:20px 22px;">'
        '<div style="font-size:12px;font-weight:700;letter-spacing:.5px;color:#0066CC;text-transform:uppercase;">Praxis-Tipp</div>'
        f'<div style="font-size:15px;color:#1F2937;margin:6px 0 16px;">{tip}</div>'
        f'<div style="font-size:16px;font-weight:800;color:#0F172A;">{DISCOUNT_LINE}</div>'
        '<div style="font-size:13px;color:#374151;margin:2px 0 14px;">für neue Partner aus Hausverwaltung, Verwaltung und Nachlass. Erwähnen Sie einfach diese E-Mail.</div>'
        '<a href="https://johnson-services.de/" style="display:inline-block;background:#0066CC;color:#ffffff;text-decoration:none;font-weight:600;font-size:14px;padding:11px 18px;border-radius:4px;">Kostenloses Festpreis-Angebot anfordern</a>'
        '<div style="font-size:13px;color:#16A34A;margin-top:14px;">&#10003; Festpreis &nbsp; &#10003; besenrein &nbsp; &#10003; kurzfristige Termine</div>'
        '</td></tr></table>'
    )


def build_html(firma: str, region: str, pitch: str, tip: str) -> str:
    body = BODY.format(firma=firma, region=region, pitch=pitch).strip()
    paras = "".join(f'<p style="margin:0 0 12px;">{p.strip().replace(chr(10), "<br>")}</p>' for p in body.split("\n\n") if p.strip())
    return (
        '<!doctype html><html lang="de"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        '<body style="margin:0;background:#F5F7FA;">'
        '<div style="max-width:560px;margin:0 auto;padding:24px;'
        "font-family:'Plus Jakarta Sans',system-ui,'Segoe UI',Roboto,Arial,sans-serif;"
        'color:#1F2937;font-size:15px;line-height:1.55;">'
        f'{paras}{value_block_html(tip)}'
        '</div></body></html>'
    )


def build_msg(r: dict, sender: str) -> EmailMessage:
    pitch = PITCH.get(r.get("zielgruppe", ""), DEFAULT_PITCH)
    firma, region = r.get("firma", ""), r.get("region", "")
    tip = _pick_tip()
    text_body = BODY.format(firma=firma, region=region, pitch=pitch)
    text_full = f"{text_body}\nPS: {DISCOUNT_LINE} für neue Partner. Praxis-Tipp: {tip}\n"
    msg = EmailMessage()
    msg["Subject"] = SUBJECT.format(region=region)
    msg["From"] = formataddr(("Johnson Services", sender))
    msg["To"] = r["email"]
    msg["Reply-To"] = sender
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="johnson-services.de")
    # Moderne, maximal kompatible Multipart-Alternative (quoted-printable, sauberer fuer Mobile-Clients)
    msg.set_content(text_full)
    msg.add_alternative(build_html(firma, region, pitch, tip), subtype="html")
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
