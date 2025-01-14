import random

from Model.Manager.MainManager import MainManager


class Controller:

    def __init__(self):
        self.chart = None
        self.manager = MainManager()

    def update(self, grid):

        # affichage de la grille
        print("Processing the grid...")

        # traitement de la grid et récupération des 10 nouvelles values
        print("Computing the grid to get new values...")
        # values = [random.randint(1, 100) for _ in range(10)]
        values = self.compute_data(grid)

        print("New values: ", values)
        self.chart.change_values(values)

    def loadChart(self, chartComponent):
        self.chart = chartComponent

    def compute_data(self, grid):
        return self.manager.compute(grid)