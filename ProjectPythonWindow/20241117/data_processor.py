# data_processor.py

import pandas as pd

class DataProcessor:
    def __init__(self, trading_data, price_data):
        self.trading_data = trading_data
        self.price_data = price_data
    
    def calculate_top_stocks(self, institution, time_range, time_span, top_n):
        # 選取近一年或近一月的資料
        date_range = pd.to_datetime("2024-10-31")  # 當前時間
        if time_range == "近一月":
            start_date = date_range - pd.DateOffset(months=1)
        else:  # "近一年"
            start_date = date_range - pd.DateOffset(years=1)
        
        # 篩選時間範圍
        trading_data_filtered = self.trading_data.loc[start_date:date_range]
        price_data_filtered = self.price_data.loc[start_date:date_range]
        
        # 計算買賣超股數*收盤價，並每月加總
        combined_data = trading_data_filtered * price_data_filtered
        monthly_data = combined_data.resample(time_span).sum()
        
        # 計算加總值並找出前N大股票
        top_stocks = monthly_data.sum().nlargest(top_n)
        return top_stocks, monthly_data[top_stocks.index]