from GA.genetic_algorithm import GeneticAlgorithm
from PSO.swarm import Swarm
import matplotlib.pyplot as plt
from GA.tools import load_data


def run_genetic_algorithm():
    print("Running the Genetic Algorithm")
    pop_size = int(input("Population Size: "))
    elite_size = int(input("Selection Size: "))
    k = int(input("K Value for Tournament Selection: "))
    lower = int(input("Lower Bound for Uniform Mutation: "))
    upper = int(input("Upper Bound for Uniform Mutation: "))
    seconds = int(input("Number of Seconds: "))
    ga = GeneticAlgorithm(pop_size, elite_size, upper, lower, k, seconds)
    best, generations = ga.timed_run()
    print("\nOptimal Weights: {}".format(best[0]))
    print("Cost: {}".format(best[1]))
    print("Number of Generations: {}\n".format(generations))
    ga.test()


def run_pso_algorithm():
    print("Running PSO Algorithm")
    inertia = float(input("Inertia (best -> 0.721): "))
    cognitive = float(input("Cognitive Coefficient (best -> 1.1193): "))
    social = float(input("Social Coefficient (best -> 1.1193): "))
    particles = int(input("Number of Particles: "))
    seconds = int(input("Number of Seconds: "))
    swarm = Swarm(inertia, cognitive, social, particles)
    swarm.timed_run(seconds)
    print("\nOptimal Weights: {}".format(swarm.global_best_position))
    print("Cost: {}".format(swarm.global_best_value))
    swarm.test()


# run_genetic_algorithm()
# run_pso_algorithm()
if __name__ == "__main__":
    print(chr(27) + "[2J")
    alg = int(
        input("Enter 1 for Genetic Algorithm\nEnter 2 for Particle Swarm Optimisation\n"))
    if alg == 1:
        run_genetic_algorithm()
    if alg == 2:
        run_pso_algorithm()
    else:
        exit()
# ga = GeneticAlgorithm(100, 10, 3, 1000)
# # best = ga.run()
# best, _ = ga.timed_run(1)
# print(best)
# seconds = []
# score = []
# for i in range(1, 11):
#     avg = 0
#     for j in range(1):
#         ga = GeneticAlgorithm(100, 20, 3, 1000)
#         best, _ = ga.timed_run(i)
#         avg += best[1]
#     # avg = avg / 5
#     seconds.append(i)
#     score.append(avg)

# print(seconds)
# print(score)
# plt.plot(seconds, score)
# plt.show()
# genetic_algorithm_train()
# Testing how well the genetic algorithm perfoms based on some changing
# variable
# How the number of generations changes the solutions
# gens_list = []
# scores = []
# for p in range(10, 50, 10):
#     pop_size = 100
#     elite_size = 20
#     k = 3
#     gens = p
#     ga = GeneticAlgorithm(
#         pop_size=pop_size, elite_size=elite_size, K=k, gens=gens)
#     best = ga.run()
#     gens_list.append(p)
#     scores.append(ga.test())
# # genetic_algorithm_train()
# print(pop)
# print(scores)
# plt.plot(gens_list, scores)
# plt.title("")
# plt.show()
