import tkinter as tk
from View.chart import ChartComponent
from View.canva import CanvaComponent

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg='white')
        self.chart_component = None
        self.canva_component = None
        self.title("POCETIPAINTIA")
        self.geometry("400x700")  # Adjusted dimensions to better fit the components

    def launch(self):
        self.mainloop()


    def addComponent(self, canvaComponent, chartComponent):
        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(pady=10, fill=tk.X)

        clear_button = tk.Button(button_frame, text="Clear", command=self.handle_clear_button)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        close_button = tk.Button(button_frame, text="Close", command=self.quit)
        close_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        self.canva_component = canvaComponent
        self.canva_component.pack(pady=10, expand=True, fill=tk.BOTH)

        self.chart_component = chartComponent
        self.chart_component.pack(pady=10, expand=True, fill=tk.BOTH)

    def handle_clear_button(self):
        self.canva_component.clear()