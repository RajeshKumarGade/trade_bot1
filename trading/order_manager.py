from config.settings import LOT_SIZE


def place_buy_order(kite, symbol):
    # Paper mode: keep this disabled for live-market backtesting period.
    # order_id = kite.place_order(
    #     variety=kite.VARIETY_REGULAR,
    #     exchange=kite.EXCHANGE_NFO,
    #     tradingsymbol=symbol,
    #     transaction_type=kite.TRANSACTION_TYPE_BUY,
    #     quantity=LOT_SIZE,
    #     product=kite.PRODUCT_MIS,
    #     order_type=kite.ORDER_TYPE_MARKET
    # )
    # return order_id
    print(f"[PAPER] BUY signal captured for {symbol}, qty={LOT_SIZE}")
    return f"PAPER_BUY_{symbol}"
