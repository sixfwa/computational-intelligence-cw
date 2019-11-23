from math import factorial, sqrt
from random import shuffle


class CompleteGraph:
    def __init__(self):
        self.graph = {}

    def add_node(self, name, coordinates):
        self.graph[name] = coordinates

    def get_coordinate(self, name):
        return self.graph[name]

    # returns a list of all the nodes on the graph
    def get_nodes(self):
        nodes = [node for node in self.graph]
        return nodes

    def node_exists(self, node):
        return node in self.graph

    def delete_node(self, node):
        if self.node_exists(node):
            del self.graph[node]

    def number_of_nodes(self):
        return len(self.get_nodes())

    def number_of_tours(self):
        return factorial(self.number_of_nodes() - 1)

    # Euclidean distance between two nodes.
    def euclidean_distance(self, node_1, node_2):
        if self.node_exists(node_1) and self.node_exists(node_2):
            node_1_coord = self.graph[node_1]
            node_2_coord = self.graph[node_2]
            x_dist = (node_2_coord[0] - node_1_coord[0]) ** 2
            y_dist = (node_2_coord[1] - node_1_coord[1]) ** 2

            return sqrt(x_dist + y_dist)

    def get_tour_cost(self, nodes):
        cost = 0
        for i in range(len(nodes)):
            if i != (len(nodes) - 1):
                cost += self.euclidean_distance(nodes[i], nodes[i+1])
        cost += self.euclidean_distance(nodes[0], nodes[len(nodes) - 1])
        return cost

    def random_tour(self):
        nodes = self.get_nodes()
        shuffle(nodes)
        tuple_nodes = tuple(nodes)
        return tuple_nodes
