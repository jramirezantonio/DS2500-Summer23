'''
    Josue Antonio
    DS 2500
    Lab 1
    5/11 - Summer 1 2023
    sunspots.py
'''
import csv
import matplotlib.pyplot as plt

SNDATA = 'SN_m_tot_V2.0.csv'

def read_csv(filename):
    ''' Fn: read_csv
        Param: filename string
        Returns: list
        Does: reads every line of csv file storing them in 2d list
    '''
    data = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter = ";")
        for row in reader:
            data.append(row)
    return data

def plot_sunspots(sunspot_means):
    ''' Fn: plot_sunspots
        Param: sunspot_means list
        Returns: nothing
        Does: creates line plot of number of sunspots over time
    '''
    positions = [i for i in range(len(sunspot_means))]
    plt.figure(figsize=(18, 8), dpi = 200)    
    plt.plot(positions, sunspot_means, color = "darkorange")
    plt.grid()
    plt.title("Number of Sunspots Over Time")
    plt.ylabel("Monthly mean total sunspot number")
    plt.xlabel("Years")
    ticks_data = [i for i in range(1749, 2022, 10)]
    tick_positions = [i for i in range(0, len(sunspot_means), 117)]
    plt.xticks(tick_positions, ticks_data, rotation = 60)

def main():
    # Gather data - read in sunspots file
    data = read_csv(SNDATA)
    
    # Computation - crete sunspot means list to plot
    sunspot_means = []
    for i in range(len(data)):
        sunspot_means.append(float(data[i][3]))
    
    #Communication - create line plot of mean sunspots over time
    plot_sunspots(sunspot_means)
    
'''
  derived estimate of the length of the sunspot cycle:
  number of peaks ~25, number of years ~3272/12 ~ 273
  hence, length of cycle ~ 273/25 = 10.92 ~ 11 years
'''
  
    
    
    
main()