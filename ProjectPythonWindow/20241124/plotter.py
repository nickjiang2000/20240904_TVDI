import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def plot_data(frame, data):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot data
    ax.plot(data["Date"], data["All Investors"], label="All Investers", marker="o")
    ax.plot(data["Date"], data["Foreign Agency"], label="Foreign Agent", marker="x")
    ax.plot(data["Date"], data["Agency"], label="Domestic Agent", marker="*")

    # Customize plot
    ax.set_title("Graph of Buying Trend", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Number of Stock Buying", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True)

    # Embed plot into tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas



