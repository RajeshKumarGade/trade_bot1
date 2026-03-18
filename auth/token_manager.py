import os

from kiteconnect import KiteConnect

from auth.credentials import read_credentials
from auth.auto_login import generate_access_token
from config.settings import ACCESS_TOKEN_FILE


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
    env_access_token = os.getenv("KITE_ACCESS_TOKEN")
    if env_access_token and is_token_working(env_access_token):
        print("Using KITE_ACCESS_TOKEN from environment")
        return env_access_token

    if os.path.exists(ACCESS_TOKEN_FILE):
        access_token = open(ACCESS_TOKEN_FILE).read().strip()
        print("Checking existing access token...")
        if is_token_working(access_token):
            print("Existing token is valid")
            return access_token
        print("Token expired or invalid. Regenerating...")
    else:
        print("Token file not found. Generating new token...")

    new_token = generate_access_token()
    if is_token_working(new_token):
        print("New token generated and verified")
        return new_token

    raise RuntimeError("Failed to generate valid access token")
