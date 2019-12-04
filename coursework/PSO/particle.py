from random import random


class Particle:
    """
    A particle will represent a weight. Which will
    be a single integer.
    """

    def __init__(self):
        self.position = 1
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = abs(self.position - random()) / 2

    def move(self):
        self.position = self.position + self.velocity


# p1 = Particle()
# p2 = Particle()
# print(p1.position)
# print(p1.velocity)
# print(p2.position)
# print(p2.velocity)
