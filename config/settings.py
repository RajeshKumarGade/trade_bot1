import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _int_env(name, default):
    value = os.getenv(name)
    return int(value) if value is not None else default


def _float_env(name, default):
    value = os.getenv(name)
    return float(value) if value is not None else default


DATA_DIR = Path(os.getenv("DATA_DIR", ".")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# API / auth files (used as fallback when env credentials are not provided)
API_KEY_FILE = str(DATA_DIR / os.getenv("API_KEY_FILE_NAME", "api_key.txt"))
ACCESS_TOKEN_FILE = str(DATA_DIR / os.getenv("ACCESS_TOKEN_FILE_NAME", "access_token.txt"))
REQUEST_TOKEN_FILE = str(DATA_DIR / os.getenv("REQUEST_TOKEN_FILE_NAME", "request_token.txt"))

# Trading
LOT_SIZE = _int_env("LOT_SIZE", 50)
OPTION_ITM_DISTANCE = _int_env("OPTION_ITM_DISTANCE", 500)

# Strategy
BB_PERIOD = _int_env("BB_PERIOD", 20)
BB_STD = _float_env("BB_STD", 2.0)

# Risk management
INITIAL_SL_PCT = _float_env("INITIAL_SL_PCT", 0.02)
TARGET_PCT = _float_env("TARGET_PCT", 0.05)
TRAIL_GAP_PCT = _float_env("TRAIL_GAP_PCT", 0.02)

# Polling / execution
MAIN_LOOP_SLEEP_SECONDS = _int_env("MAIN_LOOP_SLEEP_SECONDS", 1)
SIGNAL_CHECK_WINDOW_SECONDS = _int_env("SIGNAL_CHECK_WINDOW_SECONDS", 5)
SIGNAL_INTERVAL_MINUTES = _int_env("SIGNAL_INTERVAL_MINUTES", 5)

# Files
TRADE_LOG_FILE = str(DATA_DIR / os.getenv("TRADE_LOG_FILE_NAME", "trade_history.csv"))

# Trading time (exchange-local time)
MARKET_START = os.getenv("MARKET_START", "09:30")
MARKET_END = os.getenv("MARKET_END", "15:15")
MARKET_TIMEZONE = os.getenv("MARKET_TIMEZONE", "Asia/Kolkata")
