from backend import Dense,Tanh,Train,mse,mse_prime,predict

import matplotlib as plt
import numpy as np

X = np.reshape([[0,0],[0,0],[1,0],[1,1]],(4,2,1))
Y = np.reshape([[0],[1],[1],[0]],(4,1,1))

network = [
    Dense(2,3),
    Tanh(),
    Dense(3,1),
    Tanh()
]

Train(network,mse,mse_prime,X,Y,epochs=100000,learning_rate=0.1)

print(predict(network,[[1.2],[1.2]]))
print(predict(network,[[1],[0]]))
