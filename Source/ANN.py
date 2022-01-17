import numpy as np


class ANN:
    def __init__(self):
        # Define an empty dictionary to store layer weights & biases.
        self.layers = {}

        # Define the number of layers in the structure.
        self.layerCount = 0

        # Define a variable to store the architecture.
        self.architecture = []

    def initialiseNetwork(self, architecture, seed=99):
        # Seed the random number generator.
        np.random.seed(seed)

        # Store the network's architecture.
        self.architecture = architecture

        # The number of layers is equal to the number of elements in the architecture array.
        self.layerCount = len(architecture)

        # For each layer definition create a set of random weights & biases and add them to the dictionary.
        for layerIndex, layerInfo in enumerate(architecture):
            currIndex = layerIndex
            inputSize = layerInfo["input_dim"]
            outputSize = layerInfo["output_dim"]

            self.layers['W' + str(currIndex)] = np.random.randn(inputSize, outputSize) * 0.1
            self.layers['B' + str(currIndex)] = np.random.randn(1, outputSize) * 0.1

        return self.layers

    def feedForward(self, networkInput):
        # Store the current activation.
        currActivation = networkInput

        # Loop though all the layers in the structure.
        for layerIndex in range(self.layerCount):
            # Store the current activation as previous activation.
            prevActivation = currActivation

            # Pull the activation function from the architecture definition.
            activationFunction = self.architecture[layerIndex]["activation"]

            # Pull the necessary weights and biases needed for forward propagation.
            currWeights = self.layers["W" + str(layerIndex)]
            currBias = self.layers["B" + str(layerIndex)]

            # Calculate the activation for the current layer.
            currActivation = feedForwardSingle(prevActivation, currWeights, currBias, activationFunction)

        return currActivation


def feedForwardSingle(prevActivation, currWeights, currBias, activation="relu"):
    # Function that performs feed-forward functionality for a single layer.
    currActivation = np.dot(prevActivation, currWeights) + currBias

    if activation is "relu":
        activationFunction = relu
    elif activation is "sigmoid":
        activationFunction = sigmoid
    else:
        raise Exception('Non-supported activation function')

    return activationFunction(currActivation)


def sigmoid(Z):
    # Defines the sigmoid activation function.
    return 1 / (1 + np.exp(-Z))


def relu(x):
    # Defines the relu activation function.
    return np.maximum(0, x)


def sigmoid_backward(dA, x):
    # Defines the derivative of the sigmoid function for back-propagation.
    sig = sigmoid(x)
    return dA * sig * (1 - sig)


def relu_backward(dA, x):
    # Defines the derivative of the relu function for back-propagation.
    dZ = np.array(dA, copy=True)
    dZ[x <= 0] = 0
    return dZ


nn_architecture = [
    {"input_dim": 12, "output_dim": 12, "activation": "sigmoid"},
    {"input_dim": 12, "output_dim": 4, "activation": "sigmoid"}
]
