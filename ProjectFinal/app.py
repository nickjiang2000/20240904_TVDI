import tkinter as tk
from tkinter import ttk
from data_loader import load_data
from data_processor import process_daily_data
from plotter import plot_data


class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("國內外投信股票買賣查詢系統")

        # Left Navigation
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.stock_label = tk.Label(self.nav_frame, text="選擇股票")
        self.stock_label.pack(anchor="w")

        self.stock_combobox = ttk.Combobox(self.nav_frame, state="readonly")
        self.stock_combobox.pack(fill="x")
        self.stock_combobox.bind("<<ComboboxSelected>>", self.display_data)

        # Right Display Area
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(side="right", fill="both", expand=True)

        # Table Area
        self.table_frame = tk.Frame(self.display_frame)
        self.table_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Add Table Label
        self.table_label = tk.Label(self.table_frame, text="當日買賣股數", font=("Arial", 14))
        self.table_label.pack(anchor="w")

        self.table = ttk.Treeview(
            self.table_frame,
            columns=["Date", "All Investors", "Foreign Agency", "Agency"],
            show="headings",
        )
        self.table.heading("Date", text="日期")
        self.table.heading("All Investors", text="所有投資人")
        self.table.heading("Foreign Agency", text="外資投信")
        self.table.heading("Agency", text="投信")
        self.table.column("Date", anchor="center", width=100)
        self.table.column("All Investors", anchor="e", width=150)
        self.table.column("Foreign Agency", anchor="e", width=150)
        self.table.column("Agency", anchor="e", width=150)
        self.table.pack(fill="x", expand=True)

        # Plot Area
        self.plot_frame = tk.Frame(self.display_frame)
        self.plot_frame.pack(side="bottom", fill="both", expand=True)

        self.canvas = None  # Placeholder for the plot

        # Load Data
        self.data = load_data()
        self.stock_combobox["values"] = list(self.data["all_trading"].columns)
        self.stock_combobox.set("2330 台積電")

        # Display default stock data
        self.display_data()

    def display_data(self, event=None):
        stock = self.stock_combobox.get()
        table_data, plot_data_values = process_daily_data(self.data, stock)

        # Update table
        for row in self.table.get_children():
            self.table.delete(row)
        for row in table_data:
            self.table.insert("", "end", values=row)

        # Update plot
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = plot_data(self.plot_frame, plot_data_values)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
