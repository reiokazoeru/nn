from xml.etree.ElementTree import ParseError
from steputils import p21
from backend import Dense,Tanh,Train,mse,mse_prime,predict
import numpy as np


def p21ToNumList(FNAME):
    # Read an existing file from file system:
    try:
        file = open(FNAME,'r')
        input_string = file.read()
        stepfile = p21.loads(input_string.replace('\n',''))
    except IOError as e:
        print(str(e))
    except ParseError as e:
        # Invalid STEP-file
        print(str(e))
    else:
        # print(f'File {FNAME} is a valid STEP-file')
        chadList = []
        for i in input_string:
            chadList.append(ord(i))
        # print(chadList)
        # vStr = ''
        # for j in chadList:
        #     vStr+=chr(j)
        # print(vStr)
        return chadList

FNAME = "scripts\\mancor flame head 3dp rebuild 3.333 v6.step"

print(len(p21ToNumList(FNAME)))

# TODO : Make stl loader that takes list of paths and returns list of list of char vals in int form
# find longest one
# make all others that long with 0s in those spots
# give to system
# also tie outputs to all files MANUALLY
# run a shit ton of times and pray
# maybe round end result?


X = np.reshape([[0,0],[0,0],[1,0],[1,1]],(4,2,1))
Y = np.reshape([[0],[1],[1],[0]],(4,1,1))

network = [
    Dense(2,3),
    Tanh(),
    Dense(3,1),
    Tanh()
]

Train(network,mse,mse_prime,X,Y,epochs=10000,learning_rate=0.1)

print(predict(network,[[1.2],[1.2]]))
print(predict(network,[[1],[0]]))