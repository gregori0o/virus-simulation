from typing import Tuple


class Agent:
    def __init__(self, pos: Tuple):
        self.pos = pos
        self.age = 0
        self.is_sick = False
        self.sick_time = 0
        self.remaining_immunity = 0
        self.velocity = 5

    def step(self):
        x, y = self.pos
        self.pos = (x + 2, y)
