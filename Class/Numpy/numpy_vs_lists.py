


import numpy as np
import time
import sys


def list_version(length):
    tstart = time.time()

    # allocating lists
    X = list(range(length))
    Y = list(range(length))
    Z = []

    for i in range(len(X)):
        Z.append(X[i] + Y[i])
    tend = time.time()
    runtime = tend - tstart
    print('USING LISTS     :')
    print("Length of list  : ", len(Z))
    print("Size of the list: ", sys.getsizeof(Z))
    print("Runtime         : ", runtime)
    return runtime

def numpy_version(length):
    tstart = time.time()

    # allocating np arrays
    X = np.arange(length, dtype = np.int64)
    Y = np.arange(length, dtype = np.int64)
    Z = X + Y
    tend = time.time()
    runtime = tend - tstart
    print('USING NUMPY     :')
    print("Length of array : ", len(Z))
    print("Size of array   : ", sys.getsizeof(Z))
    print("Runtime         : ", runtime)
    return runtime
def main():
    length = 10000000
    list_runtime = list_version(length)
    numpy_runtime = numpy_version(length)

    #print(list_runtime, numpy_runtime)
    print(f"Numpy is {round(list_runtime/numpy_runtime, 2)} times faster.")

if __name__ == "__main__":
    main()