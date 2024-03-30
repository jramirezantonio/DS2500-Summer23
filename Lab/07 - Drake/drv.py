# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:50:40 2021
@author: rachlin
"""

import random as rnd
import matplotlib.pyplot as plt
import seaborn as sns
import copy


def E(drv):
    return drv.E()


class DRV:

    def __init__(self, dist=None):
        """ Constructor """
        if dist is None:
            self.dist = {}
        else:
            self.dist = copy.deepcopy(dist)

    def __getitem__(self, x):
        return self.dist.get(x, 0)

    def __setitem__(self, x, p):
        self.dist[x] = p

    def random(self, k=1):
        """ return a random value in accordance with the DRV probability 
        distribution """

        rslt = rnd.choices(list(self.dist.keys()), list(self.dist.values()), k=k)
        if k == 1:
            return rslt[0]
        else:
            return rslt

    def E(self):
        """ Expected value """
        ev = 0.0
        for (x, p) in self.dist.items():
            ev += x * p
        return ev

    def apply(self, other, op):
        """ Apply a binary operator to self and other """
        X = DRV()
        items = list(self.dist.items())
        oitems = list(other.dist.items())
        for x, px in items:
            for y, py in oitems:
                X[op(x, y)] += px * py
        return X

    def applyscalar(self, a, op):
        """ Apply a binary operator to self and a scalar a """
        X = DRV()
        items = list(self.dist.items())
        for (x, p) in items:
            X[op(x, a)] += p
        return X

    def __add__(self, other):
        """ Add two discrete random variables """
        return self.apply(other, lambda x, y: x + y)

    def __sub__(self, other):
        """ Subtract two discrete random variables  """
        return self.apply(other, lambda x, y: x - y)

    def __mul__(self, other):
        """ Multiply two discrete random variables  """
        return self.apply(other, lambda x, y: x * y)

    def __truediv__(self, other):
        """ Divide two discrete random variables  """
        return self.apply(other, lambda x, y: x / y)

    def __pow__(self, other):
        """ power function on two discrete random variables  """
        if type(other) == 'DRV':
            return self.apply(other, lambda x, y: x ** y)
        else:
            return self.applyscalar(other, lambda x, c: x ** c)

    def __radd__(self, a):
        """ Add a scalar, a by the DRV """
        return self.applyscalar(a, lambda x, c: c + x)

    def __rsub__(self, a):
        """ Subtract scalar - drv """
        return self.applyscalar(a, lambda x, c: c - x)

    def __rmul__(self, a):
        """ Multiply a scalar, a by the DRV """
        return self.applyscalar(a, lambda x, c: c * x)

    def __repr__(self):
        """ String representation of the DRV """

        xp = sorted(list(self.dist.items()))

        rslt = ''
        for x, p in xp:
            rslt += str(round(x)) + ' : ' + str(round(p, 8)) + '\n'
        return rslt

    def plot(self, title='', xscale='', yscale='',
             trials=10000, bins=20, show_cumulative=True):
        """ Display the DRV distribution """

        sample = self.random(k=trials)  # [self.random() for _ in range(trials)]

        # sns.displot(sample, kind='hist', stat='density', bins=bins)
        sns.displot(sample, kind='hist', stat='probability', bins=bins)

        plt.title(title)
        plt.xlabel('value')
        plt.grid()

        if xscale == 'log':
            plt.xscale(xscale)

        if yscale == 'log':
            plt.yscale(yscale)

        if show_cumulative:
            plt.yticks([0.0, 0.25, 0.50, 0.75, 1.00])
            xp = sorted(list(self.dist.items()))
            xval = [t[0] for t in xp]
            pval = [t[1] for t in xp]
            totalp = 0.0
            pcumul = []
            for p in pval:
                totalp += p
                pcumul.append(totalp)
            sns.lineplot(x=xval, y=pcumul)

        plt.show()
