import itertools
import random


class Virus:
    id_obj = itertools.count()

    def __init__(
        self,
        name,
        death_odds,
        sick_time,
        immunity_time,
        infection_chance,
        infection_distance,
    ):
        self.id = next(Virus.id_obj)
        self.name = name
        self._death_odds = death_odds
        self.sick_time = sick_time
        self.immunity_time = immunity_time
        self.infection_chance = infection_chance
        self.infection_distance = infection_distance

    @property
    def death_odds(self):
        if isinstance(self._death_odds, list | tuple):
            left, right = self._death_odds
            return random.randint(left, right)
        else:
            return self._death_odds
