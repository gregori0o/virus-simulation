import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QHBoxLayout, QWidget


class SimulationCanvas(FigureCanvasQTAgg):
    def __init__(self):
        fig, self.axes = plt.subplots()
        super().__init__(fig)

    def clear_plot(self):
        self.axes.cla()

    def plot_region(self, region):
        # create x and y arrays from vertex array - for plot (can I do oneliner here?)
        X, Y = list(zip(*region.vertices))
        # plot single region from his vertices
        self.axes.plot(X, Y, color=region.color)
        # plot airport
        if region.airport is not None:
            x, y = region.airport
            self.axes.scatter(x, y, color="black", marker="$A$", s=100)

    def plot_agents(self, agents):
        def get_color(agent):
            return "red" if agent.is_agent_sick() else "green"

        X = []
        Y = []
        colors = []
        for agent in agents:
            X.append(agent.pos[0])
            Y.append(agent.pos[1])
            colors.append(get_color(agent))
        self.axes.scatter(X, Y, c=colors)

    def draw_canvas(self):
        # self.axes.axis("off")
        self.draw()


class SimulationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.canvas = SimulationCanvas()
        self.layout.addWidget(self.canvas)

    # plot whole map
    def plot_state(self, regions):
        # clear all plots(regions)
        self.canvas.clear_plot()

        for region in regions:
            self.canvas.plot_region(region)
            self.canvas.plot_agents(region.agents)

        # draw map
        self.canvas.draw_canvas()
