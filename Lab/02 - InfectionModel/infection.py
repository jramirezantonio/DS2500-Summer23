"""
    infection.py: A simple grid-model for simulating the spread of
    an infectious disease.

    Josue Antonio
    5/16/2023
"""

import numpy as np
import matplotlib.pyplot as plt

def initialize_model(M, N, K):
    """ Create an MxN array of zeros. The first row contains some
    values set to 1 according to the probability parameter K (0.0...1.0)
    M = The # of days to simulate
    N - The # of students
    K - Probability that a value in the first row (i=0) is set to 1
    return - An initialized MxN numpy array
    """
    A = np.zeros((M, N), dtype = int)
    for i in range(N):
        if np.random.rand() < K:
            A[0,i] = 1
    return A

def run_model(arr, R):
    """ Rows 1 to N-1 are computed. Disease is transmitted to
    each of your neighbors with probability R.  (The next day
    they show up to class sick).  If a student is sitting next to
    two healthy students, they will be healthy the next day as well.
    Sick students become well the next day no matter what.
    arr - The array
    R - The infection transmission probability. (Only neighbors are at risk)
    return - None.  Array modified in place. """

    cols, rows = arr.shape
    for i in range(1, rows):
        for j in range(cols):
            # if student sick on previous day then student healthy on the next day
            if arr[i-1,j] == 1:
                arr[i,j] = 0
            # if student is sitting next to 2 healthy students, then the student is healthy on the next day
            elif (j > 0 and arr[i-1,j-1] == 0) and (j < (cols - 1) and arr[i-1,j+1] == 0):
                arr[i,j] = 0
            else:
                if np.random.rand() < R:
                    arr[i,j] = 1

def display_model(arr):
    """
    Display data in our grid model
    arr - A 2D array
    return - None. Image saved to file
    """
    number_days = str(arr.shape[0]) + " days"
    plt.imshow(arr, cmap = 'cividis')
    plt.title("Spread of Infection over " + number_days)
    plt.xlabel("Number of Students")
    plt.ylabel("Number of Days")
    plt.savefig('img.png', dpi = 500)
    plt.show()

def main():
    # Define key parameters (N, M, R, K)
    M = 1000
    N = 1000
    R = 0.8
    K = 0.2

    # Initialize the model
    arr = initialize_model(M, N, K)

    # Run the model
    run_model(arr, R)

    # Display the result
    #display_model(arr)
    X = []
    print(list(arr))
    #for i in range(len(arr)):
    #    X.append(arr[i][0])


if __name__ == "__main__":
    main()


