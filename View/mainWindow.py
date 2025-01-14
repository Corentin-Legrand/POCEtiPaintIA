import tkinter as tk
from View.chart import ChartComponent
from View.canva import CanvaComponent

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Phone Format Window")
        self.geometry("400x800")  # Adjusted dimensions to better fit the components

        # Add the canvas at the top
        self.canva_component = CanvaComponent(self)
        self.canva_component.pack(pady=10, expand=True, fill=tk.BOTH)

        # Add the chart at the bottom
        values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Example values
        self.chart_component = ChartComponent(self, values)
        self.chart_component.pack(pady=10, expand=True, fill=tk.BOTH)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()