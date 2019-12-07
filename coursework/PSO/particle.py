import numpy as np


class Particle:

    def __init__(self):
        pos = np.random.rand(13)
        vel = np.random.rand(13)
        self.position = list(pos)
        self.velocity = list(abs(pos - vel) / 2)
        self.position_value = None

    def set_personal_best(self):
        self.personal_best_position = self.position
        self.personal_best_value = self.position_value
