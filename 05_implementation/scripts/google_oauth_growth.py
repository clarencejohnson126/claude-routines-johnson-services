"""Generate a Google OAuth refresh token scoped for the Growth Engine.

Fork of ../../Graph-Growth-Agents/scripts/generate_google_refresh_token.py,
extended from the adwords-only scope to Search Console + GA4 + Business Profile.

Needs in .env:
    GOOGLE_OAUTH_CLIENT_ID      (provided by user)
    GOOGLE_OAUTH_CLIENT_SECRET  (PENDING — ask user)
    GOOGLE_OAUTH_SCOPES         (comma-separated; default below)

Sign in with johnson.services.rheinneckar@gmail.com when the browser opens.
Copy the printed refresh token into .env as GOOGLE_GROWTH_REFRESH_TOKEN
(this script only PRINTS it; it does not write .env).

Usage:
    python3 google_oauth_growth.py
"""
from __future__ import annotations

import sys

from env_loader import load_env, require

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/business.manage",
]


def main() -> int:
    load_env()
    creds = require("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET")
    import os

    scopes = os.environ.get("GOOGLE_OAUTH_SCOPES", "")
    scope_list = [s.strip() for s in scopes.split(",") if s.strip()] or DEFAULT_SCOPES

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Missing dep. Install with: pip3 install google-auth-oauthlib")
        return 1

    client_config = {
        "installed": {
            "client_id": creds["GOOGLE_OAUTH_CLIENT_ID"],
            "client_secret": creds["GOOGLE_OAUTH_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(client_config, scopes=scope_list)
    print("\nOpening browser for OAuth consent...")
    print(f"Sign in with: {os.environ.get('GOOGLE_OAUTH_LOGIN_EMAIL', '(see .env)')}")
    print("Scopes:", ", ".join(scope_list), "\n")

    creds_obj = None
    last_err = None
    for port in (0, 8765, 8090, 9090):
        try:
            creds_obj = flow.run_local_server(
                port=port, prompt="consent", access_type="offline",
                authorization_prompt_message="Visit this URL if browser does not open:\n{url}",
                success_message="Authentication complete. You may close this window.",
                open_browser=True,
            )
            break
        except OSError as exc:
            last_err = exc
            print(f"  port {port or 'auto'} unavailable: {exc} — trying next...")
    if creds_obj is None:
        raise RuntimeError(f"Could not bind a local port. Last error: {last_err}")

    token = creds_obj.refresh_token
    if os.environ.get("WRITE_ENV") == "1":
        from env_loader import ENV_PATH
        lines = ENV_PATH.read_text().splitlines()
        found = False
        for i, ln in enumerate(lines):
            if ln.startswith("GOOGLE_GROWTH_REFRESH_TOKEN="):
                lines[i] = "GOOGLE_GROWTH_REFRESH_TOKEN=" + token
                found = True
        if not found:
            lines.append("GOOGLE_GROWTH_REFRESH_TOKEN=" + token)
        ENV_PATH.write_text("\n".join(lines) + "\n")
        ENV_PATH.chmod(0o600)
        print("\nSUCCESS — refresh token in .env geschrieben (GOOGLE_GROWTH_REFRESH_TOKEN). Wert nicht angezeigt.")
        print("Nächster Schritt: GA4_PROPERTY_ID setzen, dann python3 gsc_audit.py")
    else:
        print("\n" + "=" * 60)
        print("SUCCESS — paste this into .env as GOOGLE_GROWTH_REFRESH_TOKEN")
        print("=" * 60)
        print(f"\nGOOGLE_GROWTH_REFRESH_TOKEN={token}\n")
        print("Then set GA4_PROPERTY_ID and run: python3 gsc_audit.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
