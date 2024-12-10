# app.py

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import pandas as pd
from data_loader import DataLoader
from data_processor import DataProcessor
from plotter import Plotter

class StockDataAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("法人歷史買賣超數據查詢系統")
        self.geometry("1000x600")

        self.loader = DataLoader()
        self.plotter = Plotter()
        self.create_left_panel()
        self.create_right_panel()
        
    def create_left_panel(self):
        left_panel = tk.Frame(self, width=250, bg="lightgray")
        left_panel.pack(side="left", fill="y")

        self.function_var = tk.StringVar(value="selection2")
        tk.Label(left_panel, text="選擇功能", bg="lightgray").pack(pady=10)
        tk.Radiobutton(left_panel, text="長期選股參考 - 法人歷史買賣超數據統計", variable=self.function_var, value="selection2", bg="lightgray").pack(anchor="w")

        self.institution_var = tk.StringVar(value="外資投信")
        institution_options = ["外資投信", "外資自營", "自營", "投信", "三大法人加總", "全股市"]
        ttk.Combobox(left_panel, textvariable=self.institution_var, values=institution_options).pack(fill="x")

        self.time_range_var = tk.StringVar(value="近一年")
        time_range_options = ["近一月", "近一年"]
        ttk.Combobox(left_panel, textvariable=self.time_range_var, values=time_range_options).pack(fill="x")

        self.time_span_var = tk.StringVar(value="月")
        time_span_options = ["近一週", "月"]
        ttk.Combobox(left_panel, textvariable=self.time_span_var, values=time_span_options).pack(fill="x")

        self.top_n_var = tk.StringVar(value="Top5")
        top_n_options = ["Top1", "Top5"]
        ttk.Combobox(left_panel, textvariable=self.top_n_var, values=top_n_options).pack(fill="x")

        tk.Button(left_panel, text="查詢", command=self.query_data).pack(pady=20)

        self.time_label = tk.Label(left_panel, text="", bg="lightgray")
        self.time_label.pack(pady=10)

    def create_right_panel(self):
        self.right_panel = tk.Frame(self, bg="white")
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.result_label = tk.Label(self.right_panel, text="請選擇查詢條件並按下查詢按鈕", bg="white", font=("Arial", 16))
        self.result_label.pack(pady=20)

    def query_data(self):
        start_time = time.time()
        institution = self.institution_var.get()
        time_range = self.time_range_var.get()
        time_span = self.time_span_var.get()
        top_n = int(self.top_n_var.get()[3:])

        trading_data = self.loader.load_trading_data()
        price_data = self.loader.load_price_data()

        processor = DataProcessor(trading_data, price_data)
        top_stocks, stock_data = processor.calculate_top_stocks(institution, time_range, time_span, top_n)

        fig = self.plotter.plot_top_stocks(stock_data, top_stocks)

        for widget in self.right_panel.winfo_children():
            widget.destroy()

        self.result_label = tk.Label(self.right_panel, text="查詢結果", font=("Arial", 14), bg="white")
        self.result_label.pack(pady=20)
        
        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()
        canvas.get_tk_widget().pack()

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.time_label.config(text=f"運算時間: {elapsed_time:.2f} 秒")
        self.log_operation(elapsed_time, institution, time_range, time_span, top_n)

    def log_operation(self, elapsed_time, institution, time_range, time_span, top_n):
        with open("log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: Institution={institution}, TimeRange={time_range}, TimeSpan={time_span}, TopN={top_n}, ElapsedTime={elapsed_time:.2f}秒\n")

if __name__ == "__main__":
    app = StockDataAnalysisApp()
    app.mainloop()