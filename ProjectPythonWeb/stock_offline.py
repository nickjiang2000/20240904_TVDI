import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

DATA_PATH = "./data/"

# 載入數據
def load_data():
    return {
        "all_trading": pd.read_csv(f"{DATA_PATH}all_trading.csv", index_col=0, parse_dates=True),
        "foreign_agency_trading": pd.read_csv(f"{DATA_PATH}foreign_agency_trading.csv", index_col=0, parse_dates=True),
        "agency_trading": pd.read_csv(f"{DATA_PATH}agency_trading.csv", index_col=0, parse_dates=True),
    }

data = load_data()

# 初始化 Dash 應用
app = dash.Dash(__name__)

# 定義應用佈局
app.layout = html.Div([
    html.H1("國內外投信股票買賣查詢系統"),
    html.Div([
        html.Label("選擇股票"),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': col, 'value': col} for col in data["all_trading"].columns],
            value='2330 台積電'
        )
    ]),
    html.Div([
        html.H2("當月買賣股數"),
        dash_table.DataTable(
            id='stock-table',
            columns=[
                {"name": "Month", "id": "Month"},
                {"name": "All Investors", "id": "All Investors"},
                {"name": "Foreign Agency", "id": "Foreign Agency"},
                {"name": "Domestic Agency", "id": "Agency"}
            ],
            style_table={
                'height': '300px',  # 設置表格高度
                'overflowY': 'auto',  # 啟用垂直滾動
                'overflowX': 'auto'  # 啟用水平滾動
            },
            style_cell={
                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_header={
                'fontWeight': 'bold'
            }
        )
    ]),
    dcc.Graph(id='stock-graph')
])

# 回調函數來更新表格和圖表
@app.callback(
    [Output('stock-table', 'data'),
     Output('stock-graph', 'figure')],
    [Input('stock-dropdown', 'value')]
)
def update_data(selected_stock):
    # 處理數據
    monthly_data = pd.DataFrame({
        "All Investors": data["all_trading"][selected_stock],
        "Foreign Agency": data["foreign_agency_trading"][selected_stock],
        "Agency": data["agency_trading"][selected_stock],
    }).fillna(0)

    monthly_data = monthly_data.resample("ME").sum()
    monthly_data = monthly_data.sort_index(ascending=False)
    monthly_data.index = monthly_data.index.strftime("%Y-%m")
    monthly_data = monthly_data.round().astype(int)

    # 準備表格數據
    table_data = monthly_data.reset_index().to_dict('records')
    for row in table_data:
        row['All Investors'] = f"{row['All Investors']:,}"
        row['Foreign Agency'] = f"{row['Foreign Agency']:,}"
        row['Agency'] = f"{row['Agency']:,}"

    # 準備圖表數據
    plot_data = monthly_data.sort_index()
    figure = {
        'data': [
            go.Scatter(x=plot_data.index, y=plot_data['All Investors'], mode='lines+markers', name='All Investors'),
            go.Scatter(x=plot_data.index, y=plot_data['Foreign Agency'], mode='lines+markers', name='Foreign Agency'),
            go.Scatter(x=plot_data.index, y=plot_data['Agency'], mode='lines+markers', name='Domestic Agency')
        ],
        'layout': go.Layout(
            title='Monthly Stock Transactions Trend',
            xaxis={'title': 'Month'},
            yaxis={'title': 'Transaction Volume'},
            hovermode='closest'
        )
    }

    return table_data, figure

if __name__ == '__main__':
    app.run_server(debug=True)
