"""Weekly SEO report (Spec ch.10 recurring). Pulls live GSC + GA4, writes a
dated report and sends a Telegram summary. Read-only; no fabrication (graceful
PENDING if the token is missing).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import notify
from env_loader import load_env
from ga4_audit import run_report
from gsc_audit import _access_token, list_sites, query

OUT = Path(__file__).resolve().parents[2] / "07_outputs" / "seo_reports"


def main() -> int:
    load_env()
    token = _access_token()
    if not token:
        notify.send("SEO-Wochenreport: GSC/GA4-Token fehlt (pending). Kein Report erzeugt.")
        print("PENDING — kein Token")
        return 0

    sites = list_sites(token)
    urls = [s.get("siteUrl") for s in sites]
    prop = next((u for u in urls if "johnson-services.de" in (u or "")), None) or os.environ.get("GSC_PROPERTY", "")
    qrows = query(token, prop, "query", days=28, limit=30)
    prows = query(token, prop, "page", days=28, limit=20)
    quickwins = sorted([r for r in qrows if 5 <= r.get("position", 99) <= 20],
                       key=lambda r: -r.get("impressions", 0))[:8]
    clicks = sum(int(r.get("clicks", 0)) for r in qrows)
    impr = sum(int(r.get("impressions", 0)) for r in qrows)

    ga_prop = os.environ.get("GA4_PROPERTY_ID", "")
    sessions, channels = 0, []
    if ga_prop:
        try:
            d = run_report(token, ga_prop, {
                "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
                "dimensions": [{"name": "sessionDefaultChannelGroup"}],
                "metrics": [{"name": "sessions"}], "limit": 12,
            })
            for row in d.get("rows", []):
                ch = row["dimensionValues"][0]["value"]
                v = row["metricValues"][0]["value"]
                channels.append((ch, v))
                sessions += int(v)
        except Exception:
            pass

    now = datetime.now(timezone.utc).isoformat(timespec="minutes")
    daystr = now[:10]
    L = [f"# Wöchentlicher SEO-Report {daystr}", "",
         f"Quelle: GSC `{prop}` + GA4 `{ga_prop or 'n/a'}` (28 Tage). Stand {now}Z.", "",
         "## Kennzahlen (28 Tage)",
         f"- GSC Klicks: **{clicks}** | Impressionen: **{impr}**",
         f"- GA4 Sitzungen: **{sessions}**", "",
         "## Quick-Wins (Position 5-20, viel Nachfrage)"]
    L += [f"- {r['keys'][0]} — Pos {r.get('position',0):.1f}, {int(r.get('impressions',0))} Impr, {int(r.get('clicks',0))} Klicks" for r in quickwins] or ["- (keine im Bereich 5-20)"]
    L += ["", "## Top-Seiten"]
    L += [f"- {r['keys'][0]} — Pos {r.get('position',0):.1f}, {int(r.get('impressions',0))} Impr, {int(r.get('clicks',0))} Klicks"
          for r in sorted(prows, key=lambda r: -r.get("impressions", 0))[:10]]
    if channels:
        L += ["", "## GA4 Sitzungen nach Kanal"] + [f"- {c}: {v}" for c, v in channels]

    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"weekly_seo_report_{daystr}.md"
    p.write_text("\n".join(L), encoding="utf-8")
    top = "; ".join(f"{r['keys'][0]} (Pos {r.get('position',0):.0f})" for r in quickwins[:3])
    notify.send(f"📊 SEO-Wochenreport {daystr}\nKlicks {clicks} | Impr {impr} | GA4-Sitzungen {sessions}\nQuick-Wins: {top or 'n/a'}\nDatei: {p.name}")
    print("geschrieben:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
