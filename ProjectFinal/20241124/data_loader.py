import pandas as pd

DATA_PATH = "./data/"

def load_data():
    data = {
        "all_trading": pd.read_csv(f"{DATA_PATH}all_trading.csv", index_col=0, parse_dates=True),
        "foreign_agency_trading": pd.read_csv(f"{DATA_PATH}foreign_agency_trading.csv", index_col=0, parse_dates=True),
        "agency_trading": pd.read_csv(f"{DATA_PATH}agency_trading.csv", index_col=0, parse_dates=True),
    }
    return data
