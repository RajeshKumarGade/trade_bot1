from config.settings import INITIAL_SL_PCT, TARGET_PCT, TRAIL_GAP_PCT
from utils.logger import log_trade

positions = {}


def place_order(kite, symbol, signal, price):
    print(f"{signal} ORDER at {price}")
    positions[symbol] = {
        "entry": price,
        "sl": price * (1 - INITIAL_SL_PCT),
        "highest": price,
        "target_hit": False,
    }
    log_trade(symbol, signal, price)


def manage_position(symbol, current_price):
    pos = positions.get(symbol)
    if not pos:
        return False

    entry = pos["entry"]
    if current_price > pos["highest"]:
        pos["highest"] = current_price

    if not pos["target_hit"] and current_price >= entry * (1 + TARGET_PCT):
        pos["target_hit"] = True

    if pos["target_hit"]:
        trailing_sl = pos["highest"] * (1 - TRAIL_GAP_PCT)
        pos["sl"] = max(pos["sl"], trailing_sl)

    if current_price <= pos["sl"]:
        print(f"EXIT {symbol} at {current_price}")
        del positions[symbol]
        return True

    return False
