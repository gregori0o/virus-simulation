import random
from typing import Tuple

import numpy as np

from utils import Direction

from world.virus import Virus


class Agent:
    def __init__(self, pos: Tuple, region, virus: Virus = None, velocity: int = 4):
        self.pos = pos
        self.age = 0
        self.is_sick = virus is not None
        self.sick_time = virus.sick_time if virus else 0
        self.virus = virus
        self.remaining_immunity = [virus.immunity_time, virus] if virus else [None, None]  # (immunity, last_virus_name)
        self.velocity = velocity
        self.direction = np.random.choice(Direction.list())
        self.region = region

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
            if self.region.is_in_region_area((x + delta_x, y + delta_y)):
                break
            delta_x = delta_y = 0
            self.direction = Direction.next(self.direction)
        self.pos = (x + delta_x, y + delta_y)

        self.agent_sick_update()

    def is_agent_sick(self):
        return self.is_sick

    def update_sickness(self):
        self.sick_time -= 1
        if self.sick_time == 0:
            self.is_sick = False
            self.virus = None

    def update_immunity(self):
        self.remaining_immunity[0] -= 1

    def agent_sick_update(self):
        if self.is_sick:
            if self.calculate_death():
                self.remove_agent()
            self.update_sickness()
        elif self.remaining_immunity[0] != 0 and self.remaining_immunity[0] is not None:
            self.update_immunity()

    def calculate_death_prob(self) -> int:
        return self.virus.death_odds

    def calculate_death(self) -> bool:
        if self.virus is None:
            raise Exception("Trying to calculate death without virus")
        is_dying = (True, False)
        death_probability = self.calculate_death_prob()
        cum_weights = (death_probability, 100 - death_probability)
        return random.choices(is_dying, cum_weights=cum_weights, k=1)[0]

    def remove_agent(self):
        self.region.remove_agent(self)

    def calculate_infection_prob(self) -> int:
        return self.virus.infection_chance

    def calculate_infection(self, neighbor) -> bool:
        if self.virus is None:
            raise Exception("Trying to calculate infection without virus")
        if neighbor.remaining_immunity[0] != 0 and neighbor.remaining_immunity[1] == self.virus:
            return False
        infected = (True, False)
        infection_probability = self.calculate_infection_prob()
        cum_weights = (infection_probability, 100 - infection_probability)
        return random.choices(infected, cum_weights=cum_weights, k=1)[0]

    def set_sickness(self, virus):
        if virus is None:
            raise Exception("Trying set sickness infection without virus")
        self.is_sick = True
        self.sick_time = virus.sick_time
        self.virus = virus
        self.remaining_immunity = [virus.immunity_time, virus]



