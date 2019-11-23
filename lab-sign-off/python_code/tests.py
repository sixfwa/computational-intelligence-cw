import unittest
from graph import CompleteGraph
from algorithms import *


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.g = CompleteGraph()
        self.g.add_node(1, (0, 0))
        self.g.add_node(2, (0, 1))
        self.g.add_node(3, (1, 1))
        self.g.add_node(4, (1, 0))

    def test_euclidean_distance(self):
        self.assertEqual(self.g.euclidean_distance(1, 2), 1)
        self.assertEqual(self.g.euclidean_distance(2, 3), 1)
        self.assertEqual(self.g.euclidean_distance(3, 4), 1)

    def test_tour_cost(self):
        a = self.g.euclidean_distance(1, 2)
        b = self.g.euclidean_distance(2, 3)
        c = self.g.euclidean_distance(3, 4)
        d = self.g.euclidean_distance(3, 4)
        cost = a + b + c + d
        self.assertEqual(self.g.get_tour_cost([1, 2, 3, 4]), cost)


class AlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.g = CompleteGraph()
        self.g.add_node(1, (1, 1))
        self.g.add_node(2, (2, 3))
        self.g.add_node(3, (6, 3))
        self.g.add_node(4, (6, 7))
        self.g.add_node(5, (7, 4))
        self.g.add_node(6, (5, 3))

    # def test_random_search(self):
    #     rs = random_search(self.g, 10)
    #     self.assertEqual(rs[0], (4, 2, 1))
    #     self.assertEqual(rs[1], 6.23606797749979)

    def test_two_opt_neighbourhood(self):
        small_tour = (1, 2, 3)
        two_opt = two_opt_neighbourhood(small_tour)
        self.assertEqual(sorted(two_opt), sorted(
            [(2, 1, 3), (1, 3, 2), (3, 2, 1)]))

    def test_best_neighbour(self):
        tour = (1, 4, 2, 5, 3, 6)
        self.assertEqual(best_neighbourhood(self.g, tour),
                         ((1, 2, 4, 5, 3, 6), 17.941549404533227))


class GeneticAlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.g = CompleteGraph()
        self.g.add_node(1, (1, 1))
        self.g.add_node(2, (2, 3))
        self.g.add_node(3, (6, 3))
        self.g.add_node(4, (6, 7))
        self.g.add_node(5, (7, 4))
        self.g.add_node(6, (5, 3))
        self.population = initial_population(self.g, 4)

    def test_initial_population(self):
        self.assertEqual(len(self.population), 4)

    def test_selection(self):
        ranked_tours = rank_tours(self.g, self.population)
        sel = selection(rank_tours, 2)
        self.assertEqual(len(selection), 2)


if __name__ == '__main__':
    unittest.main()
