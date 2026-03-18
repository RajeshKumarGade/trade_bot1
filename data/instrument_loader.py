def get_nifty_options(instrument_df):

    return instrument_df[
        instrument_df["name"] == "NIFTY"
    ]