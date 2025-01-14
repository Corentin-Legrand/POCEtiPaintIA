from Controller.MainController import Controller
from View.canva import CanvaComponent
from View.chart import ChartComponent
from View.mainWindow import MainWindow


def initProject():
    controller = Controller()
    view = MainWindow()
    canvaComponent = CanvaComponent(view)
    chartComponent = ChartComponent(view,[0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


    canvaComponent.add_observer(controller)
    controller.loadChart(chartComponent)
    view.addComponent(canvaComponent, chartComponent)
    view.launch()

initProject()