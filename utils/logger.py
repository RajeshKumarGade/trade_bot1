import csv
import os
from datetime import datetime

FILE_NAME = "trade_log.csv"


def log_trade(symbol, signal, price):

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Time", "Symbol", "Signal", "Price"])

        writer.writerow([
            datetime.now(),
            symbol,
            signal,
            price
        ])