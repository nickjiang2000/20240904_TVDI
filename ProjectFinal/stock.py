import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_PATH = "./data/"

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("國內外投信股票買賣查詢系統")

        # 左側導航區
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(self.nav_frame, text="選擇股票").pack(anchor="w")
        self.stock_combobox = ttk.Combobox(self.nav_frame, state="readonly")
        self.stock_combobox.pack(fill="x")
        self.stock_combobox.bind("<<ComboboxSelected>>", self.display_data)

        # 右側顯示區
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(side="right", fill="both", expand=True)

        # 表格區
        self.table_frame = tk.Frame(self.display_frame)
        self.table_frame.pack(side="top", fill="x", padx=10, pady=5)
        tk.Label(self.table_frame, text="當日買賣股數", font=("Arial", 14)).pack(anchor="w")

        self.table = ttk.Treeview(
            self.table_frame,
            columns=["Date", "All Investors", "Foreign Agency", "Agency"],
            show="headings",
        )
        for col, name in zip(
            ["Date", "All Investors", "Foreign Agency", "Agency"],
            ["日期", "所有投資人", "外資投信", "投信"],
        ):
            self.table.heading(col, text=name)
            self.table.column(col, anchor="center" if col == "Date" else "e", width=150)
        self.table.pack(fill="x", expand=True)

        # 圖表區
        self.plot_frame = tk.Frame(self.display_frame)
        self.plot_frame.pack(side="bottom", fill="both", expand=True)
        self.canvas = None

        # 載入數據並初始化介面
        self.data = self.load_data()
        self.stock_combobox["values"] = list(self.data["all_trading"].columns)
        self.stock_combobox.set("2330 台積電")
        self.display_data()

    def load_data(self):
        """
        載入數據
        """
        return {
            "all_trading": pd.read_csv(f"{DATA_PATH}all_trading.csv", index_col=0, parse_dates=True),
            "foreign_agency_trading": pd.read_csv(f"{DATA_PATH}foreign_agency_trading.csv", index_col=0, parse_dates=True),
            "agency_trading": pd.read_csv(f"{DATA_PATH}agency_trading.csv", index_col=0, parse_dates=True),
        }

    def process_daily_data(self, stock):
        """
        處理每日數據
        """
        table_data = pd.DataFrame({
            "Date": self.data["all_trading"].index,
            "All Investors": self.data["all_trading"][stock],
            "Foreign Agency": self.data["foreign_agency_trading"][stock],
            "Agency": self.data["agency_trading"][stock],
        }).fillna(0).sort_index(ascending=False)

        table_data["All Investors"] = table_data["All Investors"].astype(int).apply(lambda x: f"{x:,}")
        table_data["Foreign Agency"] = table_data["Foreign Agency"].astype(int).apply(lambda x: f"{x:,}")
        table_data["Agency"] = table_data["Agency"].astype(int).apply(lambda x: f"{x:,}")
        return table_data.values.tolist(), table_data

    def plot_data(self, data):
        """
        繪製股票買賣趨勢圖
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data["All Investors"].str.replace(",", "").astype(int), label="All Investors", marker="o")
        ax.plot(data.index, data["Foreign Agency"].str.replace(",", "").astype(int), label="Foreign Agency", marker="x")
        ax.plot(data.index, data["Agency"].str.replace(",", "").astype(int), label="Domestic Agency", marker="*")

        ax.set_title("Graph of Buying Trend", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Number of Stock", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True)

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def display_data(self, event=None):
        """
        顯示選定股票的表格和圖表
        """
        stock = self.stock_combobox.get()
        table_data, plot_data_values = self.process_daily_data(stock)

        # 更新表格
        for row in self.table.get_children():
            self.table.delete(row)
        for row in table_data:
            self.table.insert("", "end", values=row)

        # 更新圖表
        self.plot_data(plot_data_values)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
