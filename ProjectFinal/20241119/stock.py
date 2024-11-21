import tkinter as tk
from tkinter import ttk
import pandas as pd
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constants
DATA_PATH = "./data/"
LOG_FILE = "log.txt"

class StockAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("法人歷史買賣超數據查詢系統")
        self.geometry("1200x700")
        
        self.create_left_panel()
        self.create_right_panel()
        self.initialize_data()
    
    def create_left_panel(self):
        """Create the left navigation panel."""
        self.left_panel = tk.Frame(self, width=250, bg="lightgray")
        self.left_panel.pack(side="left", fill="y")
        
        # Feature Selection
        self.feature_var = tk.StringVar(value="long_term_reference")
        tk.Label(self.left_panel, text="選擇功能", bg="lightgray").pack(pady=10)
        tk.Radiobutton(self.left_panel, text="長期選股參考－法人歷史買賣超數據統計",
                       variable=self.feature_var, value="long_term_reference",
                       bg="lightgray").pack(anchor="w")
        
        # Institution Selection
        self.institution_var = tk.StringVar(value="全市場")
        tk.Label(self.left_panel, text="法人選擇", bg="lightgray").pack(pady=10)
        institution_options = ["全市場", "外資投信", "外資自營", "自營", "投信"]
        self.institution_dropdown = ttk.Combobox(self.left_panel, textvariable=self.institution_var, values=institution_options)
        self.institution_dropdown.pack(fill="x")
        
        # Time Range Selection
        self.time_range_var = tk.StringVar(value="近一年")
        tk.Label(self.left_panel, text="時間範圍", bg="lightgray").pack(pady=10)
        time_range_options = ["近一年", "近三年", "近五年", "近十年"]
        self.time_range_dropdown = ttk.Combobox(self.left_panel, textvariable=self.time_range_var, values=time_range_options)
        self.time_range_dropdown.pack(fill="x")
        
        # X-axis Time Span Selection
        self.time_span_var = tk.StringVar(value="月")
        tk.Label(self.left_panel, text="X軸時間跨度", bg="lightgray").pack(pady=10)
        time_span_options = ["月", "季", "年"]
        self.time_span_dropdown = ttk.Combobox(self.left_panel, textvariable=self.time_span_var, values=time_span_options)
        self.time_span_dropdown.pack(fill="x")
        
        # Y-axis Top N Selection
        self.top_n_var = tk.StringVar(value="Top5")
        tk.Label(self.left_panel, text="Y軸前幾大股票", bg="lightgray").pack(pady=10)
        top_n_options = ["Top5", "Top10", "Top30"]
        self.top_n_dropdown = ttk.Combobox(self.left_panel, textvariable=self.top_n_var, values=top_n_options)
        self.top_n_dropdown.pack(fill="x")
        
        # Query Button
        tk.Button(self.left_panel, text="查詢", command=self.query_data).pack(pady=20)
        
        # Operation Time Label
        self.time_label = tk.Label(self.left_panel, text="", bg="lightgray")
        self.time_label.pack(pady=10)
    
    def create_right_panel(self):
        """Create the right panel for displaying data and charts."""
        self.right_panel = tk.Frame(self, bg="white")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Table Section
        self.table_frame = tk.Frame(self.right_panel)
        self.table_frame.pack(fill="x", pady=10)
        
        # Chart Section
        self.chart_frame = tk.Frame(self.right_panel)
        self.chart_frame.pack(fill="both", expand=True)
    
def initialize_data(self):
    """Initialize and load all necessary data."""
    try:
        file_mapping = {
            "外資投信": "foreign_agency_trading.csv",
            "外資自營": "foreign_self_trading.csv",
            "自營": "self_trading.csv",
            "投信": "agency_trading.csv",
            "全市場": "market.csv"
        }
        self.data = {}
        for institution, file_name in file_mapping.items():
            file_path = f"{DATA_PATH}{file_name}"
            self.data[institution] = pd.read_csv(file_path, index_col=0, parse_dates=True)
    except Exception as e:
        tk.messagebox.showerror("資料載入錯誤", f"無法載入資料: {e}")
    
    def query_data(self):
        """Handle data querying based on user selection."""
        start_time = time.time()
        
        institution = self.institution_var.get()
        time_range = self.time_range_var.get()
        time_span = self.time_span_var.get()
        top_n = int(self.top_n_var.get().replace("Top", ""))
        
        # Calculate date range
        end_date = pd.Timestamp("2024-10-31")
        if time_range == "近一年":
            start_date = end_date - pd.DateOffset(years=1)
        elif time_range == "近三年":
            start_date = end_date - pd.DateOffset(years=3)
        elif time_range == "近五年":
            start_date = end_date - pd.DateOffset(years=5)
        else:
            start_date = end_date - pd.DateOffset(years=10)
        
        # Load selected institution data and filter by date range
        df = self.data[institution]
        filtered_df = df.loc[start_date:end_date]
        
        # Aggregate data and find top N stocks
        aggregated_data = filtered_df.sum(axis=0).sort_values(ascending=False)
        top_stocks = aggregated_data.head(top_n)
        
        # Display results in table
        self.display_table(top_stocks)
        
        # Plot results
        self.plot_chart(top_stocks, filtered_df)
        
        # Log operation time
        elapsed_time = time.time() - start_time
        self.time_label.config(text=f"運算時間: {elapsed_time:.2f} 秒")
        self.log_operation(institution, time_range, time_span, top_n, elapsed_time)
    
    def display_table(self, top_stocks):
        """Display the top stocks in the table."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        table = ttk.Treeview(self.table_frame, columns=("股票代號", "累積股數"), show="headings")
        table.heading("股票代號", text="股票代號")
        table.heading("累積股數", text="累積股數")
        table.pack(fill="x")
        
        for stock, value in top_stocks.items():
            table.insert("", "end", values=(stock, value))
    
    def plot_chart(self, top_stocks, filtered_df):
        """Plot the top stocks trend chart."""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(111)
        
        for stock in top_stocks.index:
            trend = filtered_df[stock].resample(self.time_span_var.get()).sum()
            ax.plot(trend.index, trend.values, label=stock)
        
        ax.set_title("前幾大買超股票趨勢")
        ax.set_xlabel("時間")
        ax.set_ylabel("累積股數")
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def log_operation(self, institution, time_range, time_span, top_n, elapsed_time):
        """Log user operation and execution time to a log file."""
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{time.ctime()} - 法人: {institution}, 時間範圍: {time_range}, "
                           f"時間跨度: {time_span}, TopN: {top_n}, 運算時間: {elapsed_time:.2f} 秒\n")


if __name__ == "__main__":
    app = StockAnalysisApp()
    app.mainloop()
