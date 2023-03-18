import itertools
import random

import numpy as np
from shapely.geometry import Point, Polygon
from world.agent import Agent


class Region:
    id_obj = itertools.count()

    def __init__(self, name, vertices, color, num_healthy_agents, sick_agents_arr, viruses):
        self.id = next(Region.id_obj)
        self.vertices = vertices
        self.name = name
        self.color = color
        self.agents_pos = None
        self.agents = []

        self._generate_agents(num_healthy_agents)
        self._generate_sick_agents(sick_agents_arr, viruses)
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

    def is_in_region_area(self, point):
        """
        Check if a point is inside a polygon defined by an array of vertices.

        Arguments:
        point -- a tuple representing the (x, y) coordinates of the test point.
        vertices -- a list of tuples representing the (x, y) coordinates of the vertices of the polygon.

        Returns:
        True if the point is inside the polygon, False otherwise.
        """
        # Cast a ray from the test point to the right
        # Count the number of times the ray intersects with the edges of the polygon
        # If the number of intersections is odd, the point is inside the polygon
        # If the number of intersections is even, the point is outside the polygon

        num_intersections = 0
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            if ((self.vertices[i][1] > point[1]) != (self.vertices[j][1] > point[1])) and (
                    point[0] < (self.vertices[j][0] - self.vertices[i][0]) * (point[1] - self.vertices[i][1]) / (
                    self.vertices[j][1] - self.vertices[i][1]) + self.vertices[i][0]):
                num_intersections += 1

        return num_intersections % 2 == 1

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
                self.agents.append(Agent(pos,
                                         self,
                                         is_sick=True,
                                         sick_time=virus.sick_time,
                                         virus_name=virus.name,
                                         remaining_immunity=virus.immunity_time)
                                   )

    def _generate_agent_pos_inside_region(self):
        # Create a polygon object from the vertices
        polygon = Polygon(np.array(self.vertices))

        # Find the bounding box of the polygon
        min_x, min_y, max_x, max_y = polygon.bounds

        # Generate random points until a point is found inside the polygon
        while True:
            # Generate a random point within the bounding box
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            point = Point(x, y)

            # check if the point is inside the convex hull
            if polygon.contains(point):
                break
        return x, y


