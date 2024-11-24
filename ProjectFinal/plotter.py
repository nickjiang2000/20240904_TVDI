import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_data(frame, data):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot data
    ax.plot(data["Date"], data["All Investors"], label="所有投資人", marker="o")
    ax.plot(data["Date"], data["Foreign Agency"], label="外資投信", marker="x")
    ax.plot(data["Date"], data["Agency"], label="投信", marker="*")

    # Customize plot
    ax.set_title("股票趨勢圖", fontsize=16)
    ax.set_xlabel("日期", fontsize=12)
    ax.set_ylabel("股數 (千分位)", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True)

    # Embed plot into tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas

