"""
A discrete random variable object (DRV)
Josue Antonio
DS2500

"""

import random as rnd
import copy
import seaborn as sns
import matplotlib.pyplot as plt

def E(X):
    return X.E()

class DRV:

    def __init__(self, dist=None):
        """ Constructor """
        if dist is None:
            self.dist = {}
        else:
            self.dist = copy.deepcopy(dist)

    def random(self, k=1):
        """ Generate a random outcome according to the probability distribution """
        outcomes = list(self.dist.keys())
        probs = list(self.dist.values())
        result = rnd.choices(outcomes, probs, k=k)
        if k == 1:
            return result[0]
        else:
            return result

    def E(self):
        return sum([x * p for (x, p) in self.dist.items()])

    def __getitem__(self, x):
        """ Enables Z[X] ==> probability that Z = X  """
        return self.dist.get(x, 0) # access prob. from x key and if it doesn't exist then prob. is 0.0

    def __setitem__(self, x, p):
        """ Enables Z[X] = p --> setting a values """
        self.dist[x] = p

    def apply(self, other, op):
        """ Apply a binary operator (+, -, *, ...) to self and other
         across every possible pair of outcomes """
        X = DRV()
        items = list(self.dist.items())
        oitems = list(other.dist.items())
        for x, px in items:
            for y, py in oitems:
                X[op(x, y)] += px * py
        return X

    def applyscalar(self, a, op):
        """ Apply a binary operator (+, *, ...) to self and to the number a """
        X = DRV()
        items = list(self.dist.items())
        for x, p in items:
            X[op(x, a)] += p
        return X

    def __add__(self, other):
        """ Add two DRVs: X + Y """
        return self.apply(other, lambda x, y: x + y)

    def __sub__(self, other):
        """ Subtract two DRVs: X - Y """
        return self.apply(other, lambda x, y: x - y)

    def __mul__(self, other):
        """ Multiply two DRVs: X * Y """
        return self.apply(other, lambda x, y: x * y)

    def __truediv__(self, other):
        """ Divide two DRVs: X / Y """
        return self.apply(other, lambda x, y: x / y)

    def __radd__(self, a):
        """ Add a to a DRV, e.g., Y = a + X """
        return self.applyscalar(a, lambda x, c: c + x)

    def __rsub__(self, a):
        """ Subtract a to a DRV, e.g., Y = a - X """
        return self.applyscalar(a, lambda x, c: c - x)

    def __rmul__(self, a):
        """ Multiply a to a DRV, e.g., Y = a * X """
        return self.applyscalar(a, lambda x, c: c * x)

    def __rtruediv__(self, a):
        """ Divide a to a DRV, e.g., Y = a / X """
        return self.applyscalar(a, lambda x, c: c / x)

    def plot(self):
        sample = self.random(k=10000)
        sns.displot(sample, kind='hist', stat='density')
        plt.show()

    def __repr__(self):
        """ Returns the DRV as a printable string """
        xp = sorted(list(self.dist.items()))
        result = ''
        for x, p in xp:
            result += str(x) + ' : ' + str(round(p, 8)) + '\n'
        return result


def main():
    D6 = DRV({1: 1/6, 2: 1/6, 3: 1/6, 4: 1/6, 5: 1/6, 6: 1/6})
    print(E(D6))

    print(D6.random(k=10))

    # roll = D6 + D6
    # print(roll)
    # roll.plot()

    score = 10 + D6
    print(score)
    score.plot()


if __name__ == "__main__":
    main()
