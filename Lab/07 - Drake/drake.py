from drv import DRV, E

def main():

    # Drake's equation random variables
    R = DRV({1.5: 1/3, 2.5: 1/3, 3: 1/3})
    f_p = DRV({0.85: 1/4, 0.9: 1/4, 0.95: 1/4, 1: 1/4})
    n_e = DRV({1: 1/5, 2: 1/5, 3: 1/5, 4: 1/5, 5: 1/5})
    f_1 = DRV({0.01: 1/10, 0.02: 1/10, 0.03: 1/10, 0.04: 1/10, 0.05: 1/10, 0.06: 1/10,
               0.07: 1/10, 0.08: 1/10, 0.09: 1/10, 0.1: 1/10})
    f_i = DRV({0.01: 1/10, 0.02: 1/10, 0.03: 1/10, 0.04: 1/10, 0.05: 1/10, 0.06: 1/10,
               0.07: 1/10, 0.08: 1/10, 0.09: 1/10, 0.1: 1/10})
    f_c = DRV({0.01: 1/10, 0.02: 1/10, 0.03: 1/10, 0.04: 1/10, 0.05: 1/10, 0.06: 1/10,
               0.07: 1/10, 0.08: 1/10, 0.09: 1/10, 0.1: 1/10})
    L = DRV({1000: 0.4, 10000: 0.3, 100000: 0.2, 1000000: 0.05, 10000000: 0.05})

    # Drake's equation estimate
    N = R * f_p * n_e * f_1 * f_i * f_c * L
    # print(E(N))

    # Plot estimate
    N.plot('How Many Advanced Civilizations in our Galaxy?', yscale='log', trials=100000, show_cumulative=False)

    """ The expected number of advanced civilizations in the Milky Way Galaxy is 617.711276874998"""


if __name__ == '__main__':
    main()