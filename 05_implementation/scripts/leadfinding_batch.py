"""Agent 002 — B2B Leadfinding batch (Spec: 20 Leads pro Lauf).

Findet neue B2B-Leads via Google Places API in den Zielgruppen, die in der
bestehenden contacts.csv (50 Leads, v.a. Hausverwaltungen) NOCH NICHT abgedeckt
sind. Dedupliziert gegen Bestand + innerhalb des Laufs. Erzeugt zusätzlich
personalisierte Outreach-Drafts (Sie-Form). KEIN Versand (Approval-Gate).

Usage:
    python3 leadfinding_batch.py [N]      # Standard N=20
"""
from __future__ import annotations

import csv
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from gmaps_scrape import best_effort_email, details, textsearch

PROOT = Path(__file__).resolve().parents[2]
ADS = Path(__file__).resolve().parents[3]
EXISTING = ADS / "Johnson-Services" / "outreach" / "contacts.csv"
EXISTING_REPO = PROOT / "05_implementation" / "data" / "contacts.csv"  # Cloud-Routine: contacts.csv im Repo (stateless)
LEAD_OUT = PROOT / "07_outputs" / "lead_lists"
MAIL_OUT = PROOT / "07_outputs" / "email_drafts"

# Zielgruppen, die im Bestand fehlen (Hausverwaltung ist bereits 40x abgedeckt)
QUERIES = [
    ("Hausverwaltung", "Hausverwaltung"),
    ("Immobilienmakler", "Immobilienmakler"),
    ("Seniorenheim/Pflege", "Seniorenheim Pflegeheim"),
    ("Nachlass/Erbrecht", "Nachlassverwalter Erbrecht Anwalt"),
    ("Facility Management", "Facility Management"),
    ("Wohnungsbaugesellschaft", "Wohnungsbaugesellschaft"),
]
REGIONS = ["Mannheim", "Heidelberg", "Ludwigshafen", "Viernheim", "Weinheim", "Schwetzingen", "Speyer", "Worms", "Darmstadt"]
CORE = {"Hausverwaltung", "Immobilienmakler", "Nachlass/Erbrecht", "Facility Management", "Wohnungsbaugesellschaft"}

PITCH = {
    "Hausverwaltung": "bei kurzfristiger Räumung und besenreiner Übergabe Ihrer Einheiten sind wir schnell und planbar zur Stelle",
    "Immobilienmakler": "vor Verkauf oder Neuvermietung räumen und reinigen wir Objekte besenrein, damit Sie schneller präsentieren können",
    "Seniorenheim/Pflege": "bei kurzfristiger Zimmer- oder Wohnungsräumung unterstützen wir Ihre Einrichtung zuverlässig",
    "Nachlass/Erbrecht": "bei Haushaltsauflösungen im Rahmen von Nachlässen arbeiten wir sorgfältig, diskret und mit fester Preiszusage",
    "Facility Management": "für Entrümpelung, Räumung und besenreine Übergabe Ihrer Objekte sind wir kurzfristig verfügbar",
    "Wohnungsbaugesellschaft": "bei Mieterwechsel und Räumungen sorgen wir für besenreine, sofort vermietbare Einheiten zum Festpreis",
}

SUFFIX = re.compile(r"\b(gmbh|mbh|co|kg|ohg|ug|e\.?k|e\.?g|ag|gbr|und|and|the)\b", re.I)


def norm(name: str) -> str:
    n = SUFFIX.sub(" ", (name or "").lower())
    return re.sub(r"[^a-z0-9]", "", n)


def load_existing() -> tuple[set, set]:
    """Dedup gegen Bestands-Leads + ALLE früheren Batches + Versand-Logs."""
    names, emails = set(), set()
    files = [EXISTING, EXISTING_REPO] + sorted(LEAD_OUT.glob("leads_batch_*.csv")) + sorted(LEAD_OUT.glob("outreach_sent_log_*.csv"))
    for p in files:
        if not p.exists():
            continue
        try:
            for r in csv.DictReader(p.open(encoding="utf-8")):
                if r.get("firma"):
                    names.add(norm(r["firma"]))
                if r.get("email"):
                    emails.add(r["email"].strip().lower())
        except Exception:
            continue
    return names, emails


def score(group: str, website: str, phone: str, email: str) -> tuple[int, str, str]:
    s = 60 + (15 if website else 0) + (15 if phone else 0) + (10 if email else 0)
    rel = "hoch" if (group in CORE and website) else "mittel"
    return min(s, 100), rel, ("qualified" if rel == "hoch" else "new")


def wait_for_network(host: str = "maps.googleapis.com", tries: int = 20, delay: int = 30) -> bool:
    """Wartet auf Netz/DNS (Mac wacht um 09:00 ggf. erst auf). Verhindert Leerlauf."""
    import socket
    for i in range(tries):
        try:
            socket.getaddrinfo(host, 443)
            return True
        except OSError:
            print(f"  Netz/DNS noch nicht bereit (Versuch {i + 1}/{tries}), warte {delay}s ...", flush=True)
            time.sleep(delay)
    print("ABBRUCH: Netz nach Wartezeit weiterhin nicht erreichbar.")
    return False


def main(target: int) -> int:
    if not wait_for_network():
        return 1
    ex_names, ex_emails = load_existing()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    day = now[:10]
    seen, rows = set(ex_names), []

    for region in REGIONS:
        for group, q in QUERIES:
            if len(rows) >= target:
                break
            try:
                results = textsearch(q, region)
            except Exception as e:
                print(f"  textsearch Fehler [{q} {region}]: {e}")
                continue
            picked = 0
            for res in results:
                if picked >= 2 or len(rows) >= target:
                    break
                name = (res.get("name") or "").strip()
                if not name or norm(name) in seen:
                    continue
                det = details(res["place_id"]) if res.get("place_id") else {}
                website = det.get("website", "")
                phone = det.get("formatted_phone_number", "")
                email = best_effort_email(website)
                if email and email.lower() in ex_emails:
                    continue
                sc, rel, status = score(group, website, phone, email)
                rows.append({
                    "firma": name, "zielgruppe": group, "region": region,
                    "website": website, "email": email, "kontakt_telefon": phone,
                    "ansprechpartner": "", "relevanz": rel, "lead_score": sc,
                    "status": status, "quelle": "Google Places API", "gefunden_am": now,
                })
                seen.add(norm(name))
                picked += 1
                time.sleep(0.2)

    if not rows:
        print("Keine neuen Leads gefunden.")
        return 1

    LEAD_OUT.mkdir(parents=True, exist_ok=True)
    csv_path = LEAD_OUT / f"leads_batch_{day}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Outreach-Drafts (Sie-Form, kein Versand)
    MAIL_OUT.mkdir(parents=True, exist_ok=True)
    md_path = MAIL_OUT / f"outreach_batch_{day}.md"
    lines = [
        f"# Outreach-Drafts {day} (Batch, {len(rows)} Leads) — KEIN Versand",
        "",
        "Status: Entwürfe. Versand ist Approval-Gate (`APPROVED_TO_SEND_OUTREACH=true`). Sie-Form. Quelle: Google Places API.",
        "Vor Versand: Ansprechpartner ergänzen, Do-not-contact + Opt-out prüfen.",
        "",
        "Signatur: Clarence Johnson · Johnson Services, Mannheim (seit 2011) · +49 151 57731682 · info@johnson-services.de",
        "",
    ]
    for r in rows:
        pitch = PITCH.get(r["zielgruppe"], "bei Entrümpelung, Räumung und besenreiner Übergabe unterstützen wir Sie zuverlässig")
        lines += [
            f"## {r['firma']} ({r['zielgruppe']}, {r['region']}) — Score {r['lead_score']}",
            f"- Web: {r['website'] or 'n/a'} · Mail: {r['email'] or 'n/a'} · Tel: {r['kontakt_telefon'] or 'n/a'}",
            "",
            f"**Betreff:** Zuverlässiger Partner für Entrümpelung und besenreine Übergabe in {r['region']}",
            "",
            "Sehr geehrte Damen und Herren,",
            "",
            f"Johnson Services unterstützt Unternehmen wie Ihres in {r['region']} und Umgebung: {pitch}. "
            "Feste Preiszusage nach kostenloser Besichtigung, kurzfristige Termine, besenreine Übergabe.",
            "",
            "Dürfen wir Ihnen bei Ihrem nächsten Fall ein unverbindliches Festpreis-Angebot machen? Eine kurze Rückmeldung genügt.",
            "",
            "---",
            "",
        ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    from collections import Counter
    print(f"✅ {len(rows)} neue Leads -> {csv_path.name}")
    print(f"✅ {len(rows)} Outreach-Drafts -> {md_path.name}")
    print("Zielgruppen:", dict(Counter(r["zielgruppe"] for r in rows)))
    print("Regionen:   ", dict(Counter(r["region"] for r in rows)))
    with_mail = sum(1 for r in rows if r["email"])
    print("Mit E-Mail: ", with_mail, "/", len(rows))

    # Auto-Versand wenn freigegeben (APPROVED_TO_SEND_OUTREACH=true) oder Test (=dry)
    flag = os.environ.get("APPROVED_TO_SEND_OUTREACH", "").lower()
    send_note = "Versand: aus (nur Drafts)"
    if flag in ("true", "dry"):
        try:
            from send_outreach_batch import already_sent_emails, new_log_path, send_leads
            sent_set = already_sent_emails()
            mail_rows = [r for r in rows if r["email"] and r["email"].strip().lower() not in sent_set]
            ok, fail = send_leads(mail_rows, new_log_path(), do_send=(flag == "true"))
            send_note = f"Versand: {'ECHT' if flag == 'true' else 'DRY'} ok={ok} fail={fail} ({len(mail_rows)} Adressen)"
        except Exception as e:
            send_note = f"Versand-FEHLER: {type(e).__name__}: {str(e)[:90]}"
    print(send_note)

    try:
        import notify
        zg = dict(Counter(r["zielgruppe"] for r in rows))
        notify.send(f"🧲 Outreach-Lauf {day}: {len(rows)} neue Leads ({with_mail} mit E-Mail)\n"
                    f"Zielgruppen: {zg}\n{send_note}\nDrafts: {md_path.name}")
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sys.exit(main(n))
