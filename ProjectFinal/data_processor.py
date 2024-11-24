import pandas as pd

def process_daily_data(data, stock):
    all_trading = data["all_trading"]
    foreign_agency_trading = data["foreign_agency_trading"]
    agency_trading = data["agency_trading"]

    # Filter data for the selected stock
    table_data = pd.DataFrame({
        "Date": all_trading.index,
        "All Investors": all_trading[stock],
        "Foreign Agency": foreign_agency_trading[stock],
        "Agency": agency_trading[stock],
    }).reset_index()

    plot_data = table_data.copy()
    return table_data.values.tolist(), plot_data
