import os

from kiteconnect import KiteConnect

from auth.credentials import read_credentials


def is_token_working(access_token):
    try:
        key_secret = read_credentials()
        kite = KiteConnect(api_key=key_secret[0])
        kite.set_access_token(access_token)
        kite.profile()
        return True
    except Exception as exc:
        print("Token invalid:", str(exc))
        return False


def get_access_token():
    env_access_token = os.getenv("KITE_ACCESS_TOKEN", "").strip()
    if not env_access_token:
        raise RuntimeError(
            "KITE_ACCESS_TOKEN is required. Generate a fresh access token daily and set it in Railway variables."
        )

    if not is_token_working(env_access_token):
        raise RuntimeError(
            "KITE_ACCESS_TOKEN is invalid/expired. Update Railway variable with a fresh token."
        )

    print("Using KITE_ACCESS_TOKEN from environment")
    return env_access_token
