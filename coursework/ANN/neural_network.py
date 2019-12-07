from tools import load_data
import random


class Neuron:

    def __init__(self):
        self.inputs = None
        self.weights = []
        self.bias = 0

    def initialise_weights(self):
        for i in range(len(self.inputs)):
            self.weights.append(random.random())

    def weighted_sum(self):
        self.w_sum = sum(
            [a * b for a, b in zip(self.inputs, self.weights)]) + (self.bias * random.random())

    def relu(self):
        self.output = max(0, self.w_sum)


class Layer:

    def __init__(self, size):
        self.neurons = []
        for i in range(size):
            self.neurons.append(Neuron())

    def get_outputs(self):
        self.outputs = []
        for neuron in self.neurons:
            self.outputs.append(neuron.output)
        self.outputs = tuple(self.outputs)
        return self.outputs


class NeuralNetwork:

    def __init__(self):
        self.train_data = []
        self.train_targets = []
        train_data_raw, train_targets_raw = load_data("cwk_train")
        for i in train_data_raw:
            self.train_data.append(tuple(i))
        for i in train_targets_raw:
            self.train_targets.append(tuple(i))


td, tt = load_data("cwk_train")
train_data = []
train_targets = []
for i in td:
    train_data.append(tuple(i))
for i in tt:
    train_targets.append(i)

# The input layer for the first training sample
first_sample = train_data[0]

# Create the first hidden layer
layerOne = Layer(4)
for neuron in layerOne.neurons:
    neuron.inputs = first_sample
    neuron.initialise_weights()

# set weighted sum and output for each neuron in layer one
for neuron in layerOne.neurons:
    neuron.weighted_sum()
    neuron.relu()

print("Hidden Layer One Output: {}".format(layerOne.get_outputs()))

# Create the second hidden layer
layerTwo = Layer(4)
for neuron in layerTwo.neurons:
    neuron.inputs = layerOne.get_outputs()
    neuron.initialise_weights()

# set weighted sum and output for each neuron in layer two
for neuron in layerTwo.neurons:
    neuron.weighted_sum()
    neuron.relu()

print("Hidden Layer Two Output: {}".format(layerTwo.get_outputs()))

# Create the output layer
layerOutput = Layer(1)
for neuron in layerOutput.neurons:
    neuron.inputs = layerTwo.get_outputs()
    neuron.initialise_weights()

# Calculate the output
layerOutput.neurons[0].weighted_sum()
print(layerOutput.neurons[0].w_sum)


# print(layerOne.neurons)
# neuronOne = Neuron()
# neuronOne.inputs = train_data[0]
# neuronOne.initialise_weights()
# print(len(neuronOne.inputs))
# print(len(neuronOne.weights))
# neuronOne.weighted_sum()
# print(neuronOne.w_sum)
# neuronOne.relu()
# print(neuronOne.output)
