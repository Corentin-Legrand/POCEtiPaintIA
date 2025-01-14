import random

from Model.Manager.MainManager import MainManager


class Controller:

    def __init__(self):
        self.chart = None
        self.manager = MainManager()

    def update(self, grid):
        if all(value == 0 for row in grid for value in row):
            values = [0] * 11
        else:
            values = self.compute_data(grid)

        self.chart.change_values(values)

    def loadChart(self, chartComponent):
        self.chart = chartComponent

    def compute_data(self, grid):
        return self.manager.compute(grid)