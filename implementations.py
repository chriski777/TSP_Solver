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

nearestNeighbor = att48_graph.nearestNeighbor()
nodeDict = att48_graph.nodeDict
greedy = att48_graph.greedy()
convHullTour, visualTour = att48_graph.convexhullInsert()
print("Cost for nearestNeighbor: " + str(att48_graph.cost(nearestNeighbor)))
print("Cost for greedy: " + str(att48_graph.cost(greedy)))
print("Cost for Convex Hull Insertion : " + str(att48_graph.cost(convHullTour)))

######################
###Create Snapshots
######################

#For ConvHull Algorithm
for i in range(0,len(visualTour)):
    fig = plt.figure()
    G = nx.Graph()
    G.add_nodes_from(nodeDict.keys())
    nx.draw_networkx_nodes(G,nodeDict,node_size=10,nodelist = nodeDict.keys(),node_color='r')
    #For Visualization of 
    nx.draw_networkx_edges(G,nodeDict, edgelist = visualTour[i])
    plt.savefig("%s%s.png" % ("ConvHullTour",i))
for n, p in nodeDict.iteritems():
    G.node[n]['pos'] = p
plt.close('all')
