from config.settings import OPTION_ITM_DISTANCE


def get_option_symbol(kite, instrument_df, option_type):
    if option_type not in ("CE", "PE"):
        raise ValueError(f"Invalid option type: {option_type}")

    spot = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]

    strike = round(spot / 100) * 100

    if option_type == "CE":
        strike -= OPTION_ITM_DISTANCE
    else:
        strike += OPTION_ITM_DISTANCE

    options = instrument_df[
        (instrument_df["name"] == "NIFTY") &
        (instrument_df["strike"] == strike) &
        (instrument_df["instrument_type"] == option_type)
    ]

    options = options.sort_values("expiry")
    if options.empty:
        raise RuntimeError(f"No option contract found for strike {strike} {option_type}")

    return options.iloc[0]
