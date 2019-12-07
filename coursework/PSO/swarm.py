from tools import load_data
from particle import Particle
import random
"""
Pseudocode
BEGIN
    INITIALISE population [DONE]
    REPEAT UNTIL (termination condition IS satisfied) DO
        UPDATE global best [DONE]
        FOR EACH (particle IN population) DO
            1. UPDATE velocity AND position [DONE]
            2. EVALUATE new position
            3. UPDATE personal best
        OD
    OD
END
"""


class Swarm:

    def __init__(self, inertia, cognitive, social, num_particles):
        self.train_data, self.train_targets = load_data("cwk_train")
        self.train_targets = list(self.train_targets)
        self.num_particles = num_particles
        self.inertia = inertia
        self.cognitive = cognitive
        self.social = social
        # initialise population
        self.particles = []
        for i in range(self.num_particles):
            self.particles.append(Particle())

    def estimate(self, position, sample):
        return sum([a * b for a, b in zip(position, sample)])

    def set_particle_costs(self):
        """
        This method will be called when initialising
        """
        for particle in self.particles:
            co = 0
            for i in range(len(self.train_data)):
                sample = list(self.train_data[i])
                co += abs(self.estimate(particle.position,
                                        sample) - self.train_targets[i])
            cost = (1 / len(self.train_data)) * co
            particle.position_value = cost
            particle.set_personal_best()
        self.global_best_position = self.particles[0].position
        self.global_best_value = self.particles[0].position_value

    def set_global_best(self):
        for particle in self.particles:
            if particle.position_value < self.global_best_value:
                self.global_best_position = particle.position
                self.global_best_value = particle.position_value

    def evaluate_particle_position(self, particle):
        """
        Takes a particle as an argument and sets 
        the particle position costof that particle
        """
        co = 0
        for i in range(len(self.train_data)):
            sample = list(self.train_data[i])
            co += abs(self.estimate(particle.position,
                                    sample) - self.train_targets[i])
        particle.position_value = co * (1 / len(self.train_data))

    def update_personal_bests(self):
        for particle in self.particles:
            self.evaluate_particle_position(particle)
            if particle.position_value < particle.personal_best_value:
                particle.personal_best_position = particle.position
                particle.personal_best_value = particle.position_value

    def update_velocity(self):
        for particle in self.particles:
            for index in range(len(particle.position)):
                i = self.inertia * particle.velocity[index]
                c = self.cognitive * random.random() * \
                    (particle.personal_best_position[index] -
                     particle.position[index])
                s = self.social * random.random() * \
                    (self.global_best_position[index] -
                     particle.position[index])
                particle.velocity[index] = i + c + s

    def move_particles(self):
        for particle in self.particles:
            particle.position = [
                a + b for a, b in zip(particle.position, particle.velocity)]
            particle.position_value = self.evaluate_particle_position(particle)

    def run(self, iterations):
        self.set_particle_costs()
        for k in range(iterations):
            self.set_global_best()
            self.update_velocity()
            self.move_particles()
            self.update_personal_bests()


swarm = Swarm(0.721, 1.1193, 1.1193, 38)
swarm.run(600)
print(swarm.global_best_value)
weights = swarm.global_best_position

test_data, test_target = load_data("cwk_test")
sample = list(test_data[0])
pred = swarm.estimate(weights, sample)
print("Pred: {}".format(pred))
print("Real: {}".format(test_target[0]))
print(weights)
