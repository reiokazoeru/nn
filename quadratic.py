import inspect
import numpy as np
from backend import Dense,Tanh,Train,mse,mse_prime,predict


X = np.reshape([[0,0],[1,1],[-1,1],[0,1],[1,0],[2,4],[-3,9],[5,2]],(8,2,1))
Y = np.reshape([[1],[1],[1],[0],[0],[1],[1],[0]],(8,1,1))

network = [
    Dense(2,3),
    Tanh(),
    Dense(3,1),
    Tanh()
]

Train(network,mse,mse_prime,X,Y,epochs=1000,learning_rate=0.1)

print(predict(network,[[3],[9]]))
print(predict(network,[[1],[0]]))
print("\n")
