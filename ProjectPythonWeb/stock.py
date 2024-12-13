# Perplexity 協作的版本，改自能及時從FinLab API下載的stock3.py（由Tom開發）
# 未解決日期顯示問題；能產出進階功能分析"主力買超比例"、"顯示主力買超前15名"

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
import finlab
from finlab import data
from dotenv import load_dotenv
import os

# Load environment variables and set up finlab
load_dotenv()
finlab.login(os.getenv('FINLAB_API_KEY'))
data.set_storage(data.FileStorage(path="D:\\pickle"))

# Load stock list
def get_stock_list_from_excel():
    try:
        df = pd.read_excel("./data/tw_stock_topics.xlsx")
        return [f"{row['stock_no']} {row['stock_name']}" for index, row in df.iterrows()]
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

# Load data
def load_data():
    try:
        foreign = data.get('institutional_investors_trading_summary:外陸資買賣超股數(不含外資自營商)')
        foreign_dealer = data.get('institutional_investors_trading_summary:外資自營商買賣超股數')
        foreign_total = foreign.fillna(0) + foreign_dealer.fillna(0)
        investment_trust = data.get('institutional_investors_trading_summary:投信買賣超股數')
        dealer = data.get('institutional_investors_trading_summary:自營商買賣超股數(自行買賣)')
        close_price = data.get("price:收盤價")
        volume = data.get("price:成交股數")
        
        return {
            "foreign_trading": foreign_total,
            "investment_trust_trading": investment_trust.fillna(0),
            "dealer_trading": dealer.fillna(0),
            "close_price": close_price,
            "volume": volume
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

# Initialize the Dash app
app = dash.Dash(__name__)

# Load data
stock_data = load_data()
stock_list = get_stock_list_from_excel()

# App layout
app.layout = html.Div([
    html.H1("國內外投信股票買賣查詢系統"),
    
    html.Div([
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': stock, 'value': stock} for stock in stock_list],
            value=stock_list[0] if stock_list else None,
            style={'width': '50%'}
        ),
        html.Button('分析主力買超比例', id='analyze-button', n_clicks=0),
        html.Button('顯示主力買超前15名', id='top-stocks-button', n_clicks=0),
    ]),
    
    html.Div([
        html.H2("三大法人買賣超資訊"),
        dash_table.DataTable(
            id='stock-table',
            columns=[
                {"name": "月份", "id": "Month"},
                {"name": "外資買賣超", "id": "Foreign"},
                {"name": "投信買賣超", "id": "Investment Trust"},
                {"name": "自營商買賣超", "id": "Dealer"}
            ],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center'}
        ),
    ]),
    
    dcc.Graph(id='stock-graph'),
    
    html.Div(id='analysis-output'),
    html.Div(id='top-stocks-output')
])

# Callback for updating stock data
@app.callback(
    [Output('stock-table', 'data'),
     Output('stock-graph', 'figure')],
    [Input('stock-dropdown', 'value')]
)
def update_stock_data(selected_stock):
    if not selected_stock:
        return [], {}
    
    stock_code = selected_stock.split()[0]
    
    # Process monthly data
    monthly_data = pd.DataFrame({
        "Foreign": stock_data["foreign_trading"][stock_code],
        "Investment Trust": stock_data["investment_trust_trading"][stock_code],
        "Dealer": stock_data["dealer_trading"][stock_code],
    }).fillna(0)
    
    monthly_data = monthly_data.resample("ME").sum()
    monthly_data = monthly_data.sort_index(ascending=False)
    monthly_data.index = monthly_data.index.strftime("%Y-%m")
    monthly_data = monthly_data.round().astype(int)
    
    for col in monthly_data.columns:
        monthly_data[col] = monthly_data[col].apply(lambda x: f"{x/1000:,.0f}")
    
    table_data = monthly_data.reset_index().to_dict('records')
    
    # Create graph
    price_data = stock_data["close_price"][stock_code]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_data.index, y=price_data, name="收盤價", line=dict(color='black', width=2)))
    
    for col, color in zip(["Foreign", "Investment Trust", "Dealer"], ['red', 'green', 'blue']):
        values = monthly_data[col].str.replace(",", "").astype(float)
        fig.add_trace(go.Bar(x=monthly_data.index, y=values, name=col, marker_color=color))
    
    fig.update_layout(
        title=f"{selected_stock} 股價與三大法人買賣超趨勢",
        xaxis_title="月份",
        yaxis_title="股價 / 買賣超張數",
        barmode='group'
    )
    
    return table_data, fig

# Callback for analyzing institutional ratio
@app.callback(
    Output('analysis-output', 'children'),
    [Input('analyze-button', 'n_clicks')],
    [State('stock-dropdown', 'value')]
)
def analyze_institutional_ratio(n_clicks, selected_stock):
    if n_clicks == 0 or not selected_stock:
        return html.Div()
    
    stock_code = selected_stock.split()[0]
    
    latest_data = pd.DataFrame({
        'foreign': stock_data['foreign_trading'][stock_code],
        'trust': stock_data['investment_trust_trading'][stock_code],
        'dealer': stock_data['dealer_trading'][stock_code],
        'volume': stock_data['volume'][stock_code]
    }).tail(20)
    
    latest_data['foreign_ratio'] = latest_data['foreign'] / latest_data['volume'] * 100
    latest_data['trust_ratio'] = latest_data['trust'] / latest_data['volume'] * 100
    latest_data['total_ratio'] = (latest_data['foreign'] + latest_data['trust'] + latest_data['dealer']) / latest_data['volume'] * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=latest_data.index, y=latest_data['foreign_ratio'], name='外資買超比例', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=latest_data.index, y=latest_data['trust_ratio'], name='投信買超比例', line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=latest_data.index, y=latest_data['total_ratio'], name='三大法人買超比例', line=dict(color='blue', width=2)))
    
    fig.update_layout(
        title=f"{selected_stock} 近20日主力買超比例",
        xaxis_title="日期",
        yaxis_title="買超比例(%)"
    )
    
    return dcc.Graph(figure=fig)

# Callback for showing top stocks
@app.callback(
    Output('top-stocks-output', 'children'),
    [Input('top-stocks-button', 'n_clicks')]
)
def show_top_stocks(n_clicks):
    if n_clicks == 0:
        return html.Div()
    
    all_stocks_data = pd.DataFrame()
    
    for stock in stock_list:
        stock_code = stock.split()[0]
        try:
            foreign = stock_data['foreign_trading'][stock_code].tail(20).sum()
            trust = stock_data['investment_trust_trading'][stock_code].tail(20).sum()
            dealer = stock_data['dealer_trading'][stock_code].tail(20).sum()
            
            all_stocks_data.loc[stock, '外資買超'] = foreign
            all_stocks_data.loc[stock, '投信買超'] = trust
            all_stocks_data.loc[stock, '自營商買超'] = dealer
            all_stocks_data.loc[stock, '三大法人買超'] = foreign + trust + dealer
        except Exception:
            continue
    
    top_15 = all_stocks_data.nlargest(15, '三大法人買超')
    
    table_data = [
        {
            "Rank": rank,
            "Stock": idx,
            "Foreign": f"{row['外資買超']/1000:,.0f}",
            "Trust": f"{row['投信買超']/1000:,.0f}",
            "Dealer": f"{row['自營商買超']/1000:,.0f}",
            "Total": f"{row['三大法人買超']/1000:,.0f}"
        }
        for rank, (idx, row) in enumerate(top_15.iterrows(), 1)
    ]
    
    return html.Div([
        html.H2("近20日主力買超排行榜"),
        dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "排名", "id": "Rank"},
                {"name": "股票", "id": "Stock"},
                {"name": "外資買超", "id": "Foreign"},
                {"name": "投信買超", "id": "Trust"},
                {"name": "自營商買超", "id": "Dealer"},
                {"name": "三大法人買超", "id": "Total"}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'}
        ),
        html.P("註：買超單位為張", style={'fontSize': 12})
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
