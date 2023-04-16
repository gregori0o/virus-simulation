from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from widgets.simulation_widget import SimulationWidget
from world.region import Region

from world.virus import Virus

from world.world import World


class MainWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.simulation_widget = SimulationWidget()
        self.layout.addWidget(self.simulation_widget)

        self.button = QPushButton("NEXT STEP")
        self.button.clicked.connect(self.step)
        self.layout.addWidget(self.button)

        self.world = World(config)

        self.simulation_widget.plot_state(
            self.world.get_regions()
        )

    def step(self):
        for region in self.world.get_regions():
            region.step()
        self.simulation_widget.plot_state(
            self.world.get_regions()
        )
