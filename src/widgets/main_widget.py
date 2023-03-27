from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget

from widgets.simulation_widget import SimulationWidget
from world.region import Region

from world.virus import Virus


class MainWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.simulation_widget = SimulationWidget()
        self.layout.addWidget(self.simulation_widget)

        self.button = QPushButton("NEXT STEP")
        self.button.clicked.connect(self.step)
        self.layout.addWidget(self.button)

        # TODO viruses and regions should not be place here - maybe create class "World" and place it there
        self.viruses = []
        self._create_viruses(config["viruses"])

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
                       region["number_of_healthy_agents"],
                       region["number_of_infected_agents"],
                       self.viruses)
            )

    def _create_viruses(self, viruses):
        for virus in viruses:
            self.viruses.append(Virus(name=virus["name"],
                                      death_odds=virus["death_odds"],
                                      sick_time=virus["sick_time"],
                                      immunity_time=virus["immunity_time"],
                                      infection_chance=virus["infection_chance"],
                                      infection_distance=virus["infection_distance"])
                                )
