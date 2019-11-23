import operator


def from_csv(file, skip):
    data = []
    with open("{}.csv".format(file), "r") as f:
        content = f.readlines()
        for i in range(skip):
            content.pop(0)

    for item in content:
        new_item = item.rstrip()
        new_item = new_item.split(',')
        float_item = [float(x) for x in new_item]
        data.append(float_item)

    return data


# Returns the shortest tour from a dictionary of tours
def shortest_tour(tours):
    return min(tours.items(), key=operator.itemgetter(1))


# Returns a sorted dictionary of the tours from the cheapest to the
# most expensive
def sorted_tours(tours):
    return sorted(tours.items(), key=operator.itemgetter(1))


# Swap two element positions in a list
def swap_elements(tour, pos_1, pos_2):
    list_tour = list(tour)
    list_tour[pos_1], list_tour[pos_2] = list_tour[pos_2], list_tour[pos_1]
    tuple_tour = tuple(list_tour)
    return tuple_tour


# d1 = from_csv("ulysses16")
# d2 = from_csv("cities18_9")
# print(d2)
