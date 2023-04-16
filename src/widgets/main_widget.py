from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from utils import AutomateSteps
from widgets.charts_widget import ChartsWidget
from widgets.simulation_widget import SimulationWidget
from world.region import Region
from world.virus import Virus
from world.world import World


class MainWidget(QWidget):
    def __init__(self, config):
        super().__init__()

        self.config = config
        self.is_run = False
        self.world = World(self.config)

        self.layout = QHBoxLayout(self)

        self.simulation_panel = QGroupBox("Simulation")
        self.simulation_panel_layout = QVBoxLayout(self.simulation_panel)

        self.simulation_widget = SimulationWidget()
        self.simulation_panel_layout.addWidget(self.simulation_widget)

        self.automat = AutomateSteps(self.step_world, self.restart_world)
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

        self.simulation_panel_layout.addLayout(self.control_panel)
        self.simulation_widget.plot_state(self.world.get_regions())

        self.statistic_panel = QGroupBox("Statistics")
        self.statistic_panel_layout = QVBoxLayout(self.statistic_panel)
        self.charts_widget = ChartsWidget(self.world.statistic)
        self.statistic_panel_layout.addWidget(self.charts_widget)

        self.layout.addWidget(self.simulation_panel, stretch=2)
        self.layout.addWidget(self.statistic_panel, stretch=1)

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

    def step_world(self):
        self.world.step()
        self.simulation_widget.plot_state(self.world.get_regions())
        self.charts_widget.plot_statistics()

    def restart_world(self):
        self.world.restart()
        self.simulation_widget.plot_state(self.world.get_regions())
        self.charts_widget.restart_statistics(self.world.statistic)
