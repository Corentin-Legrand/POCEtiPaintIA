import tkinter as tk
from View.chart import ChartComponent
from View.canva import CanvaComponent

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.chart_component = None
        self.canva_component = None
        self.title("Phone Format Window")
        self.geometry("400x700")  # Adjusted dimensions to better fit the components

    def launch(self):
        self.mainloop()

    def addComponent(self, canvaComponent, chartComponent):
        self.canva_component = canvaComponent
        self.canva_component.pack(pady=10, expand=True, fill=tk.BOTH)

        self.chart_component = chartComponent
        self.chart_component.pack(pady=10, expand=True, fill=tk.BOTH)

