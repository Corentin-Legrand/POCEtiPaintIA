import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartComponent(tk.Frame):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.create_bar_chart(values)

    def create_bar_chart(self, values):
        figure = Figure(figsize=(3.6, 3.6), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(range(1, 11), values)
        ax.set_xlabel('Bar Number')
        ax.set_ylabel('Percentage')
        ax.set_title('Bar Chart')

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)