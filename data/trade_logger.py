import pandas as pd
import os
from datetime import datetime
from config.settings import TRADE_LOG_FILE


def log_trade(symbol, entry, exit_price, reason):

    pnl = exit_price - entry

    row = pd.DataFrame(
        [[datetime.now(), symbol, entry, exit_price, pnl, reason]],
        columns=["Time", "Symbol", "Entry", "Exit", "PnL", "ExitReason"]
    )

    if not os.path.exists(TRADE_LOG_FILE):
        row.to_csv(TRADE_LOG_FILE, index=False)
    else:
        row.to_csv(TRADE_LOG_FILE, mode="a", header=False, index=False)
