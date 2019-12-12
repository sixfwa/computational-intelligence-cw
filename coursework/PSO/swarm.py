from tools import load_data
from PSO.particle import Particle
import random
import time
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
        self.test_data, self.test_targets = load_data("cwk_test")
        self.test_targets = list(self.test_targets)
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

    def timed_run(self, seconds):
        start = time.time()
        finish = start + seconds
        self.set_particle_costs()
        while start < finish:
            self.set_global_best()
            self.update_velocity()
            self.move_particles()
            self.update_personal_bests()
            start = time.time()

    def run(self, iterations):
        self.set_particle_costs()
        for k in range(iterations):
            self.set_global_best()
            self.update_velocity()
            self.move_particles()
            self.update_personal_bests()

    def test(self):
        cost = 0
        for i in range(len(self.test_targets)):
            pred = sum(
                [a * b for a, b in zip(self.global_best_position, list(self.test_data[i]))])
            print("Target: {}\tPrediction: {}".format(
                self.test_targets[i], pred))
            cost += abs(pred - self.test_targets[i])

        print("Test Cost: {}".format(cost * (1 / len(self.test_targets))))

    # def test(self):
        # n = len(self.test_targets)
        # total = 0
        # for i in range(n):
        # total += abs(self.estimate(self.global_best_position, i) - )
