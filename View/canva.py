import tkinter as tk
from Helpers.Observable import Observable


class CanvaComponent(tk.Frame, Observable):
    def __init__(self, parent):
        super().__init__(parent)
        Observable.__init__(self)  # Initialisation explicite d'Observable

        # Paramètres
        self.num_cells = 28
        self.canvas_width = 336   # Par ex. : 28 * 12 = 336
        self.canvas_height = 336  # Pareil pour la hauteur pour un carré

        self.cell_size = self.canvas_width // self.num_cells

        # Canvas + gestion
        self.canvas = None
        self.drawing = False
        self.last_painted_cell = None

        # Matrice (28x28) pour l’opacité et pour le rectangle
        # Opacité = 0, 50, 75, 100
        self.opacities = [[0 for _ in range(self.num_cells)] for _ in range(self.num_cells)]
        # Références directes aux rectangles sur le canvas
        self.rectangles = [[None for _ in range(self.num_cells)] for _ in range(self.num_cells)]
        # Grille de valeurs [0..1] associée à chaque cellule
        self.grid = [[0.0 for _ in range(self.num_cells)] for _ in range(self.num_cells)]

        self.configure(bg='white')  # Set the background of the frame to white
        self._create_canvas()
        self._create_grid()
    def _create_canvas(self):
        """Crée et configure le Canvas principal."""
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height,  bg='grey')
        self.canvas.pack()

        # Bind des événements
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def _create_grid(self):
        """Crée le quadrillage et stocke les références des rectangles dans self.rectangles."""
        for j in range(self.num_cells):
            for i in range(self.num_cells):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                rect_id = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    outline='gray', fill='white'
                )
                self.rectangles[j][i] = rect_id
                self.opacities[j][i] = 0
                self.grid[j][i] = 0.0

    def start_drawing(self, event):
        """Début du dessin : on active le 'mode dessin' et on peint directement la cellule sous le curseur."""
        self.drawing = True
        self.last_painted_cell = None
        self.paint(event)

    def stop_drawing(self, event):
        """Fin du dessin."""
        self.drawing = False

    def paint(self, event):
        """Peint la cellule (et ses voisines) si on est en mode dessin."""
        if not self.drawing:
            return

        # Conversion coordonnées (pixels) → index (cellules)
        i = event.x // self.cell_size
        j = event.y // self.cell_size

        # Vérifier si on est toujours dans la zone du canvas
        if not (0 <= i < self.num_cells and 0 <= j < self.num_cells):
            return

        # Éviter de repeindre si la cellule est la même que précédemment
        current_cell = (i, j)
        if current_cell == self.last_painted_cell:
            return
        self.last_painted_cell = current_cell

        # Liste des cellules à peindre : la cellule centrale + ses 4 voisines
        cells_to_paint = [
            (i, j),      # centrale
            (i - 1, j),  # gauche
            (i + 1, j),  # droite
            (i, j - 1),  # haut
            (i, j + 1)   # bas
        ]

        for index, (cx, cy) in enumerate(cells_to_paint):
            if 0 <= cx < self.num_cells and 0 <= cy < self.num_cells:
                if index == 0:
                    # La cellule centrale : opacité = 100% directement
                    self.paint_cell(cx, cy, force_max=True)
                else:
                    # Cellule voisine : incrément par paliers (50->75->100)
                    self.paint_cell(cx, cy)

        # Notifier les observateurs après toutes les mises à jour
        self.notify_observers(self.grid)

    def paint_cell(self, i, j, force_max=False):
        """Met à jour l’opacité et la couleur/stipple de la cellule [j][i]."""
        current_opacity = self.opacities[j][i]

        if force_max:
            new_opacity = 100
        else:
            # Incrémente les paliers : 0 → 50 → 75 → 100
            if current_opacity == 0:
                new_opacity = 50
            elif current_opacity == 50:
                new_opacity = 75
            elif current_opacity == 75:
                new_opacity = 100
            else:
                new_opacity = current_opacity  # Pas d'augmentation si déjà 100

        # Détermination du stipple et de la valeur grid associée
        if new_opacity == 0:
            fill_color = 'white'
            stipple_pattern = ''
            grid_value = 0.0
        elif new_opacity == 50:
            fill_color = 'black'
            stipple_pattern = 'gray50'
            grid_value = 0.5
        elif new_opacity == 75:
            fill_color = 'black'
            stipple_pattern = 'gray25'
            grid_value = 0.75
        else:  # 100
            fill_color = 'black'
            stipple_pattern = ''
            grid_value = 1.0

        # Application sur le canvas
        rect_id = self.rectangles[j][i]
        self.canvas.itemconfig(rect_id, fill=fill_color, stipple=stipple_pattern)

        # Mise à jour des structures internes
        self.opacities[j][i] = new_opacity
        self.grid[j][i] = grid_value

    def clear(self):
        """Efface tout le contenu du canvas et réinitialise la grille."""
        for j in range(self.num_cells):
            for i in range(self.num_cells):
                # Remettre chaque cellule en blanc
                rect_id = self.rectangles[j][i]
                self.canvas.itemconfig(rect_id, fill='white', stipple='')
                self.opacities[j][i] = 0
                self.grid[j][i] = 0.0

        # Notifier les observateurs après réinitialisation
        self.notify_observers(self.grid)
