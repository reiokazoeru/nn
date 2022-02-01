import json
from pydoc import describe
import numpy as np
from time import time
import pickle

class Layer:
    def __init__(self) -> None:
        self.input = None
        self.output = None
    def forward(self,input):
        # TODO: Return out
        pass
    def backward(self,output_gradient, learning_rate):
        # TODO: update parameters and return input gradient
        pass
class Dense(Layer):
    def __init__(self,input_size,output_size) -> None:
        self.weights = np.random.randn(output_size,input_size)
        self.bias = np.random.randn(output_size,1)
    def forward(self, input):
        self.input = input
        return np.dot(self.weights,self.input)+self.bias
    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        self.weights -= learning_rate*weights_gradient
        self.bias -= learning_rate * output_gradient
        return np.dot(self.weights.T,output_gradient)
class Activation(Layer):
    def __init__(self,activation,activation_prime) -> None:
        self.activation = activation
        self.activation_prime = activation_prime
    def forward(self, input):
        self.input = input
        return self.activation(self.input)
    def backward(self, output_gradient, learning_rate):
        return np.multiply(output_gradient,self.activation_prime(self.input))
class Tanh(Activation):
    def __init__(self) -> None:
        def tanh(x):
            return np.tanh(x)
        def tanh_prime(x):
            return 1-np.tanh(x) **2
        super().__init__(tanh,tanh_prime)
class Network():
    def __init__(self,netList) -> None: 
        """
        netlist format:
        [in values,dense layer n width,out values]
        """
        self.netList = netList
    def genNetwork(self):
        nL = self.netList
        net = []
        for i,j in enumerate(nL):
            net.append(Dense(j,nL[i+1]))
            net.append(Tanh())
        self.net = net
    def loadNetwork(self,fName):
        with open(fName,'rb') as inp:
            net = pickle.load(inp)
    def saveNetwork(self,cFName):
        if cFName == None:
            with open(str(round(time()))+'network.obj','wb') as outp:
                pickle.dump(self.net,outp,pickle.HIGHEST_PROTOCOL)
        else:
            with open(cFName+'.obj','wb') as outp:
                pickle.dump(self.net,outp,pickle.HIGHEST_PROTOCOL)

        

def mse(y_true,y_pred):
    return np.mean(np.power(y_pred-y_true,2))
def mse_prime(y_true,y_pred):
    return 2 * (y_pred-y_true) / np.size(y_true)
def predict(network, input):
    output = input
    for layer in network:
        output = layer.forward(output)
    return output
def Train(network, loss, loss_prime, x_train, y_train, epochs = 1000, learning_rate = 0.01, verbose = True):
    for e in range(epochs):
        error = 0
        for x, y in zip(x_train, y_train):
            # forward
            output = predict(network, x)

            # error
            error += loss(y, output)

            # backward
            grad = loss_prime(y, output)
            for layer in reversed(network):
                grad = layer.backward(grad, learning_rate)

        error /= len(x_train)
        if verbose:
            print(f"{e + 1}/{epochs}, error={error}")
def SaveNet(network): #save trained network
    denseNet = []
    for i,layer in enumerate(network):
        if i%2 != 0:
            denseNet.append(layer)
    network = denseNet
    with open(str(round(time()))+'network.obj','w') as outp:
        pickle.dump(network,outp,pickle.HIGHEST_PROTOCOL)    
    print('Saved Network as '+str(round(time()))+'network.obj')
def LoadNet(fPath):
    return json.load(open(fPath))
def jsonLoader(fName):
    jsonFile = open(fName)
    rawList = json.load(jsonFile)

    xList = []
    yList = []

    for head in rawList:
        tempList = []
        for data in head["in"]:
            tempList.append(head["in"][data])
        xList.append(tempList)
        tempList = []
        for data in head["out"]:
            tempList.append(head["out"][data])
        yList.append(tempList)
    inLen = len(xList[0])
    outLen = len(yList[0])
    X = np.reshape(xList,(len(xList),inLen,1))
    Y = np.reshape(yList,(len(yList),outLen,1))
    return X,Y,inLen,outLen