from typing import Tuple

import numpy as np

from utils import Direction


class Agent:
    def __init__(self, pos: Tuple, map, velocity: int = 4):
        self.pos = pos
        self.age = 0
        self.is_sick = False
        self.sick_time = 0
        self.remaining_immunity = 0
        self.velocity = velocity
        self.direction = np.random.choice(Direction.list())
        self.map = map

    def step(self):
        """Try to make step. If it goes off the map, turn right (change self.direction to next). If it cannot make step, stays in place."""
        x, y = self.pos
        # turn means how change direction
        # -2 - go left from self.direction
        # 0 - go as self.direction
        # 2 - go right from self.direction
        turn = np.random.choice(
            [-2, -1, 0, 1, 2], p=[1 / 15, 3 / 15, 7 / 15, 3 / 15, 1 / 15]
        )
        delta_x = delta_y = 0
        for _ in range(4):
            match self.direction:
                case Direction.UP.value:
                    delta_x = turn * self.velocity // 2
                    delta_y = -1 * (np.abs(turn) - 2) * self.velocity // 2
                case Direction.DOWN.value:
                    delta_x = -1 * turn * self.velocity // 2
                    delta_y = (np.abs(turn) - 2) * self.velocity // 2
                case Direction.RIGHT.value:
                    delta_x = -1 * (np.abs(turn) - 2) * self.velocity // 2
                    delta_y = -1 * turn * self.velocity // 2
                case Direction.LEFT.value:
                    delta_x = (np.abs(turn) - 2) * self.velocity // 2
                    delta_y = turn * self.velocity // 2
            if self.map.is_in_map_area((x + delta_x, y + delta_y)):
                break
            delta_x = delta_y = 0
            self.direction = Direction.next(self.direction)
        self.pos = (x + delta_x, y + delta_y)
