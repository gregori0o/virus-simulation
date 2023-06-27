from random import shuffle

from stats.global_stat import GlobalStatistic
from world.region import Region
from world.virus import Virus


class World:
    def __init__(self, config):
        self.config = config
        if self.config.get("flights"):
            self.flights_frequency = self.config["flights"]["frequency"]
        else:
            self.flights_frequency = 0
        self.restart()

    def get_regions(self):
        return self.regions

    def get_viruses(self):
        return self.viruses

    def restart(self):
        self.step_num = 0
        self.regions = []
        self.viruses = []
        self._create_viruses(self.config["viruses"])
        self._create_regions(self.config["regions"])
        self.statistic = GlobalStatistic(
            [region.name for region in self.regions],
            [virus.name for virus in self.viruses],
        )

    def _create_regions(self, regions):
        for region in regions:
            self.regions.append(
                Region(
                    region["name"],
                    region["vertices"],
                    region["color"],
                    region["number_of_healthy_agents"],
                    region["number_of_infected_agents"],
                    region.get("has_airport"),
                    self.viruses,
                )
            )

    def _create_viruses(self, viruses):
        for virus in viruses:
            self.viruses.append(
                Virus(
                    name=virus["name"],
                    death_odds=virus["death_odds"],
                    sick_time=virus["sick_time"],
                    immunity_time=virus["immunity_time"],
                    infection_chance=virus["infection_chance"],
                    infection_distance=virus["infection_distance"],
                )
            )

    def step(self):
        for region in self.regions:
            region.step()

        if self.flights_frequency > 0 and self.step_num % self.flights_frequency == 0:
            passengers = []
            num_passengers = []
            for region in self.regions:
                country_passengers = region.get_passengers(
                    self.config["flights"]["travelers"]
                )
                passengers += country_passengers
                num_passengers.append(len(country_passengers))
            shuffle(passengers)
            idx = 0
            for num, region in zip(num_passengers, self.regions):
                if num == 0:
                    continue
                country_passengers = passengers[idx : idx + num]
                idx += num
                region.put_passengers(country_passengers)

        for region in self.regions:
            self.statistic.add_data(self.step_num, region.name, region.statistic)
        self.statistic.sum_step(self.step_num)

        self.step_num += 1
