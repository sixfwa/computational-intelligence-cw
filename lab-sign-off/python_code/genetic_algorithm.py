from utils import sorted_tours, shortest_tour
import random
import time


class GeneticAlgorithm:
    # 1. First create a population with random tours - DONE
    # 2. Rank each of the tours within the population - DONE
    # 3. Select the best tours based on the elite size store them - DONE
    # 4. Function which breeds tours from the elite dictionary - DONE
    # 5. Breed the tours from the elite dictionary - DONE
    # 6. Mutate the children - DONE
    # 7. Create the next generation - DONE
    def __init__(self, graph, pop_size, elite_size, rate, gens):
        self.graph = graph
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.rate = rate
        self.gens = gens
        self.start = None
        self.end = None

    def initialise_population(self):
        self.population = []
        for i in range(self.pop_size):
            self.population.append(self.graph.random_tour())

    def rank_population(self):
        ranked = {}
        for individual in self.population:
            ranked[individual] = self.graph.get_tour_cost(individual)

        return sorted_tours(ranked)

    # Parent selection by tournament
    def selection_by_tournament(self, ranked):
        self.elite = {}
        for i in range(self.elite_size):
            self.elite[ranked[i][0]] = ranked[i][1]

    # Order 1 crossover for TSP
    def breed(self, parent_1, parent_2):
        child = []
        child_p1 = []
        child_p2 = []

        gene_a = int(random.random() * len(parent_1))
        gene_b = int(random.random() * len(parent_2))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child_p1.append(parent_1[i])

        child_p2 = [elem for elem in parent_2 if elem not in child_p1]

        child = child_p1 + child_p2

        return tuple(child)

    def breed_elite_population(self):
        children = []
        elite_tours = [elite_tour for elite_tour in self.elite]

        for i in range(len(elite_tours)):
            child = self.breed(elite_tours[i],
                               elite_tours[len(elite_tours) - i - 1])
            children.append(child)

        return children

    def mutate(self, child):
        child = list(child)
        for swapped in range(len(child)):
            if (random.random() < self.rate):
                swap_with = int(random.random() * len(child))

                location_1 = child[swapped]
                location_2 = child[swap_with]

                child[swapped] = location_2
                child[swap_with] = location_1

        return tuple(child)

    def mutate_children(self):
        mutated_children = []
        children = self.breed_elite_population()
        for i in range(len(children)):
            mutated_child = self.mutate(children[i])
            mutated_children.append(mutated_child)

        return mutated_children

    def next_generation(self):
        # Create a dictionary out of the mutated children
        new_gen = {}
        for child in self.mutate_children():
            new_gen[child] = self.graph.get_tour_cost(child)

        self.elite.update(new_gen)

        self.elite = sorted_tours(self.elite)[:3]
        new_elite = {}
        for item in self.elite:
            new_elite[item[0]] = item[1]

        self.elite = new_elite

    def run(self):
        self.start = time.time()
        # initialise the population
        self.initialise_population()
        # rank the population
        self.selection_by_tournament(self.rank_population())
        for i in range(self.gens):
            self.breed_elite_population()
            self.mutate_children()
            self.next_generation()
        self.end = time.time()
        time_taken = self.end - self.start
        return shortest_tour(self.elite), time_taken
