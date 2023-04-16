from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSpinBox, QVBoxLayout, QWidget

from utils import AutomateSteps
from widgets.simulation_widget import SimulationWidget
from world.region import Region
from world.virus import Virus
from world.world import World


class MainWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.config = config

        self.layout = QVBoxLayout(self)
        self.simulation_widget = SimulationWidget()
        self.layout.addWidget(self.simulation_widget)

        self.automat = AutomateSteps(self.step, self.restart_world)
        self.control_panel = QHBoxLayout()

        self.interval_box = QSpinBox()
        self.interval_box.setMinimum(20)
        self.interval_box.setMaximum(2000)
        self.interval_box.setValue(200)
        self.interval_box.setSingleStep(20)

        self.start_button = QPushButton("START")
        self.start_button.clicked.connect(self.start_pause)

        self.restart_button = QPushButton("RESTART")
        self.restart_button.clicked.connect(self.automat.restart)

        self.control_panel.addWidget(self.interval_box)
        self.control_panel.addWidget(self.start_button)
        self.control_panel.addWidget(self.restart_button)

        self.layout.addLayout(self.control_panel)

        self.is_run = False
        self.restart_world()

    def start_pause(self):
        if self.is_run:
            self.automat.pause()
            self.start_button.setText("START")
            self.restart_button.setEnabled(True)
            self.interval_box.setEnabled(True)
        else:
            self.restart_button.setEnabled(False)
            self.interval_box.setEnabled(False)
            self.automat.set_time(self.interval_box.value())
            self.automat.resume()
            self.start_button.setText("PAUSE")
        self.is_run = not self.is_run

    def restart_world(self):
        self.world = World(self.config)

        self.simulation_widget.plot_state(self.world.get_regions())

    def step(self):
        for region in self.world.get_regions():
            region.step()
        self.simulation_widget.plot_state(self.world.get_regions())
