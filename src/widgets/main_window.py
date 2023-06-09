import json
from datetime import datetime

from PyQt5.QtWidgets import QDesktopWidget, QHBoxLayout, QMainWindow, QWidget

from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Virus Simulation")
        self.setGeometry(0, 0, 1200, 600)

        # position the window in the middle of the screen
        rect = self.frameGeometry()
        rect.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        simulation_id = datetime.now().isoformat()
        with open(f"results/configuration_{simulation_id}.json", "w") as f:
            json.dump(config, f)

        self.generalLayout.addWidget(MainWidget(config["main_widget"], simulation_id))

        self.show()
