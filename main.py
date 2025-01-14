from Controller.MainController import Controller
from View.canva import CanvaComponent
from View.chart import ChartComponent
from View.mainWindow import MainWindow


def initProject():
    controller = Controller()
    view = MainWindow()
    canvaComponent = CanvaComponent(view)
    chartComponent = ChartComponent(view,[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])


    canvaComponent.add_observer(controller)
    controller.loadChart(chartComponent)
    view.addComponent(canvaComponent, chartComponent)
    view.launch()

initProject()