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
        self.sick_info = {}
        self.immunity_info = {}
        self.velocity = velocity
        self.direction = np.random.choice(Direction.list())
        self.region = region
        if virus is None:
            self.region.statistic.healthy_birth()
        else:
            self.region.statistic.sick_birth(virus.name)
            self.sick_info[virus.name] = (virus.sick_time, virus)

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

    def is_agent_sick(self, virus_name=None):
        if virus_name is None:
            return self.is_sick
        return self.sick_info.get(virus_name) is not None

    def update_sickness(self):
        to_remove = []
        for virus_name, (sick_time, virus) in self.sick_info.items():
            sick_time -= 1
            if sick_time == 0:
                to_remove.append(virus_name)
                self.region.statistic.end_sick(virus_name)
                self.immunity_info[virus_name] = (virus.immunity_time + 1, virus)
            else:
                self.sick_info[virus_name] = (sick_time, virus)
        for virus_name in to_remove:
            del self.sick_info[virus_name]
        if not self.sick_info:
            if self.is_sick:
                self.region.statistic.end_be_sick()
            self.is_sick = False

    def update_immunity(self):
        to_remove = []
        for virus_name, tmp in self.immunity_info.items():
            remaining_immunity, virus = tmp
            remaining_immunity -= 1
            if remaining_immunity == 0:
                to_remove.append(virus_name)
                self.region.statistic.end_immune(virus_name)
            else:
                self.immunity_info[virus_name] = (remaining_immunity, virus)
        for virus_name in to_remove:
            del self.immunity_info[virus_name]

    def agent_sick_update(self):
        if self.is_sick:
            if self.calculate_death():
                self.remove_agent()
                return
            self.update_sickness()
        self.update_immunity()

    def calculate_death_prob(self) -> int:
        return max([virus.death_odds for _, virus in self.sick_info.values()])

    def calculate_death(self) -> bool:
        if not self.sick_info:
            raise Exception("Trying to calculate death without virus")
        is_dying = (True, False)
        death_probability = self.calculate_death_prob()
        weights = (death_probability, 100 - death_probability)
        return random.choices(is_dying, weights=weights, k=1)[0]

    def remove_agent(self):
        self.region.statistic.death(self)
        self.region.remove_agent(self)

    def calculate_infection_prob(self, virus_name) -> int:
        return self.sick_info[virus_name][1].infection_chance

    def calculate_infection(self, neighbor, virus_name) -> bool:
        if self.sick_info.get(virus_name) is None:
            raise Exception(f"Trying to calculate infection without virus {virus_name}")
        if neighbor.immunity_info.get(virus_name) is not None:
            return False
        infected = (True, False)
        infection_probability = self.calculate_infection_prob(virus_name)
        weights = (infection_probability, 100 - infection_probability)
        return random.choices(infected, weights=weights, k=1)[0]

    def set_sickness(self, virus):
        if virus is None:
            raise Exception("Trying set sickness infection without virus")
        if not self.is_sick:
            self.region.statistic.start_be_sick()
        self.region.statistic.start_sick(virus.name)
        self.is_sick = True
        self.sick_info[virus.name] = (virus.sick_time, virus)
