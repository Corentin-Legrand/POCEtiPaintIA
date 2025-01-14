import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ChartComponent(tk.Frame):
    def __init__(self, parent, values):
        super().__init__(parent)
        self.figure = Figure(figsize=(3.3, 3.3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.create_bar_chart(values)

    def create_bar_chart(self, values):
        self.ax.clear()
        self.ax.bar(range(1, len(values) + 1), values)
        self.ax.set_xticks(range(1, len(values) + 1))  # Set x-ticks to display all numbers
        self.ax.set_title('Estimation du modèle')
        self.canvas.draw()

    def change_values(self, values):
        self.create_bar_chart(values)