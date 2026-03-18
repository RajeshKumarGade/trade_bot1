import os

from config.settings import API_KEY_FILE


def read_credentials():
    api_key = os.getenv("KITE_API_KEY")
    api_secret = os.getenv("KITE_API_SECRET")
    user_id = os.getenv("KITE_USER_ID")
    password = os.getenv("KITE_PASSWORD")
    totp_secret = os.getenv("KITE_TOTP_SECRET")

    if api_key and api_secret:
        return [api_key, api_secret, user_id, password, totp_secret]

    key_secret = open(API_KEY_FILE).read().split()
    if len(key_secret) < 2:
        raise ValueError(
            "Set KITE_API_KEY/KITE_API_SECRET env vars or provide api_key.txt with api_key api_secret."
        )
    return key_secret
