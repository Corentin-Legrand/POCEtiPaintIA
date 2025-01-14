import tkinter as tk

class CanvaComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = None
        self.cell_size = None
        self.drawing = False
        self.cell_opacity = {}  # Dictionary to store the opacity of each cell
        self.last_painted_cell = None  # Track the last painted cell
        self.create_canvas()

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=360, height=360, bg='white')
        self.canvas.pack()

        self.cell_size = 360 // 28
        self.create_grid()
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def create_grid(self):
        for i in range(28):
            for j in range(28):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='gray', fill='white', tags=f"cell_{i}_{j}")
                self.cell_opacity[(i, j)] = 0  # Initialize all cells with 0 opacity

    def start_drawing(self, event):
        self.drawing = True
        self.last_painted_cell = None
        self.paint(event)

    def stop_drawing(self, event):
        self.drawing = False

    def paint(self, event):
        if not self.drawing:
            return
        x, y = event.x, event.y
        i, j = x // self.cell_size, y // self.cell_size
        current_cell = (i, j)

        if current_cell == self.last_painted_cell:
            return

        self.last_painted_cell = current_cell
        cells_to_paint = [(i, j), (i-1, j), (i+1, j), (i, j-1), (i, j+1)]

        for idx, cell in enumerate(cells_to_paint):
            if 0 <= cell[0] < 28 and 0 <= cell[1] < 28:
                current_opacity = self.cell_opacity[cell]
                if idx == 0:  # Central cell
                    if current_opacity < 100:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='')
                        self.cell_opacity[cell] = 100
                else:  # Surrounding cells
                    if current_opacity == 0:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='gray50')
                        self.cell_opacity[cell] = 50
                    elif current_opacity == 50:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='gray25')
                        self.cell_opacity[cell] = 75
                    elif current_opacity == 75:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='')
                        self.cell_opacity[cell] = 100