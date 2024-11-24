def calculate_buy_sell_ratio(data, stock):
    monthly_sum = data.groupby(data.index.to_period("M")).sum()
    monthly_ratio = {
        "Foreign Agency": monthly_sum["Foreign Agency"] / monthly_sum["All Investors"],
        "Agency": monthly_sum["Agency"] / monthly_sum["All Investors"],
    }
    return monthly_ratio
