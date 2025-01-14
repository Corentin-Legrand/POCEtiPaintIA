import random
class Controller:

    def __init__(self):
        self.chart = None

    def update(self, grid):

        # affichage de la grille
        print("Processing the grid...")
        for row in grid:
            print(row)
        print("\n")

        # traitement de la grid et récupération des 10 nouvelles values
        print("Computing the grid to get new values...")

        # affichage des 10 nouvelles values

        values = [random.randint(1, 100) for _ in range(10)]
        print("New values: ", values)
        self.chart.change_values(values)


    def loadChart(self, chartComponent):
        self.chart = chartComponent