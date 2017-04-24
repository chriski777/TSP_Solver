import plotly 
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx
import Graph_TSP as Graph
import dataset_processing as D
import numpy as np
import matplotlib.pyplot as plt
plotly.tools.set_credentials_file(username='chriski777', api_key='PE1PC0QMswvn4XZSZMHg')

#Data directory names
dataDir = "datasetTSP"
att48 = "att48"

######################
###Data Processing
######################
#Feed in a directory which has your xy coordinates and your adjacency matrices
att48_DS = D.dataset_processing(dataDir,att48)

######################
###Initialization
######################
att48_graph = Graph.Graph_TSP(att48_DS.nodeDict,att48_DS.adjMatrix)

x = att48_graph.nearestNeighbor()
b = att48_graph.nodeDict
y = att48_graph.greedy()

print("Cost for nearestNeighbor: " + str(att48_graph.cost(x)))
print("Cost for greedy: " + str(att48_graph.cost(y)))
'''
######################
###Create Snapshots
######################
for i in range(0,49):
    fig = plt.figure()
    G = nx.Graph()
    G.add_nodes_from(b.keys())
    nx.draw_networkx_nodes(G,b,node_size=10,nodelist = b.keys(),node_color='r')
    nx.draw_networkx_edges(G,b, edgelist = y[0:i])
    plt.savefig("%s.png" % i)

for n, p in b.iteritems():
    G.node[n]['pos'] = p
'''
