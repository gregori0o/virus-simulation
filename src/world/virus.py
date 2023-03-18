import itertools


class Virus:
    id_obj = itertools.count()

    def __init__(self, name, death_odds, sick_time, immunity_time):
        self.id = next(Virus.id_obj)
        self.name = name
        self.death_odds = death_odds
        self.sick_time = sick_time
        self.immunity_time = immunity_time