import numpy as np
import random


class Particle:

    def __init__(self):
        pos = self.initialise_position()
        vel = np.random.rand(13)
        self.position = list(pos)
        self.velocity = list(abs(pos - vel) / 2)
        self.position_value = None

    def set_personal_best(self):
        self.personal_best_position = self.position
        self.personal_best_value = self.position_value

    def initialise_position(self):
        pos = []
        for i in range(13):
            pos.append(random.uniform(-2, 2))

        return pos
