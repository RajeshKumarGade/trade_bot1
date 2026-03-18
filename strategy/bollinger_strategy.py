from tvDatafeed import TvDatafeed, Interval
from config.settings import BB_PERIOD, BB_STD

tv = TvDatafeed()


def check_signal():
    df = tv.get_hist(
        symbol="NIFTY",
        exchange="NSE",
        interval=Interval.in_5_minute,
        n_bars=50
    )
    if df is None or len(df) < max(BB_PERIOD + 3, 25):
        return None, None

    df["sma"] = df["close"].rolling(BB_PERIOD).mean()
    df["std"] = df["close"].rolling(BB_PERIOD).std()
    df["upper"] = df["sma"] + BB_STD * df["std"]
    df["lower"] = df["sma"] - BB_STD * df["std"]

    p1 = df.iloc[-2]
    p2 = df.iloc[-3]
    p3 = df.iloc[-4]

    candle_time = df.index[-2]

    if p1["close"] > p1["upper"] and (p2["close"] < p2["upper"] or p3["close"] < p3["upper"]):
        return "CE", candle_time

    if p1["close"] < p1["lower"] and (p2["close"] > p2["lower"] or p3["close"] > p3["lower"]):
        return "PE", candle_time

    return None, candle_time
