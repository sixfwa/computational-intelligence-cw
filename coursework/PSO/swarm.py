from tools import load_data
from particle import Particle
"""
Pseudocode
BEGIN 
    INITIALISE population
    REPEAT UNTIL (termination condition IS satisfied) DO
        UPDATE global best
        FOR EACH (particle IN population) DO
            1. UPDATE velocity AND position
            2. EVALUATE new position
            3. UPDATE personal best
        OD
    OD
END
"""


class Swarm:
    """
    global best position will be an array of the best set of particles
    """

    def __init__(self):
        self.swarm = []
        self.train_data, self.train_targets = load_data("cwk_train")
        self.train_targets = list(self.train_targets)
        for i in range(len(self.train_data[0])):
            self.swarm.append(Particle())
        self.gbest_position = [p.pbest_position for p in self.swarm]

    def estimate(self, train_index):
        return sum([a * b for a, b in zip(self.gbest_position, self.train_data[train_index])])

    def cost(self, train_index):
        estimate = self.estimate(train_index)
        return abs(estimate - self.train_targets[train_index])


swarm = Swarm()
print(swarm.estimate(0))
print(swarm.cost(0))
