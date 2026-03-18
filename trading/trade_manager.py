from config.settings import INITIAL_SL_PCT, LOT_SIZE, TARGET_PCT
from data.trade_logger import log_trade
from execution.websocket_handler import PriceTracker


def place_sell_order(kite, symbol):
    # Paper mode: keep this disabled for live-market backtesting period.
    # return kite.place_order(
    #     variety=kite.VARIETY_REGULAR,
    #     exchange=kite.EXCHANGE_NFO,
    #     tradingsymbol=symbol,
    #     transaction_type=kite.TRANSACTION_TYPE_SELL,
    #     quantity=LOT_SIZE,
    #     product=kite.PRODUCT_MIS,
    #     order_type=kite.ORDER_TYPE_MARKET
    # )
    print(f"[PAPER] SELL signal captured for {symbol}, qty={LOT_SIZE}")
    return f"PAPER_SELL_{symbol}"


def manage_trade(kite, api_key, access_token, instrument_token, symbol, entry_price):
    initial_sl = entry_price * (1 - INITIAL_SL_PCT)
    target_price = entry_price * (1 + TARGET_PCT)

    state = {
        "sl_price": initial_sl,
        "exited": False,
    }

    def exit_trade(ws, last_price, reason):
        if state["exited"]:
            return
        state["exited"] = True

        place_sell_order(kite, symbol)
        log_trade(symbol=symbol, entry=entry_price, exit_price=last_price, reason=reason)
        ws.stop()

    def on_price(ws, price):
        if price is None or state["exited"]:
            return

        if price <= state["sl_price"]:
            exit_trade(ws, price, "STOPLOSS")
            return

        if price >= target_price:
            exit_trade(ws, price, "TARGET")

    tracker = PriceTracker(
        api_key=api_key,
        access_token=access_token,
        instrument_token=instrument_token,
        on_price=on_price,
    )

    tracker.connect()
    tracker.wait()
