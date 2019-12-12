from tools import load_data
import numpy as np
import operator
import random
import time

# Load training data and targets
train_data, train_targets = load_data("cwk_train")
train_targets = list(train_targets)


class GeneticAlgorithm:

    def __init__(self, pop_size, elite_size, K, upper, lower, seconds):
        self.train_data, self.train_targets = load_data("cwk_train")
        self.test_data, self.test_targets = load_data("cwk_test")
        self.train_targets = list(self.train_targets)
        self.test_targets = list(self.test_targets)
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.upper = upper
        self.lower = lower
        self.seconds = seconds
        self.K = K
        self.population = []

    def initialise_population(self):
        n = len(train_data[0])
        for i in range(self.pop_size):
            ind = []
            for i in range(13):
                ind.append(random.uniform(-3, 3))
            self.population.append(tuple(ind))

    def estimate(self, individual, train_index):
        return sum([a * b for a, b in zip(individual, self.train_data[train_index])])

    def cost_function(self, individual):
        n = len(self.train_data)
        total = 0
        for i in range(n):
            total += abs(self.estimate(individual, i) -
                         self.train_targets[i])

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
        child_1 = []
        child_2 = []
        pos = 0
        while pos == 0:
            pos = int(random.random() * len(parent_1))

        child_1.extend(parent_1[:pos])
        child_1.extend(parent_2[pos:])
        child_2.extend(parent_2[:pos])
        child_2.extend(parent_1[pos:])

        # child_1 = [0] * len(parent_1)
        # gene_a = 0
        # gene_b = 0
        # while gene_a == gene_b:
        #     gene_a = int(random.random() * len(parent_1))
        #     gene_b = int(random.random() * len(parent_1))

        # start_gene = min(gene_a, gene_b)
        # end_gene = max(gene_a, gene_b)
        # # Child 1
        # for i in range(start_gene, end_gene + 1):
        #     child_1[i] = parent_1[i]

        # # Child 1
        # for i in range(len(parent_2)):
        #     if i not in range(start_gene, end_gene + 1):
        #         child_1[i] = parent_2[i]

        # missing = list(set(parent_2) - set(parent_1))
        # count = 0
        # for i in range(len(child_1)):
        #     if child_1[i] == 0:
        #         child_1[i] = missing[count]
        #         count += 1

        # child_2 = parent_1 + parent_2
        # child_2 = list(child_2)
        # for elem in child_1:
        #     if elem in child_2:
        #         child_2.remove(elem)

        return tuple(child_1), tuple(child_2)

    def breed_population(self):
        children = []
        elite_individuals = [ind for ind in self.elite]
        for i in range(len(elite_individuals)):
            child_1, child_2 = self.breed(
                elite_individuals[i], elite_individuals[len(elite_individuals) - i - 1])
            children.append(child_1)
            children.append(child_2)

        return children

    def mutate(self, child):
        child = list(child)

        location = int(random.random() * len(child))
        child[location] = random.uniform(self.lower, self.upper)

        # location_1 = 0
        # location_2 = 0
        # while location_1 == location_2:
        #     location_1 = int(random.random() * len(child))
        #     location_2 = int(random.random() * len(child))
        # genotype_one = child[location_1]
        # genotype_two = child[location_2]
        # child[location_1] = genotype_two
        # child[location_2] = genotype_one

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
        self.elite = new_elite

    def run(self):
        self.initialise_population()
        self.selection_by_tournament(self.K)

        for i in range(self.gens):
            self.breed_population()
            self.mutate_children()
            self.next_generation()
        return min(self.elite.items(), key=operator.itemgetter(1))

    def timed_run(self):
        start = time.time()
        finish = start + self.seconds
        generations = 0
        self.initialise_population()
        self.selection_by_tournament(self.K)
        print(min(self.elite.items(), key=operator.itemgetter(1)))
        while start < finish:
            self.breed_population()
            self.mutate_children()
            self.next_generation()
            generations += 1
            start = time.time()
        return min(self.elite.items(), key=operator.itemgetter(1)), generations

    def test(self):
        best = min(self.elite.items(), key=operator.itemgetter(1))[0]
        cost = 0
        for i in range(len(self.test_targets)):
            pred = sum([a * b for a, b in zip(best, list(self.test_data[i]))])
            print("Target: {}\tPrediction: {}".format(
                self.test_targets[i], pred))
            cost += abs(pred - self.test_targets[i])

        print("\nTest Cost: {}".format(cost * (1 / len(self.test_targets))))
