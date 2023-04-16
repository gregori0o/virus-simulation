from world.region import Region
from world.virus import Virus


class World:
    def __init__(self, config):
        self.config = config
        self.viruses = []
        self.regions = []
        self._create_viruses(config["viruses"])
        self._create_regions(config["regions"])

    def get_regions(self):
        return self.regions

    def get_viruses(self):
        return self.viruses

    def _create_regions(self, regions):
        for region in regions:
            self.regions.append(
                Region(
                    region["name"],
                    region["vertices"],
                    region["color"],
                    region["number_of_healthy_agents"],
                    region["number_of_infected_agents"],
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
