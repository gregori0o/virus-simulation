from enum import Enum
from time import sleep
from typing import Callable

from PyQt5.QtCore import QThread, pyqtSignal


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))

    @classmethod
    def next(cls, dir):
        match dir:
            case cls.UP.value:
                return cls.RIGHT.value
            case cls.RIGHT.value:
                return cls.DOWN.value
            case cls.DOWN.value:
                return cls.LEFT.value
            case cls.LEFT.value:
                return cls.UP.value


class Runner(QThread):
    signal = pyqtSignal()

    def __init__(self, step_time: int = 10):
        super().__init__()
        self.is_running = False
        self.step_time = step_time

    def run(self):
        while self.is_running:
            self.signal.emit()
            sleep(self.step_time / 1000)


class AutomateSteps:
    def __init__(self, to_execute: Callable, when_restart: Callable):
        self.to_execute = to_execute
        self.when_restart = when_restart
        self.thread = None
        self.step_time = 10

    def set_time(self, time: int):
        self.step_time = time

    def resume(self):
        self.thread = Runner(self.step_time)
        self.thread.signal.connect(self.to_execute)
        self.thread.is_running = True
        self.thread.start()

    def pause(self):
        if self.thread:
            self.thread.is_running = False
            self.thread.wait()
            self.thread = None

    def restart(self):
        self.pause()
        self.when_restart()
