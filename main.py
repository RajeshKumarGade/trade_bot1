import datetime as dt
import threading
import time
from zoneinfo import ZoneInfo

from auth.session import read_access_session
from config.settings import (
    MAIN_LOOP_SLEEP_SECONDS,
    MARKET_END,
    MARKET_START,
    MARKET_TIMEZONE,
    SIGNAL_CHECK_WINDOW_SECONDS,
    SIGNAL_INTERVAL_MINUTES,
)
from strategy.bollinger_strategy import check_signal
from trading.order_manager import place_buy_order
from trading.trade_manager import manage_trade
from utils.option_selector import get_option_symbol
from utils.trade_manager import can_trade, clear_trade, mark_trade


def _time_in_window(now):
    current = now.strftime("%H:%M")
    return MARKET_START <= current <= MARKET_END


def _market_now():
    return dt.datetime.now(ZoneInfo(MARKET_TIMEZONE))


def _start_trade_manager(
    kite, api_key, access_token, token, symbol, entry_price, candle_time
):
    try:
        manage_trade(kite, api_key, access_token, token, symbol, entry_price)
    finally:
        clear_trade()
        print(f"Trade lifecycle completed for candle {candle_time}")


def main():
    print("BUILD_MARKER: TOKEN_ENV_V3")
    key_secret, access_token, kite, _dump, instrument_df = read_access_session()
    api_key = key_secret[0]

    print("Trading bot started")

    while True:
        now = _market_now()

        if (
            _time_in_window(now)
            and now.minute % SIGNAL_INTERVAL_MINUTES == 0
            and now.second < SIGNAL_CHECK_WINDOW_SECONDS
        ):
            signal, candle_time = check_signal()

            if can_trade(signal, candle_time):
                option = get_option_symbol(kite, instrument_df, signal)
                symbol = option["tradingsymbol"]
                token = option["instrument_token"]

                place_buy_order(kite, symbol)
                mark_trade(candle_time)
                time.sleep(2)

                quote_key = f"NFO:{symbol}"
                entry_price = kite.ltp(quote_key)[quote_key]["last_price"]

                trade_thread = threading.Thread(
                    target=_start_trade_manager,
                    args=(
                        kite,
                        api_key,
                        access_token,
                        token,
                        symbol,
                        entry_price,
                        candle_time,
                    ),
                    daemon=True,
                )
                trade_thread.start()

        time.sleep(MAIN_LOOP_SLEEP_SECONDS)


if __name__ == "__main__":
    main()
