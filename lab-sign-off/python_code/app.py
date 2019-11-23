from graph import CompleteGraph
from algorithms import *
from utils import from_csv, shortest_tour
from genetic_algorithm import GeneticAlgorithm

# ulysses16 -> 3
data = from_csv("cities90_11", 3)

graph = CompleteGraph()

# Add information from ulysses16 to the CompleteGraph
for item in data:
    name = item[0]
    coordinate = (item[1], item[2])
    graph.add_node(name, coordinate)


def demonstrate_cost():
    tour = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    print("\t\t Demonstrate Cost of Tour")
    print("Tour: {}".format(tour))
    print("Cost: {}\n".format(graph.get_tour_cost(tour)))


def demonstrate_random_search(limit):
    print("\t\tRandom Search Algorithm Example ({} seconds)".format(limit))
    shortest = random_search(graph, limit)
    print("Shortest Tour: {}".format(shortest[0]))
    print("Cost: {}\n".format(shortest[1]))


def demonstrate_two_opt_neighbourhood():
    tour = graph.random_tour()
    print("2-Opt Neighbourhood Example")
    print("Tour: {}".format(tour))
    for opt_tour in two_opt_neighbourhood(tour):
        print(opt_tour)


def demonstrate_best_neighbourhood():
    tour = graph.random_tour()
    print("Random Tour: {}".format(tour))
    print(best_neighbourhood(graph, tour))


def demonstrate_local_search(limit):
    print("\t\tLocal Search Algorithm Example ({} seconds)".format(limit))
    shortest = local_search(graph, limit)
    print("Shortest Tour: {}".format(shortest[0]))
    print("Cost: {}\n".format(shortest[1]))


def demonstrate_genetic_algorithm(pop_size, elite_size, rate, gens):
    print("\t\tGenetic Algorithm")
    print("Initial Population Size: {}".format(pop_size))
    print("Elite Size: {}".format(elite_size))
    print("Mutation Rate: {}".format(rate))
    print("Generations: {}".format(gens))
    ga = GeneticAlgorithm(graph, pop_size, elite_size, rate, gens)
    tour, t = ga.run()
    print("Shortest Tour: {}".format(tour[0]))
    print("Cost: {}".format(tour[1]))
    print("Number of Seconds Taken: {}\n".format(t))


def main():
    demonstrate_cost()
    demonstrate_random_search(1)
    demonstrate_local_search(1)
    demonstrate_genetic_algorithm(10, 5, 0.02, 100)


if __name__ == "__main__":
    main()
