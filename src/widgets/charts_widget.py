import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QWidget


class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self):
        fig, self.axes = plt.subplots()
        super().__init__(fig)

    def clear_plot(self):
        self.axes.cla()

    def draw_canvas(self):
        self.draw()

    def plot(self, h, s, i, d=None):
        self.axes.plot(h, color="green", label="healthy")
        self.axes.plot(s, color="red", label="sick")
        self.axes.plot(i, color="blue", label="immune")
        if d is not None:
            self.axes.plot(d, color="black", label="deaths")
        self.axes.legend()


class ChartsWidget(QWidget):
    def __init__(self, statistic):
        super().__init__()

        self.statistic = statistic
        self.window_size = 100

        self.layout = QVBoxLayout(self)

        self.canvas = ChartCanvas()
        self.layout.addWidget(self.canvas)

        self.region_box = QComboBox()
        self.region_box.addItems(["world"] + self.statistic.region_names)
        self.layout.addWidget(self.region_box)

        self.virus_box = QComboBox()
        self.virus_box.addItems(self.statistic.virus_names)
        self.layout.addWidget(self.virus_box)

        self.region_box.currentTextChanged.connect(self.plot_statistics)
        self.virus_box.currentTextChanged.connect(self.plot_statistics)
        self.plot_statistics

    def plot_statistics(self):
        region_name = self.region_box.currentText()
        virus_name = self.virus_box.currentText()
        h, s, i = self.statistic.get_sick_window(
            self.window_size, virus_name, region_name
        )
        _, _, d = self.statistic.get_global_window(
            self.window_size, region_name
        )  # must be change if simulate more than one virus
        self.canvas.clear_plot()
        self.canvas.plot(h, s, i, d)
        self.canvas.draw_canvas()

    def restart_statistics(self, statistic):
        self.statistic = statistic
        self.plot_statistics()
