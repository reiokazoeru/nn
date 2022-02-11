import numpy as np
from backend import Network

#net checks if point is on f(x)=x^2

X = np.reshape([[0,0],[1,1],[-1,1],[0,1],[1,0],[2,4],[-3,9],[5,2]],(8,2,1))
Y = np.reshape([[1],[1],[1],[0],[0],[1],[1],[0]],(8,1,1))

network = Network([2,3,1])
network.genNetwork()


network.train(X,Y)

print(network.predict([[3],[9]]))
print(network.predict([[1],[0]]))
print("\n")
