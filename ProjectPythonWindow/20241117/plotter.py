# plotter.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter:
    def plot_top_stocks(self, stock_data, top_stocks):
        fig, ax = plt.subplots(figsize=(10, 6))
        for stock in top_stocks.index:
            ax.plot(stock_data.index, stock_data[stock], label=stock)
        
        ax.set_title("前幾大買超股票趨勢")
        ax.set_xlabel("時間")
        ax.set_ylabel("累積加總")
        ax.legend()
        
        return fig