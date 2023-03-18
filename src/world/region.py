import numpy as np

from utils import RegionShape
from world.agent import Agent


class Region:
    def __init__(self, width, heigth, num_agents, shape=RegionShape.RECTANGLE.value):
        self.shape = shape
        self.width = width
        self.heigth = heigth
        self.agents = []
        for _ in range(num_agents):
            pos = self.generate_pos_from_map()
            self.agents.append(Agent(pos, self))
        self.make_pos_dir()

    def step(self):
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

    def is_in_map_area(self, x, y):
        """Check if x, y position is in map"""
        if self.shape == RegionShape.RECTANGLE.value:
            if x < 0 or x >= self.width or y < 0 or y >= self.heigth:
                return False
            return True
        else:
            raise NotImplementedError()

    def generate_pos_from_map(self):
        if self.shape == RegionShape.RECTANGLE.value:
            return np.random.randint(self.width), np.random.randint(self.heigth)
        else:
            raise NotImplementedError()
