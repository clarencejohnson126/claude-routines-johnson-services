#!/bin/bash
# One-shot 08:00 sender for the first Johnson B2B outreach batch.
# Runs send_outreach_batch.py --send once, then removes its own launchd job
# so it never repeats. Double-send is additionally blocked by the script's
# idempotency guard (sent-log check).
set -u
PLIST="$HOME/Library/LaunchAgents/com.johnson.outreach.batch1.plist"
DIR="/Users/clarence/Desktop/AUTOMATED ADS/Agentic Johnson Services/05_implementation/scripts"
LOGF="/tmp/johnson_outreach_batch1.log"
PY=/usr/local/bin/python3
[ -x "$PY" ] || PY="$(command -v python3)"

echo "=== $(date) START outreach batch1 (py=$PY) ===" >> "$LOGF"
cd "$DIR" || { echo "cd failed" >> "$LOGF"; exit 1; }
"$PY" send_outreach_batch.py --send >> "$LOGF" 2>&1
echo "=== $(date) DONE ===" >> "$LOGF"

# run only once: delete plist + unload self
/bin/rm -f "$PLIST"
/bin/launchctl bootout "gui/$(id -u)/com.johnson.outreach.batch1" 2>/dev/null || true
