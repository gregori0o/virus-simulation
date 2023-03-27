import json
import sys

from PyQt5.QtWidgets import QApplication

from widgets.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    with open('configuration.json', 'r') as f:
        config = json.load(f)
    window = MainWindow(config)  # noqa

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
