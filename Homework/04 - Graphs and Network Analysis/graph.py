"""
Josue Antonio
06/12/2023
graph.py: Weighted and unweighted graphs
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

GAD = 'gad_data.csv'

class Graph:
    """Graph class, for an undirected, unweighted graph with an adjacency list representation
        For an edge A-B, it appears in the adjacency list as A-B and B-A
    """

    def __init__(self, V=[], E=[]):
        """ Create a new graph from a list of vertices V and edges E.
        By default, the graph is undirected and unweighted """
        self.G = {}  # Node label -> {Set of adjacent nodes}
        for v in V:
            self.add_vertex(v)
        for (x, y) in E:
            self.add_edge(x, y)
            
    def add_vertex(self, v):
        """ Add a vertex (with no connected edges) to the graph"""
        self.G[v] = set()
        
    def add_edge(self, u, v):
        # add vertices in case they don't already exist
        if u not in self.G:
            self.add_vertex(u)
        if v not in self.G:
            self.add_vertex(v)
        self.G[u].add(v)
        self.G[v].add(u)

    def remove_edge(self, u, v):
        """ Remove an edge from the graph  """
        self.G[u].remove(v)
        self.G[v].remove(u)

    def __getitem__(self, v):
        """ Return all vertices adjacent to v (overriding index operator!)"""
        if v in self.G:
            return self.G[v]
        else:
            return set()

    def __repr__(self):
        """ Print the graph """
        graph_str = ''
        for v in self.G:
            graph_str += '['+v+'] => ' + str(self.G[v]) + '\n'
        return graph_str

    def is_adjacent(self, u, v):
        """ Test if u and v are adjacent """
        if v in self.G[u] and u in self.G[v]:
            return True
        else:
            return False

    def get_vertices(self):
        """ Get a list of all vertices in the graph """
        return list(self.G.keys())

    def get_edges(self):
        """ Return a list of edges in the graph.  Each edge is a tuple (u,v) """
        edges = []
        for v, e in self.G.items():
            for u in e:
                edges.append((v, u))
        return edges

    def num_vertices(self):
        """ Return the number of vertices in the graph """
        return len(self.G)

    def num_edges(self):
        """ Return the number of edges in the undirected graph """
        # iterate over all edge sets # use get_edges # (a,b) and (b,a) counts as the same edge
        edges = self.get_edges()

        # edges are double counted in get_edges
        return int(len(edges) / 2)

    def deg(self, v):
        """ What is the degree of vertex v?  i.e., how many
        other vertices are adjacent """
        return len(self.G[v])

    def degree_distribution(self):
        """ Compute the degree distribution of the graph
        Return a dictionary (key=degree, value=# vertices of that degree. """
        degrees = [self.deg(v) for v in self.get_vertices()]
        counts = Counter(degrees)

        # Sorted by keys thanks to: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
        myKeys = list(counts.keys())
        myKeys.sort()
        sorted_dict = {i: counts[i] for i in myKeys}
        return sorted_dict

    def toDF(self, columns=['u', 'v']):
        """ Convert the graph to a pandas dataframe representation """
        df = pd.DataFrame(columns=columns)
        for edge in self.get_edges():
            df = df.append({columns[0]: edge[0], columns[1]: edge[1]}, ignore_index=True)
        return df

    def fromDF(self, df, columns=['u', 'v']):
        """ Convert from a pandas dataframe with two columns
        identifying the vertices.  Each row is an edge. """
        for i in range(len(df)):
            self.add_edge(df.loc[i, columns[0]], df.loc[i, columns[1]])

    def visualize(self, fig=1, directed=False):
        """ Render the graph using networkx library: conda install networkx """
        df = self.toDF()

        options = {
            "font_size": 15,
            "node_size": 800,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 1,
            "width": 1,
        }

        graph_type = nx.Graph()

        G = nx.from_pandas_edgelist(df, df.columns[0], df.columns[1], create_using=graph_type)
        pos = nx.circular_layout(G)
        # pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx(G, pos, with_labels=True, **options)
        plt.show()

class WeightedGraph(Graph):
    """
    A weighted graph is a graph with weights attached to each edge
    Many of the methods on a weighted graph can be inherited from Graph
    without modification!
    """
    def __init__(self, V=[], WE=[]):
        super().__init__(V)
        for (x, y, w) in WE:
            self.add_weighted_edge(x, y, w)

    def add_weighted_edge(self, u, v, w):
        # add vertices in case they don't already exist
        if u not in self.G:
            self.add_vertex(u)
        if v not in self.G:
            self.add_vertex(v)
        self.G[u].add((v, w))
        self.G[v].add((u, w))

    def get_weighted_edges(self):
        """ Return a list of edges in the graph.  Each edge is a tuple (u, v, w) """
        edges = []
        for v, e in self.G.items():
            for t in e:
                edges.append((v, t))
        return edges

    def subgraph(self, V):
        subgraph = WeightedGraph()
        for v in V:
            edges = self.G[v]
            for edge in edges:
                if edge in V:
                    subgraph.add_edge(v, edge)
        return subgraph

    def asthma_visualize(self, V=[], fig=1, directed=False):
        """ Modification of the visualize method to enable bipartite layout plotting """
        df = self.toDF()

        options = {
            "font_size": 10,
            "node_size": 250,
            "node_color": "white",
            "edgecolors": "black",
            "linewidths": 1,
            "width": 1,
        }

        graph_type = nx.Graph()

        G = nx.from_pandas_edgelist(df, df.columns[0], df.columns[1], create_using=graph_type)
        pos = nx.bipartite_layout(G, V)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx(G, pos, with_labels=True, **options)
        plt.show()

def read_gad_data(filename, columns=['gene', 'disease', 'num_positive']):
    """ Read gene, disease, and num_positive columns from gad data (ignore records with num_positive = 0)"""
    df = pd.read_csv(filename)
    df = df[columns]
    df = df[df.num_positive != 0]
    return df

def main():

    # Read data - store gad data
    df = read_gad_data(GAD)

    # Instantiate weighted graph from gad data
    gad_g = WeightedGraph()
    gad_g.fromDF(df, columns=['gene', 'disease'])

    # Computation/Visualization - compute degree distribution of gad graph nodes
    # Plot distribution using a log scale for both axes
    degrees = gad_g.degree_distribution()
    plt.scatter(degrees.keys(), degrees.values(), marker='.')
    plt.title('Degree Distribution (log scale)')
    plt.xlabel("Degree")
    plt.ylabel("Number of Vertices")
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    # Is the gene-disease association network scale free?
    # not quite since the plot is not a straight line

    # Find nodes linked to asthma
    asthma_genes = gad_g['asthma']

    # Compute diseases linked to each gene connected to asthma
    diseases = set()
    for gene in asthma_genes:
        for disease in gad_g[gene]:
            diseases.add(disease)
    V = asthma_genes.union(diseases)

    # Create and visualize graph associated with the asthma-linked genes and the respective linked diseases
    subgraph = gad_g.subgraph(V)
    subgraph.asthma_visualize(V=asthma_genes)
    # Can you identify what other diseases are strongly connected to genes linked to asthma?
    # Diabetes type 1, rheumatoid arthritis , hiv, and tuberculosis seem to have 4 genes linked
    # to asthma


if __name__ == '__main__':
    main()

"""
Undirected Graph
|V|: 8
|E|: 10
Adjacent to A: {'B', 'G', 'H', 'C'}
[A] => {'B', 'G', 'H', 'C'}
[B] => {'F', 'C', 'A'}
[C] => {'D', 'B', 'A'}
[D] => {'E', 'C'}
[E] => {'D', 'F'}
[F] => {'B', 'H', 'E'}
[G] => {'A'}
[H] => {'F', 'A'}


Undirected Graph
|V|: 8
|E|: 10
Adjacent to A: {('C', 3), ('B', 5), ('G', 2), ('H', 9)}
[A] => {('C', 3), ('B', 5), ('G', 2), ('H', 9)}
[B] => {('A', 5), ('C', 0), ('F', 3)}
[C] => {('A', 3), ('D', 1), ('B', 0)}
[D] => {('E', 12), ('C', 1)}
[E] => {('F', 16), ('D', 12)}
[F] => {('E', 16), ('H', 8), ('B', 3)}
[G] => {('A', 2)}
[H] => {('A', 9), ('F', 8)}
"""
