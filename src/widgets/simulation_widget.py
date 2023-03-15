import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QHBoxLayout, QWidget


class SimulationCanvas(FigureCanvasQTAgg):
    def __init__(self):
        fig, self.axes = plt.subplots()
        super().__init__(fig)

    def clear_plot(self):
        self.axes.cla()

    def plot_rectangle(self, width, heigth):
        self.axes.plot([0, width, width, 0, 0], [0, 0, heigth, heigth, 0], color="blue")
        self.axes.axis("off")
        self.draw()

    def plot_agents(self, agents):
        def get_color(agent):
            return "green"

        X = []
        Y = []
        colors = []
        for agent in agents:
            X.append(agent.pos[0])
            Y.append(agent.pos[1])
            colors.append(get_color(agent))
        self.axes.scatter(X, Y, c=colors)
        self.draw()


class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.canvas = SimulationCanvas()
        self.layout.addWidget(self.canvas)

    def plot_state(self, width, heigth, shape, agents):
        self.canvas.clear_plot()
        if shape == "rectangle":
            self.canvas.plot_rectangle(width, heigth)
        else:
            raise NotImplementedError
        self.canvas.plot_agents(agents)
