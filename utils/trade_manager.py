import datetime

last_candle = None
in_trade = False

def can_trade(signal, candle_time):
    global last_candle, in_trade

    if signal is None:
        return False

    if in_trade:
        return False

    if last_candle == candle_time:
        return False

    return True


def mark_trade(candle_time):
    global last_candle, in_trade
    last_candle = candle_time
    in_trade = True


def clear_trade():
    global in_trade
    in_trade = False