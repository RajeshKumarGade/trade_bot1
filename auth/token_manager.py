import os
from pathlib import Path

from config.settings import ACCESS_TOKEN_FILE

TOKEN_ENV_KEYS = [
    "KITE_ACCESS_TOKEN",
    "ACCESS_TOKEN",
    "ZERODHA_ACCESS_TOKEN",
    "RAILWAY_KITE_ACCESS_TOKEN",
]


def _sanitize_token(value):
    token = (value or "").strip()
    if (
        len(token) >= 2
        and token[0] == token[-1]
        and token[0] in ("'", '"')
    ):
        token = token[1:-1].strip()
    return token


def _token_from_env():
    for key in TOKEN_ENV_KEYS:
        token = _sanitize_token(os.getenv(key))
        if token:
            print(f"Using access token from environment key: {key}")
            return token
    return ""


def _token_from_file():
    token_file = Path(ACCESS_TOKEN_FILE)
    if not token_file.exists():
        return ""
    token = _sanitize_token(token_file.read_text(encoding="utf-8"))
    if token:
        print(f"Using access token from file: {token_file}")
    return token


def get_access_token():
    token = _token_from_env()
    if token:
        return token

    token = _token_from_file()
    if token:
        return token

    diagnostics = ", ".join(
        f"{key}={'set' if os.getenv(key) else 'missing'}" for key in TOKEN_ENV_KEYS
    )
    raise RuntimeError(
        "Access token not found in env or file. "
        f"Checked env keys: {diagnostics}. "
        f"Checked file: {ACCESS_TOKEN_FILE}."
    )
