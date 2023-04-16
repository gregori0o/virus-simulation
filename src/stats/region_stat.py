from collections import defaultdict


class RegionStatistic:
    def __init__(self):
        self.sick = 0
        self.healthy = 0
        self.deaths = 0

        self.sick_disease = defaultdict(lambda: 0)
        self.immune_disease = defaultdict(lambda: 0)

    def get_total(self):
        return self.sick + self.healthy

    def get_healthy(self, virus_name=None):
        if virus_name is None:
            return self.healthy
        return (
            self.healthy
            - self.sick_disease[virus_name]
            - self.immune_disease[virus_name]
        )

    def get_sick(self, virus_name=None):
        if virus_name is None:
            return self.sick
        return self.sick_disease[virus_name]

    def get_immune(self, virus_name):
        return self.immune_disease[virus_name]

    def get_deaths(self):
        return self.deaths

    def healthy_birth(self):
        self.healthy += 1

    def sick_birth(self, virus_name):
        self.sick += 1
        self.sick_disease[virus_name] += 1

    def death(self, agent):
        self.deaths += 1
        if agent.is_agent_sick():
            self.sick -= 1
            for virus_name in agent.sick_info.keys():
                self.sick_disease[virus_name] -= 1
            for virus_name in agent.immunity_info.keys():
                self.immune_disease[virus_name] -= 1
        else:
            self.healthy -= 1

    def end_immune(self, virus_name):
        self.immune_disease[virus_name] -= 1

    def start_sick(self, virus_name):
        self.sick_disease[virus_name] += 1

    def end_sick(self, virus_name):
        self.sick_disease[virus_name] -= 1
        self.immune_disease[virus_name] += 1

    def start_be_sick(self):
        self.healthy -= 1
        self.sick += 1

    def end_be_sick(self):
        self.healthy += 1
        self.sick -= 1
