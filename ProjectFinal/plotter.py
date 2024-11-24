import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_data(frame, data):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data["Date"], data["All Investors"], label="所有投資人")
    ax.plot(data["Date"], data["Foreign Agency"], label="外資投信")
    ax.plot(data["Date"], data["Agency"], label="投信")
    ax.legend()
    ax.set_title("股票趨勢圖")
    ax.set_xlabel("日期")
    ax.set_ylabel("股數")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas
