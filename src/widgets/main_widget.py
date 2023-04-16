from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from widgets.simulation_widget import SimulationWidget
from world.region import Region


class MainWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.simulation_widget = SimulationWidget()
        self.layout.addWidget(self.simulation_widget)

        self.button = QPushButton("NEXT STEP")
        self.button.clicked.connect(self.step)
        self.layout.addWidget(self.button)

        self.regions = []
        self._create_regions(config["regions"])
        self.simulation_widget.plot_state(
            self.regions
        )

    def step(self):
        for region in self.regions:
            region.step()
        self.simulation_widget.plot_state(
            self.regions
        )

    def _create_regions(self, regions):
        for region in regions:
            self.regions.append(
                Region(region["name"],
                       region["vertices"],
                       region["color"],
                       region["number_of_agents"])
            )
