import numpy as np


# Loads the training data from the csv file and returns
# it as a numpy array
def load_data(filename):
    data = []
    with open("data/{}.csv".format(filename), "r") as f:
        content = f.readlines()

    for item in content:
        new_item = item.rstrip()
        new_item = new_item.split(',')
        float_item = [float(x) for x in new_item]
        data.append(float_item)

    data_array = np.asarray(data)
    target = data_array[:, 0]
    data = data_array[:, 1:]
    return data, target
