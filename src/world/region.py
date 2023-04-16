import itertools
import random
from collections import defaultdict

import numpy as np
from shapely.geometry import Point, Polygon

from world.agent import Agent


class RegionStatistic:
    def __init__(self):
        self.sick = 0
        self.healthy = 0

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

    def healthy_birth(self):
        self.healthy += 1

    def sick_birth(self, virus_name):
        self.sick += 1
        self.sick_disease[virus_name] += 1

    def death(self, agent):
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


class Region:
    id_obj = itertools.count()

    def __init__(
        self, name, vertices, color, num_healthy_agents, sick_agents_arr, viruses
    ):
        self.id = next(Region.id_obj)
        self.vertices = vertices
        self.name = name
        self.color = color
        self.agents_pos = None
        self.agents = []
        self.polygon = Polygon(np.array(vertices))
        self.statistic = RegionStatistic()

        self._generate_agents(num_healthy_agents)
        self._generate_sick_agents(sick_agents_arr, viruses)
        self.make_pos_dir()

    def step(self):
        # infection method - can be moved under agents step
        self.infect()

        # agents moving
        for agent in self.agents:
            agent.step()
        self.make_pos_dir()

    def make_pos_dir(self):
        self.agents_pos = {}
        for agent in self.agents:
            self.agents_pos[agent.pos] = self.agents_pos.get(agent.pos, []) + [agent]

    def get_neighborhood(self, agent, size=1):
        x, y = agent.pos
        neighborhood = []
        for i in range(x - size, x + size + 1):
            for j in range(y - size, y + size + 1):
                neighborhood += self.agents_pos.get((i, j), [])
        return [n for n in neighborhood if n != agent]

    def is_in_region_area(self, point):
        return self.polygon.contains(Point(point))

    def _generate_agents(self, num_agents):
        for _ in range(num_agents):
            pos = self._generate_agent_pos_inside_region()
            self.agents.append(Agent(pos, self))

    def _generate_sick_agents(self, sick_agents_arr, viruses):
        # In case if we want to create two viruses per simulation
        for sick_agents in sick_agents_arr:
            virus = next(virus for virus in viruses if virus.name == sick_agents[1])
            for _ in range(int(sick_agents[0])):
                pos = self._generate_agent_pos_inside_region()
                self.agents.append(Agent(pos, self, virus=virus))

    def _generate_agent_pos_inside_region(self):
        # Find the bounding box of the polygon
        min_x, min_y, max_x, max_y = self.polygon.bounds

        # Generate random points until a point is found inside the polygon
        while True:
            # Generate a random point within the bounding box
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            point = Point(x, y)

            # check if the point is inside the convex hull
            if self.polygon.contains(point):
                break
        return x, y

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def infect(self):
        for agent in self.agents:
            # if agent is NOT sick - continue iteration
            if agent.is_agent_sick():
                if not agent.sick_info:
                    raise "Agent is sick without having virus"

                # maybe it's better to iterate over agants again and check their position?
                for _, virus in agent.sick_info.values():
                    self.infect_by_position(agent, virus)

    def infect_by_position(self, agent, virus):
        x, y = agent.pos
        infection_distance = agent.sick_info[virus.name][1].infection_distance
        for i in range(max(0, x - infection_distance), x + infection_distance + 1):
            for j in range(max(0, y - infection_distance), y + infection_distance + 1):
                for neighbor in self.agents_pos.get((i, j), []):
                    if not neighbor.is_agent_sick(virus.name):
                        if agent.calculate_infection(neighbor, virus.name):
                            neighbor.set_sickness(virus)
