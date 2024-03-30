from drv import DRV, E

def main():

    burger = DRV({250: 0.25, 500: 0.25, 750: 0.25, 1000: 0.25})
    fries = DRV({200: 0.10, 500: 0.30, 1000: 0.40, 5000: 0.20})
    coke = DRV({100: 0.05, 1000: 0.80, 2000: 0.15})
    profit = 0.25 * burger + 0.50 * fries + 1.0 * coke
    expenses = DRV({2500: 0.2, 2000: 0.30, 1800: 0.5})

    net = profit - expenses
    annual_net = .365 * net  # profit per year $000

    print("Expected Annual Net: ", E(annual_net))
    annual_net.plot()


if __name__ == "__main__":
    main()