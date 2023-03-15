import numpy as np

from world.agent import Agent


class Region:
    def __init__(self, width, heigth, num_agents, shape="rectangle"):
        self.shape = shape
        self.width = width
        self.heigth = heigth
        self.agents = []
        for _ in range(num_agents):
            pos = (np.random.randint(self.width), np.random.randint(self.heigth))
            self.agents.append(Agent(pos))

    def step(self):
        for agent in self.agents:
            agent.step()
