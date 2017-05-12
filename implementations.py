import networkx as nx
import Graph_TSP as Graph
import dataset_processing as D
import numpy as np
import matplotlib.pyplot as plt
import os
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

optimal = att48_DS.solution
nearestNeighbor = att48_graph.nearestNeighbor()
nodeDict = att48_graph.nodeDict
greedy = att48_graph.greedy()
convHullTour, visualTour = att48_graph.convexhullInsert()
christoFides = att48_graph.christoFides()
print("Cost for nearestNeighbor: " + str(att48_graph.cost(nearestNeighbor)))
print("Cost for greedy: " + str(att48_graph.cost(greedy)))
print("Cost for Convex Hull Insertion : " + str(att48_graph.cost(convHullTour)))
print("Cost for Christofides : " + str(att48_graph.cost(christoFides)))
print("Optimal Cost : " + str(att48_graph.cost(optimal)))

######################
###Create Snapshots
######################
'''
newFolder = "ConvHullPics"
if not os.path.exists(newFolder):
    os.makedirs(newFolder)
for i in range(0,len(visualTour)):
    fig = plt.figure()
    G = nx.Graph()
    G.add_nodes_from(nodeDict.keys())
    nx.draw_networkx_nodes(G,nodeDict,node_size=10,nodelist = nodeDict.keys(),node_color='r')
    #For Visualization of Convex Hull Paths formed by algorithm
    nx.draw_networkx_edges(G,nodeDict, edgelist = visualTour[i])
    plt.savefig("%s/%s/%s%s.png" % (att48,newFolder,"ConvHullTour",i))
for n, p in nodeDict.iteritems():
    G.node[n]['pos'] = p
plt.close('all')
'''