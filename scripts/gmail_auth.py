"""
gmail_auth.py — First-run OAuth flow for Gmail access.

Run once per machine to authorize and save token:
    python scripts/gmail_auth.py

Reads credentials from environment:
    GMAIL_CLIENT_ID
    GMAIL_CLIENT_SECRET

Saves token to: data/gmail_token.json  (gitignored)
Token auto-refreshes on subsequent runs via gmail_scanner.py.
"""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

REPO_ROOT = Path(__file__).resolve().parent.parent
TOKEN_PATH = REPO_ROOT / "data" / "gmail_token.json"


def get_client_config() -> dict:
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise EnvironmentError(
            "GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set in environment.\n"
            "Run StudyBook env bootstrap first: pwsh scripts/env/env_setter.ps1"
        )
    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def run_auth_flow() -> Credentials:
    # Check for existing valid token
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        if creds and creds.valid:
            print(f"Token already valid: {TOKEN_PATH}")
            return creds
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
            _save_token(creds)
            print("Token refreshed.")
            return creds

    # Run full OAuth flow
    print("Starting OAuth flow — a browser window will open...")
    config = get_client_config()
    flow = InstalledAppFlow.from_client_config(config, SCOPES)
    creds = flow.run_local_server(port=0)
    _save_token(creds)
    print(f"Token saved to: {TOKEN_PATH}")
    return creds


def _save_token(creds: Credentials) -> None:
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())


if __name__ == "__main__":
    run_auth_flow()
    print("Auth complete. You can now run: python scripts/gmail_scanner.py")
