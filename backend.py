import numpy as np

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
        tanh = lambda x: np.tanh(x)
        tanh_prime = lambda x: 1-np.tanh(x) **2
        super().__init__(tanh,tanh_prime)
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
def Save(network): #save trained network
    savinL = [None for i in range(network)]
    for i,layer in enumerate(network):
        if type(layer) is Dense:
            savinL[i] = {"enum":i,"type":Dense,"weights":layer.weights,"bias":layer.bias}
        elif type(layer) is Tanh:
            savinL[i] = {"enum":i,"type":Tanh}
    return {"network":network,"values":savinL}
