import time
import random
from utils import shortest_tour, swap_elements, sorted_tours


# Parameters CompleteGraph and time limit
def random_search(graph, limit):
    number_of_tours = graph.number_of_tours()
    tours = {}
    start = time.time()
    finish = start + limit
    while start < finish:
        # {tour (tuple): cost (float)}
        tour = graph.random_tour()
        cost = graph.get_tour_cost(tour)
        if not tour in tours:
            tours[tour] = cost
        start = time.time()
    shortest = shortest_tour(tours)
    return shortest


# Takes a tour as input and returns the 2-opt neighbourhood of
# the tour as output
def two_opt_neighbourhood(tour):
    switched_tours = []
    for i in range(len(tour)):
        for j in range(len(tour)):
            switched = swap_elements(tour, i, j)
            if not switched in switched_tours and switched != tour and not switched[::-1] in switched_tours:
                switched_tours.append(switched)
    return switched_tours


# Best Neighbour Step Function
# Takes a neighbourhood (with the same structure as that returned by the two opt function)
# and returns the shortest tour in the neighbourhood
def best_neighbourhood(graph, tour):
    neighbourhood_tours = two_opt_neighbourhood(tour)
    cost_dictionary = {}
    for neighbourhood_tour in neighbourhood_tours:
        cost_dictionary[neighbourhood_tour] = graph.get_tour_cost(
            neighbourhood_tour)

    shortest = shortest_tour(cost_dictionary)
    return shortest


# Combining the above algorithm's.
# After generating a random tour it should repeatedly try to make
# the best local improving move. When a local optimum is reached,
# it should generate a new random solution and start the local
# search procedure from there. This process should continue until
# the set timer limit expires.

# After generating a random tour it should repeatedly try to make
# the best local improving move
def local_search(graph, limit):
    best_tour = graph.random_tour()
    best_cost = graph.get_tour_cost(best_tour)
    best_tours = {}
    start = time.time()
    finish = start + limit
    while start < finish:
        new_tour = best_neighbourhood(graph, best_tour)[0]
        new_cost = graph.get_tour_cost(new_tour)
        if new_cost < best_cost:
            best_tour = new_tour
            best_cost = new_cost
            best_tours[best_tour] = best_cost
        else:
            best_tour = graph.random_tour()
            best_cost = graph.get_tour_cost(best_tour)
        start = time.time()

    return shortest_tour(best_tours)
