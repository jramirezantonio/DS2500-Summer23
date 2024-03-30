"""
The k-means clustering algorithm
@author J. Rachlin

"""
import csv
import pandas as pd
import random as rnd
import copy
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def read_iris_data(filename):
    """ Read csv data from a file into attributes (data), and targets (classes) """
    data = []
    classes = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            data.append(tuple([float(x) for x in row[:4]]))
            classes.append(row[4])
    return data, classes

def pick_initial_centroids(data, k):
    """ Picking k random data points as initial centroids """
    return rnd.sample(data, k)

def euclidean(p1, p2):
    """ Compute euclidean distance between two points p1 and p2"""
    return sum([(x1 - x2) ** 2 for x1, x2 in zip(p1, p2)])

def closest(point, centroids, dfunc):
    """ Determine the closest centroid for ONE point
    using the specified distance function dfunc"""
    nearest = 0
    nearest_dist = dfunc(centroids[0], point)

    for c in range(1, len(centroids)):
        dist = dfunc(centroids[c], point)
        if dist < nearest_dist:
            nearest = c
            nearest_dist = dist
    return nearest

def find_closest_centroid(data, centroids, dfunc):
    """ For each data point find the closes centroid
    data - our data set
    centroids - The list of centroids
    dfunc - distance function
    return a dictionary (centroid # --> list of points)"""

    cdict = defaultdict(list)
    for point in data:
        c = closest(point, centroids, dfunc)
        cdict[c].append(point)
    return cdict

def adjust_centroids(cdict):
    adjusted = []
    for c in cdict:
        pts = cdict[c]
        df = pd.DataFrame(pts)
        centroid = list(df.mean())
        adjusted.append(centroid)
    return adjusted


def kmeans(data, k):
    """ Perform k-means clustering
     data - our attribute data (list of tuple)
     k - the # of clusters
     return - a list of k centroids (tuples) """

    # Step 1. Pick k random points to be the initial centroids
    centroids = pick_initial_centroids(data, k)

    # Step 2. Assign each point to a cluster by finding the nearest centroid
    cdict = find_closest_centroid(data, centroids, euclidean)

    # Step 3. Repeatedly adjust (move) each centroid by averaging the attribrute
    #         values of the points associated with that centroid (cluster)
    new_centroids = adjust_centroids(cdict)
    while centroids != new_centroids:
        centroids = copy.deepcopy(new_centroids)
        cdict = find_closest_centroid(data, centroids, euclidean)
        new_centroids = adjust_centroids(cdict)

    # Step 4. Once centroids have converged to a fixed location , return them
    return centroids

def visualize(data, centroids):
    df = pd.DataFrame(data)
    df['cluster'] = [closest(point, centroids, euclidean) for point in data]
    sns.pairplot(df, hue='cluster', palette='tab10')
    plt.show()

def wcss(data, kmin=1, kmax=10):
    wvals = []
    for k in range(kmin, kmax + 1):
        centroids = kmeans(data, k)


def main():
    # Read the data - split out the raw data from the target categories/classes
    data, classes = read_iris_data('iris.dat')
    # print(data)

    # Cluster the data (specifying the number of clusters (k) )
    centroids = kmeans(data, k=5)

    # Visualize the clusters to validate the result
    visualize(data, centroids)

    # iris = pd.read_csv('iris.dat')
    # sns.pairplot(iris, hue='species')
    # plt.show()


if __name__ == "__main__":
    main()