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
    })

    # Handle NaN values: Replace with 0
    table_data = table_data.fillna(0)

    # Sort data by date descending
    table_data = table_data.sort_index(ascending=False)

    # Format values with thousand separators and round to integers
    table_data["All Investors"] = table_data["All Investors"].apply(lambda x: f"{int(x):,}")
    table_data["Foreign Agency"] = table_data["Foreign Agency"].apply(lambda x: f"{int(x):,}")
    table_data["Agency"] = table_data["Agency"].apply(lambda x: f"{int(x):,}")

    return table_data.values.tolist(), table_data
