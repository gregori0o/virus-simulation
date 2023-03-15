from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from widgets.simulation_widget import SimulationWidget
from world.region import Region


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.simulation_widget = SimulationWidget()
        self.layout.addWidget(self.simulation_widget)

        self.button = QPushButton("NEXT STEP")
        self.button.clicked.connect(self.step)
        self.layout.addWidget(self.button)

        self.region = Region(200, 100, 50)
        self.simulation_widget.plot_state(
            self.region.width, self.region.heigth, self.region.shape, self.region.agents
        )

    def step(self):
        self.region.step()
        self.simulation_widget.plot_state(
            self.region.width, self.region.heigth, self.region.shape, self.region.agents
        )
