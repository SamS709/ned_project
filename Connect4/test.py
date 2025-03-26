from Camera import *

A = np.array([[0,0]])

A = np.concatenate((A,np.array([[1,2]])))

A = np.concatenate((A,np.array([[5,6]])))

for pos in A:
    print(pos)

