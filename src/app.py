import json
import sys

from PyQt5.QtWidgets import QApplication

from widgets.main_window import MainWindow


def main(conf_file):
    app = QApplication(sys.argv)
    with open(conf_file, "r") as f:
        config = json.load(f)
    window = MainWindow(config)  # noqa

    sys.exit(app.exec_())


if __name__ == "__main__":
    conf_file = sys.argv[1] if len(sys.argv) > 1 else "configurations/base.json"
    main(conf_file)
