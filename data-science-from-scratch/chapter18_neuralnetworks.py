from chapter04_linearalgebra import dot
import math
import matplotlib.pyplot as plt
import random


################
#              #
#  PERCEPTRON  #
#              #
################

def step_function(x):
    return 1 if x >= 0 else 0

def perceptron_output(weights, bias, x):
    """returns 1 if the perceptron 'fires'' 0 if not"""
    calculation = dot(weights, x) + bias
    return step_function(calculation)

##################
#                #
#  FEED FORWARD  #
#                #
##################

def sigmoid(t):
    return 1 / (1 + math.exp(-t))

def neuron_output(weights, inputs):
    return sigmoid(dot(weights, inputs))

def feed_forward(neural_network, input_vector):
    """takes in a neural network represented as a list of lists
    of weights and returns the output from forward-propagating the input"""

    outputs = []

    # process one layer at a time

    for layer in neural_network:
        input_with_bias = input_vector + [1]                    # add a bias input
        output = [neuron_output(neuron, input_with_bias)        # compute the output
                  for neuron in layer]                          # for each neuron
        outputs.append(output)                                  # and remember it

        # then the input to the next layer is the output of this one
        input_vector = output
    return outputs


#####################
#                   #
#  BACKPROPAGATION  #
#                   #
#####################

def backpropagate(network, input_vector, targets):

    hidden_outputs, outputs = feed_forward(network, input_vector)

    # the output * (1 - output) is from the derivative sigmoid
    output_deltas = [output * (1 - output) * (output - target)
                     for output, target in zip(outputs, targets)]

    # adjust weights for output layer, one neuron at a time
    for i, output_neuron in enumerate(network[-1]):
        # focus on the ith output layer neuron
        for j, hidden_output in enumerate(hidden_outputs + [1]):
            # adjust the jth weight based on both
            # this neuron's delta and its jth input
            output_neuron[j] -= output_deltas[i] * hidden_output

    # back-propagate errors to hidden layer
    hidden_deltas = [hidden_output * (1 - hidden_output) *
                      dot(output_deltas, [n[i] for n in network[-1]])
                     for i, hidden_output in enumerate(hidden_outputs)]

    # adjust weights for hidden layer, one neuron at a time
    for i, hidden_neuron in enumerate(network[0]):
        for j, input in enumerate(input_vector + [1]):
            hidden_neuron[j] -= hidden_deltas[i] * input


raw_digits = [
          """11111
             1...1
             1...1
             1...1
             11111""",

          """..1..
             ..1..
             ..1..
             ..1..
             ..1..""",

          """11111
             ....1
             11111
             1....
             11111""",

          """11111
             ....1
             11111
             ....1
             11111""",

          """1...1
             1...1
             11111
             ....1
             ....1""",

          """11111
             1....
             11111
             ....1
             11111""",

          """11111
             1....
             11111
             1...1
             11111""",

          """11111
             ....1
             ....1
             ....1
             ....1""",

          """11111
             1...1
             11111
             1...1
             11111""",

          """11111
             1...1
             11111
             ....1
             11111"""]

random.seed(0)          # to get repeatable results
input_size = 25         # each input is a vector of length 25
num_hidden = 5          # we'll have 5 neurons in each hidden layer
output_size = 10        # we need 10 outputs for each input

#each hidden neuron has one weight per input, plus a bias weight
hidden_layer = [[random.random() for _ in range(input_size + 1)] for _ in range(num_hidden)]

# each output neuron has one weight per input, plus a bias weight
output_layer = [[random.random() for _ in range(num_hidden + 1)] for _ in range(output_size)]


# the network starts out with random weights
network = [hidden_layer, output_layer]


def make_digit(raw_digit):
    return [1 if c == '1' else 0
            for row in raw_digit.split("\n")
            for c in row.strip()]


inputs = list(map(make_digit, raw_digits))

targets = [[1 if i == j else 0 for i in range(10)]
           for j in range(10)]

for i in range(10000):
    print("iteration", i)
    for input_vector, target_vector in zip(inputs, targets):
        backpropagate(network, input_vector, target_vector)

def predict(input):
    return feed_forward(network, input)[-1]

number_7 = predict(inputs[7])
position_7 = number_7.index(max(number_7))
print(position_7, [round(p,4) for p in number_7])


number_3 = predict([0,1,1,1,0,    # .@@@.
                   0,0,0,1,1,    # ...@@
                   0,0,1,1,0,    # ..@@.
                   0,0,0,1,1,    # ...@@
                   0,1,1,1,0])   # .@@@.

position_3 = number_3.index(max(number_3))
print(position_3, [round(p,4) for p in number_3])

number_1 = predict([0,0,1,0,0,
                    0,0,1,0,0,
                    0,0,1,0,0,
                    0,0,1,0,0,
                    0,0,1,0,0])

position_1 = number_1.index(max(number_1))
print(position_1, [round(p,4) for p in number_1])