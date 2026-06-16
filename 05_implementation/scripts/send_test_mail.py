"""Send ONE outreach preview test mail to the own IONOS address.

Approved 2026-06-15 (Outreach-Testmail). Sends to info@johnson-services.de only,
clearly marked [TEST]. NO sending to leads. Real send to leads stays a separate
approval gate (APPROVED_TO_SEND_OUTREACH=true).

Usage:
    python3 send_test_mail.py
"""
from __future__ import annotations

import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from email.utils import formataddr

from env_loader import require

BODY = """Sehr geehrte Damen und Herren,

wenn bei Ihnen eine Wohnung kurzfristig geräumt und besenrein übergeben werden
muss, springt Johnson Services schnell und planbar ein.

Wir übernehmen Entrümpelung, Haushaltsauflösung und Wohnungsauflösung in Mannheim
und Umgebung, auf Wunsch inklusive Reinigung, damit die Einheit direkt wieder
vermietbar ist. Feste Preiszusage vorab, keine Nachforderungen, Termin in der
Regel innerhalb weniger Tage.

Dürfen wir Ihnen ein unverbindliches Angebot für Ihren nächsten Fall machen?
Eine kurze Rückmeldung oder ein Anruf genügt.

Mit freundlichen Grüßen
Clarence Johnson
Johnson Services, Mannheim (seit 2011)
Tel/WhatsApp: +49 151 57731682
info@johnson-services.de · johnson-services.de

------------------------------------------------------------
Hinweis: Dies ist eine TEST-Vorschau an die eigene Adresse zur Format- und
Zustellkontrolle. Es wurde NICHTS an Leads gesendet.
"""


def main() -> int:
    c = require("IONOS_EMAIL", "IONOS_EMAIL_PASSWORD", "IONOS_SMTP_SERVER", "IONOS_SMTP_PORT")
    recipient = "info@johnson-services.de"
    msg = MIMEText(BODY, "plain", "utf-8")
    msg["Subject"] = "[TEST] Outreach-Vorschau Johnson Services"
    msg["From"] = formataddr(("Johnson Services", c["IONOS_EMAIL"]))
    msg["To"] = recipient
    try:
        with smtplib.SMTP(c["IONOS_SMTP_SERVER"], int(c["IONOS_SMTP_PORT"]), timeout=30) as s:
            s.ehlo()
            s.starttls(context=ssl.create_default_context())
            s.login(c["IONOS_EMAIL"], c["IONOS_EMAIL_PASSWORD"])
            s.send_message(msg)
    except Exception as e:
        print(f"FEHLER beim Versand: {type(e).__name__}: {str(e)[:160]}")
        return 1
    print(f"✅ Testmail gesendet an {recipient} (Betreff: [TEST] Outreach-Vorschau Johnson Services)")
    print("   Bitte Posteingang prüfen: Zustellung, Formatierung, Absender, Spam-Ordner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
