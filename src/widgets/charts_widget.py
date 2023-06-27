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

    def plot(self, data):
        for arr, color, label in data:
            self.axes.plot(arr, color=color, label=label)
        self.axes.legend()


class ChartsWidget(QWidget):
    def __init__(self, statistic):
        super().__init__()

        self.statistic = statistic
        self.window_size = 100

        self.layout = QVBoxLayout(self)

        self.global_canvas = ChartCanvas()
        self.layout.addWidget(self.global_canvas)

        self.global_region_box = QComboBox()
        self.global_region_box.addItems(["world"] + self.statistic.region_names)
        self.layout.addWidget(self.global_region_box)
        self.global_region_box.currentTextChanged.connect(self.plot_global_statistics)

        self.sick_canvas = ChartCanvas()
        self.layout.addWidget(self.sick_canvas)

        self.region_box = QComboBox()
        self.region_box.addItems(["world"] + self.statistic.region_names)
        self.layout.addWidget(self.region_box)

        self.virus_box = QComboBox()
        self.virus_box.addItems(self.statistic.virus_names)
        self.layout.addWidget(self.virus_box)

        self.region_box.currentTextChanged.connect(self.plot_sick_statistics)
        self.virus_box.currentTextChanged.connect(self.plot_sick_statistics)

        self.plot_statistics()

    def plot_sick_statistics(self):
        region_name = self.region_box.currentText()
        virus_name = self.virus_box.currentText()
        h, s, i = self.statistic.get_sick_window(
            self.window_size, virus_name, region_name
        )
        data = [
            (h, "green", "not infected"),
            (s, "red", "sick"),
            (i, "blue", "immune"),
        ]
        self.sick_canvas.clear_plot()
        self.sick_canvas.plot(data)
        self.sick_canvas.draw_canvas()

    def plot_global_statistics(self):
        region_name = self.global_region_box.currentText()
        h, s, d = self.statistic.get_global_window(self.window_size, region_name)
        data = [
            (h, "green", "healthy"),
            (s, "red", "sick"),
            (d, "black", "deaths"),
        ]
        self.global_canvas.clear_plot()
        self.global_canvas.plot(data)
        self.global_canvas.draw_canvas()

    def plot_statistics(self):
        self.plot_sick_statistics()
        self.plot_global_statistics()

    def restart_statistics(self, statistic):
        self.statistic = statistic
        self.plot_statistics()
