import pandas as pd
from kiteconnect import KiteConnect

from auth.credentials import read_credentials
from auth.token_manager import get_access_token


def read_access_session():
    access_token = get_access_token()
    key_secret = read_credentials()

    kite = KiteConnect(api_key=key_secret[0])
    kite.set_access_token(access_token)

    print("Downloading instrument dump...")
    instrument_dump = kite.instruments("NFO")
    instrument_df = pd.DataFrame(instrument_dump)

    return key_secret, access_token, kite, instrument_dump, instrument_df


# Backward-compat alias for older imports.
def readAccessToken():
    return read_access_session()
