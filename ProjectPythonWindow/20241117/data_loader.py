# data_loader.py

import pandas as pd

class DataLoader:
    def __init__(self, data_path="data/"):
        self.trading_data_path = f"{data_path}foreign_agency_trading_summary.csv"
        self.price_data_path = f"{data_path}closing_price.csv"
        
    def load_trading_data(self):
        return pd.read_csv(self.trading_data_path, index_col=0, parse_dates=True)

    def load_price_data(self):
        return pd.read_csv(self.price_data_path, index_col=0, parse_dates=True)