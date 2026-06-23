import sys

import random

import numpy as np

import pandas as pd

import data_loader

def relu(x):
    pass

def relu_prime(x):
    pass

def sigmoid(x):
    pass

def sigmoid_prime(x):
    pass

class Network(object):

    def __init__(self, sizes, eta):
        pass

    def forward(self, x):
        pass

    def backward(self, a, s, y):
        pass

    def step(self, activations, deltas):        
        pass


    def test(self, test_data):
        
        count = 0

        for x, y in test_data:
            
            a, _ = self.forward(x)

            output = a[-1]

            if output.shape == y.shape:
                if (np.round(output) == y).all():
                    count += 1
            else:
                if np.argmax(output) == y:
                    count += 1

        return count


    def train(self, training_data, test_data, n_epochs, mini_batch_size):
        pass



def main(ARGS):

    try:
        mode = ARGS[0]
    except:
        mode = "mnist"

    if mode == "xor4":
        training_data, test_data = data_loader.load_xor_4bit_data()

    elif mode == "xor8":
        training_data, test_data = data_loader.load_xor_8bit_data()

    else:
        training_data, _, test_data = data_loader.load_data_wrapper()

    # train network

    return 0

if __name__ == "__main__":

    ARGS = sys.argv[1:]

    RETCODE = main(ARGS)

    sys.exit(RETCODE)