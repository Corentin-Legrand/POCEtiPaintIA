import tkinter as tk
from Helpers.Observable import Observable


class CanvaComponent(tk.Frame, Observable):
    def __init__(self, parent):
        super().__init__(parent)
        Observable.__init__(self)  # Initialiser explicitement Observable
        self.canvas = None
        self.cell_size = None
        self.drawing = False
        self.cell_opacity = {}  # Dictionnaire pour stocker l'opacité de chaque cellule
        self.grid = [[0 for _ in range(28)] for _ in range(28)]  # Grille de 28x28 avec des valeurs entre 0 et 1
        self.last_painted_cell = None  # Suivre la dernière cellule peinte
        self.create_canvas()

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=330, height=330)
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
                self.cell_opacity[(i, j)] = 0  # Initialiser toutes les cellules avec une opacité de 0

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
                if idx == 0:  # Cellule centrale
                    if current_opacity < 100:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='')
                        self.cell_opacity[cell] = 100
                        self.grid[cell[1]][cell[0]] = 1  # Noir complet
                else:  # Cellules environnantes
                    if current_opacity == 0:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='gray50')
                        self.cell_opacity[cell] = 50
                        self.grid[cell[1]][cell[0]] = 0.5  # Gris clair
                    elif current_opacity == 50:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='gray25')
                        self.cell_opacity[cell] = 75
                        self.grid[cell[1]][cell[0]] = 0.75  # Gris foncé
                    elif current_opacity == 75:
                        self.canvas.itemconfig(f"cell_{cell[0]}_{cell[1]}", fill='black', stipple='')
                        self.cell_opacity[cell] = 100
                        self.grid[cell[1]][cell[0]] = 1  # Noir complet

        # Notifier les observateurs avec la grille mise à jour
        self.notify_observers(self.grid)
