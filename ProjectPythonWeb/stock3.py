from dotenv import load_dotenv
import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import finlab
from finlab import data
import os

# Initialize environment
os.system('cls')
load_dotenv()
finlab.login(os.getenv('FINLAB_API_KEY'))
data.set_storage(data.FileStorage(path="D:\pickle"))

# Global variables
close_price = pd.DataFrame()
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Load data using finlab API
def load_data():
    try:
        foreign = data.get(
            'institutional_investors_trading_summary:外陸資買賣超股數(不含外資自營商)')
        foreign_dealer = data.get(
            'institutional_investors_trading_summary:外資自營商買賣超股數')
        investment_trust = data.get(
            'institutional_investors_trading_summary:投信買賣超股數')
        dealer = data.get(
            'institutional_investors_trading_summary:自營商買賣超股數(自行買賣)')

        foreign_total = foreign.fillna(0) + foreign_dealer.fillna(0)
        global close_price
        close_price = data.get("price:收盤價")

        return {
            "foreign_trading": foreign_total,
            "investment_trust_trading": investment_trust.fillna(0),
            "dealer_trading": dealer.fillna(0)
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

data_dict = load_data()

# Load stock list from Excel
def get_stock_list_from_excel():
    try:
        df = pd.read_excel("./data/tw_stock_topics.xlsx")
        return [f"{row['stock_no']} {row['stock_name']}" for _, row in df.iterrows()]
    except Exception as e:
        print(f"Error reading stock list: {e}")
        return []

stock_list = get_stock_list_from_excel()

# Dash App
app = dash.Dash(__name__)
app.title = "Stock Analysis Dashboard"

app.layout = html.Div([
    html.Div([
        html.H2("國內外投信股票買賣查詢系統", style={"textAlign": "center"}),

        html.Label("選擇股票："),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{"label": stock, "value": stock.split()[0]} for stock in stock_list],
            value="2330",  # 預設選擇台積電
        ),
    ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

    html.Div([
        html.H3("三大法人買賣超資訊", style={"textAlign": "center"}),
        dash_table.DataTable(
            id='stock-table',
            columns=[
                {"name": "月份", "id": "Month"},
                {"name": "外資買賣超", "id": "Foreign"},
                {"name": "投信買賣超", "id": "Investment Trust"},
                {"name": "自營商買賣超", "id": "Dealer"}
            ],
            style_table={"overflowX": "auto", "overflowY": "auto", "height": "300px"},
            style_cell={"textAlign": "center"},
        ),

        html.H3("最近20日主力買超比例", style={"textAlign": "center"}),  # 標題格式統一
        dcc.Graph(id="main-force-plot", style={"height": "400px"})
    ], style={"width": "65%", "display": "inline-block", "padding": "20px"})
])

# Callbacks
@app.callback(
    [Output("stock-table", "data"), Output("main-force-plot", "figure")],
    [Input("stock-dropdown", "value")]
)
def display_stock_data(stock_code):
    if not stock_code:
        return [], go.Figure()

    try:
        # 三大法人買賣超資訊
        monthly_data = pd.DataFrame({
            "Foreign": data_dict["foreign_trading"][stock_code],
            "Investment Trust": data_dict["investment_trust_trading"][stock_code],
            "Dealer": data_dict["dealer_trading"][stock_code],
        }).fillna(0)

        monthly_data = monthly_data.resample("M").sum()
        monthly_data["Month"] = monthly_data.index.strftime("%Y-%m")
        monthly_data = monthly_data.iloc[::-1]  # 資料反向排序，最新資料在上
        table_data = monthly_data.reset_index().to_dict("records")

        # 最近20日主力買超比例
        volume = data.get("price:成交股數")
        daily_data = pd.DataFrame({
            "Foreign": data_dict["foreign_trading"][stock_code],
            "Investment Trust": data_dict["investment_trust_trading"][stock_code],
            "Dealer": data_dict["dealer_trading"][stock_code],
            "Volume": volume[stock_code]
        }).tail(20)

        daily_data["Total"] = daily_data["Foreign"] + daily_data["Investment Trust"] + daily_data["Dealer"]
        daily_data["Main Force Ratio"] = daily_data["Total"] / daily_data["Volume"] * 100

        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily_data.index, y=daily_data["Main Force Ratio"], name="主力買超比例"))
        fig.update_layout(
            title="最近20日主力買超比例",  # 恢復標題
            xaxis_title="日期",
            yaxis_title="買超比例 (%)"
        )

        return table_data, fig

    except Exception as e:
        print(f"Error processing stock data: {e}")
        return [], go.Figure()

if __name__ == "__main__":
    app.run_server(debug=True)