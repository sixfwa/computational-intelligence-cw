from tools import load_data
import numpy as np
import operator
import random
# TODO - Initialise population with random candidate solutions DONE
# TODO - Write cost function DONE
# TODO - Evaluate each candidate DONE
# TODO - Sort population with the best to worst

# Load training data and targets
train_data, train_targets = load_data("cwk_train")
train_targets = list(train_targets)


class GeneticAlgorithm:

    def __init__(self, pop_size, elite_size, rate, gens):
        self.train_data, self.train_targets = load_data("cwk_train")
        self.train_targets = list(self.train_targets)
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.rate = rate
        self.gens = gens
        self.population = []

    def initialise_population(self):
        n = len(train_data[0])
        for i in range(self.pop_size):
            self.population.append(tuple(np.random.rand(n)))

    def estimate(self, individual, train_index):
        return sum([a * b for a, b in zip(individual, train_data[train_index])])

    def cost_function(self, individual):
        n = len(self.train_data)
        total = 0
        for i in range(n):
            total += abs(self.estimate(individual, i) - self.train_targets[i])

        return (1 / n) * total

    def rank_population(self):
        ranked = {}
        for individual in self.population:
            ranked[individual] = self.cost_function(individual)
        return sorted(ranked.items(), key=operator.itemgetter(1))

    def selection_by_tournament(self, K):
        """
        select K individuals from the population at random and select
        the best out of those.
        """
        ranked = self.rank_population()
        self.elite = {}
        while len(self.elite) < self.elite_size:
            k_selection = {}
            for i in range(K):
                sel = random.choice(ranked)
                ranked.remove(sel)
                k_selection[sel[0]] = sel[1]
            best = min(k_selection.items(), key=operator.itemgetter(1))
            self.elite[best[0]] = best[1]

    def breed(self, parent_1, parent_2):
        child = [0] * len(parent_1)

        gene_a = 0
        gene_b = 0
        while gene_a == gene_b:
            gene_a = int(random.random() * len(parent_1))
            gene_b = int(random.random() * len(parent_1))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene + 1):
            child[i] = parent_1[i]

        for i in range(len(parent_2)):
            if i not in range(start_gene, end_gene + 1):
                child[i] = parent_2[i]

        missing = list(set(parent_2) - set(parent_1))
        count = 0
        for i in range(len(child)):
            if child[i] == 0:
                child[i] = missing[count]
                count += 1

        return tuple(child)

    def breed_population(self):
        children = []
        elite_individuals = [ind for ind in self.elite]
        for i in range(len(elite_individuals)):
            child = self.breed(
                elite_individuals[i], elite_individuals[len(elite_individuals) - i - 1])
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
        children = self.breed_population()
        for i in range(len(children)):
            mutated_child = self.mutate(children[i])
            mutated_children.append(mutated_child)
        return mutated_children

    def next_generation(self):
        # created a new empty dictionary
        new_gen = {}
        for child in self.mutate_children():
            new_gen[child] = self.cost_function(child)

        self.elite.update(new_gen)
        sorted_elite = sorted(self.elite.items(),
                              key=operator.itemgetter(1))
        new_elite = {}
        for i in range(self.elite_size):
            new_elite[sorted_elite[i][0]] = sorted_elite[i][1]
        # for item in sorted_elite:
            # new_elite[item[0]] = item[1]
        self.elite = new_elite

    def run(self):
        self.initialise_population()
        self.selection_by_tournament(5)
        for i in range(self.gens):
            self.breed_population()
            self.mutate_children()
            self.next_generation()
        return min(self.elite.items(), key=operator.itemgetter(1))


ga = GeneticAlgorithm(pop_size=100, elite_size=10, rate=0.1, gens=500)

print(ga.run())
# ga.initialise_population()
# ranked = ga.rank_population()
# ga.selection_by_tournament(5)
# print(ga.elite)
# ga.selection_by_tournament(2)
# children = ga.breed_population()
# print(len(children))
# best = ga.run()
# print(ga.elite)
# best = ga.run()
# print(best)
# elite size = elite_size * K < population

# ga.selection_by_tournament(ranked, 5)
# parents = []
# for ind in ga.elite:
#     parents.append(ind)

# for k, v in ga.elite.items():
#     print(v)

# print()
# a = sorted(ga.elite.items(), key=operator.itemgetter(1))[:3]
# print(type(a))
# for i in a:
#     print(i[1])
# print()
# p1 = parents[0]
# p2 = parents[1]
# child = ga.breed(p1, p2)
# print("Parent 1 Cost: {}".format(ga.cost_function(p1)))
# print("Parent 2 Cost: {}".format(ga.cost_function(p2)))
# print("Child Cost: {}".format(ga.cost_function(child)))
