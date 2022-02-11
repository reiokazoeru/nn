import pickle
import matplotlib as plt
import numpy as np
import json
from time import time
from backend import Dense,Tanh,jsonLoader,LoadNet,SaveNet

"""
Concept - Give NN values that occur in different heads to receive a bunch of numbers back

TO-DO
2. Run low epoch test
3. maybe make rounding function

DONE 
1. Make Load that takes json path and loads data into training in put and output variables

"""

fName = 'headData.json'

X,Y,inLen,outLen = jsonLoader(fName)
# print(X)
network = [
    Dense(inLen,inLen+1),
    Tanh(),
    Dense(inLen+1,outLen-1),
    Tanh(),
    Dense(outLen-1,outLen),
    Tanh()
]


# LoadNet()
# Train(network,mse,mse_prime,X,Y,epochs=10000,learning_rate=1)
# save network

