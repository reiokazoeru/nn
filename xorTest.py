from tkinter.tix import Tree
from backend import Dense,Tanh,Train,mse,mse_prime,predict,Network

import matplotlib as plt
import numpy as np

X = np.reshape([[0,0],[0,0],[1,0],[1,1]],(4,2,1))
Y = np.reshape([[0],[1],[1],[0]],(4,1,1))

network = Network([2,3,1])
network.genNetwork()

network.train(X,Y)

print(network.predict([[1.2],[1.2]]))

print(network.predict([[1],[0]]))