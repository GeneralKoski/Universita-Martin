import sys

import random

import numpy as np

import pandas as pd

import data_loader

def relu(x):
    return np.maximum(0, x)

def relu_prime(x):
    return np.where(x > 0, 1, 0)

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_prime(x):
    s = sigmoid(x)
    return ( 1 - s ) * s

class Network(object):

    def __init__(self, sizes, eta):
        
        self.sizes = sizes # numero neuroni strato per strato
        
        self.eta = eta

        # numero di layer
        self.num_layers = len(sizes) - 2

        # bias
        self.biases = [ np.random.randn(n, 1) for n in sizes[1:] ]
        # self.biases = []
        # for n in sizes[1:]:
        #     self.biases.append( np.random.randn(n, 1) )

        # weights
        self.weights = [ 
            np.random.randn(a, b) 
            for a, b in zip(sizes[:-1], sizes[1:]) 
        ]

        self.activation_functions = [ 
            sigmoid for _ in range(self.num_layers + 1) 
        ]
        self.activation_functions[-1] = sigmoid
        # self.activation_functions[-1] = relu

        self.activation_functions_prime = [ 
            sigmoid_prime for _ in range(self.num_layers + 1) 
        ]
        self.activation_functions_prime[-1] = sigmoid_prime


    def forward(self, x): # x è l'input della rete (784, 1)

        a = [x] # activations
        s = [0] # pre_activations 

        i = 0
        for W, b in zip(self.weights, self.biases):
            # W * x + b
            s.append(
                np.dot( np.transpose(W), a[-1] ) + b
                # 784 x n, 784 x 1
                # n x 784, 784, 1 --> n x 1
            )
            # sigma(W * x + b)
            a.append( sigmoid(s[-1]) )
            # a.append( self.activation_functions[i](s[-1]) )
            i += 1
        
        # return a[-1]
        return a, s

    def backward(self, a, s, y): 
        # attivazioni (y dalla rete), pre_attivazioni, y del dataset
        
        delta = [ np.zeros((n, 1)) for n in self.sizes[1:] ] # lista di vettori di errore delta

        # strato di output: ( sigma(s) - y ) * sigma'(s)
        delta[-1] = (a[-1] - y) * \
            self.activation_functions_prime[-1](s[-1])

        for l in range(self.num_layers - 1, -1, -1):

            # n x 10 matrice di pesi
            # delta 10 x 1
            # ---> vettore n x 1
            delta[l] = np.dot( 
                self.weights[l + 1], delta[l + 1] 
                ) * self.activation_functions_prime[l + 1](s[l + 1])

            print(delta.shape)

        return delta

    def step(self, activations, deltas):
        
        # 784 x n, n x n_2, n_2 x 10
        gradient_W = [ np.zeros(w.shape) for w in self.weights ]
        gradient_b = [ np.zeros(b.shape) for b in self.biases ]

        num_input = len(activations)

        for l in range(self.num_layers, -1, -1): # backprop

            sum_w = 0
            for k in range(num_input):
                sum_w += np.dot( 
                    activations[k][l], np.transpose( deltas[k][l] ) 
                )
                # attivazione penultimo strato
                # attivazione n_2 x 1
                # delta (errore) strato di output
                # delta 10 x 1
                # --> gradiente di W:  n_2 x 10

            sum_b = 0
            for k in range(num_input):
                sum_b += deltas[k][l]

            gradient_W[l] = sum_w
            gradient_b[l] = sum_b

        # Discesa del gradiente:
        self.weights = [
            w - (self.eta / num_input) * dw
            for w, dw in zip( self.weights, gradient_W )
        ]
        #  W - (eta * dw) / n_input

        self.biases = [
            b - (self.eta / num_input) * db
            for b, db in zip( self.biases, gradient_b )
        ]


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
        
        n = len(training_data)

        for i in range(n_epochs):

            random.shuffle(training_data)

            mini_batches = [ training_data[k : k + mini_batch_size] 
                            for k in range(0, n, mini_batch_size) ]
            
            # for x, y in training_data:

            for mini_batch in mini_batches:

                activations = []
                deltas = []

                for x, y in mini_batch:

                    a, s = self.forward(x) # passo in avanti

                    delta = self.backward(a, s, y) # errori all'indietro

                    activations.append(a)
                    deltas.append(delta)

                self.step(activations, deltas) # discesa gradiente

            count = self.test(test_data)

            print("Epoch", str(i), ":", str(count), "/", str(len(test_data)), "(", str(count / (len(test_data)) * 100), "% )")


def load_xor_4bit_data():

    df = pd.read_csv('data.csv')

    training_data = df.to_numpy()[:]
    training_inputs = [np.reshape(x, (8, 1)) for x in training_data[:, :-4]]
    training_results = [np.reshape(y, (4, 1)) for y in training_data[:, -4:]]

    training_data = list(zip(training_inputs, training_results))

    test_data = df.to_numpy()[:]
    test_inputs = [np.reshape(x, (8, 1)) for x in test_data[:, :-4]]
    test_results = [np.reshape(y, (4, 1)) for y in test_data[:, -4:]]

    test_data = list(zip(test_inputs, test_results))

    return training_data, test_data


def load_xor_8bit_data():

    df = pd.read_csv('data2.csv')

    training_data = df.to_numpy()[:]
    training_inputs = [np.reshape(x, (16, 1)) for x in training_data[:, :-8]]
    training_results = [np.reshape(y, (8, 1)) for y in training_data[:, -8:]]

    training_data = list(zip(training_inputs, training_results))

    test_data = df.to_numpy()[:]
    test_inputs = [np.reshape(x, (16, 1)) for x in test_data[:, :-8]]
    test_results = [np.reshape(y, (8, 1)) for y in test_data[:, -8:]]

    test_data = list(zip(test_inputs, test_results))

    return training_data, test_data


def main(ARGS):

    try:
        mode = ARGS[0]
    except:
        mode = "mnist"

    if mode == "xor4":
        training_data, test_data = load_xor_4bit_data()


    elif mode == "xor8":
        training_data, test_data = load_xor_8bit_data()

    else:
        training_data, _, test_data = data_loader.load_data_wrapper()

    nn = Network([28*28, 256, 10], 0.01)

    nn.train(training_data, test_data, 10, 64)

    return 0

if __name__ == "__main__":

    ARGS = sys.argv[1:]

    RETCODE = main(ARGS)

    sys.exit(RETCODE)