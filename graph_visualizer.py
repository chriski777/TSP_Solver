import matplotlib.pyplot as plt
import networkx as nx
import Graph_TSP as Graph
import dataset_processing as D
import numpy as np
import matplotlib.pyplot as plt
import os
class graph_visualizer:
	def __init__(self,solExist):
		self.solExist = solExist
		return
	######################
	###Create Snapshots
	######################
	def snapshotMaker(self,dataGraph):
		algorithms = ["NearestNeighbor", "Greedy", "ConvHull","Christofides", "Optimal"]
		newDir = dataGraph.instanceName
		if not os.path.exists(newDir):
			os.makedirs(newDir)
		for alg in algorithms:
			newFolder = "%s/%s" % (dataGraph.instanceName, alg) 
			if not os.path.exists(newFolder):
			    os.makedirs(newFolder)
			if alg == "NearestNeighbor":
				self.snapshotHelper(dataGraph,dataGraph.nearestNeighbor(),newFolder,alg)
			if alg == "Greedy":
				self.snapshotHelper(dataGraph,dataGraph.greedy(), newFolder,alg)
			if alg == "ConvHull":
				convHullTour,visualTour = dataGraph.convexhullInsert()
				self.snapshotConvHelper(dataGraph,visualTour, newFolder,alg)
			if alg == "Christofides":
				christoFides = dataGraph.christoFides()
				self.snapshotChrisHelper(dataGraph,christoFides, newFolder,alg)
			if self.solExist:
				if alg == "Optimal":
					self.snapshotHelper(dataGraph,dataGraph.solution, newFolder,alg)

	def snapshotConvHelper(self,dataGraph,algEdges, directory,alg):
		fig = plt.figure()
		for i in range(0,len(algEdges)):
		    G = nx.Graph()
		    G.add_nodes_from(dataGraph.nodeDict.keys())
		    nx.draw_networkx_nodes(G,dataGraph.nodeDict,node_size=10,nodelist = dataGraph.nodeDict.keys(),node_color='r')
		    #For Visualization of Convex Hull Paths formed by algorithm, visualTour[i]
		    nx.draw_networkx_edges(G,dataGraph.nodeDict, edgelist = algEdges[i])
		    dtry = "%s/%s%s.png" % (directory,alg,i)
		    plt.savefig(dtry)
		    plt.clf()
		for n, p in dataGraph.nodeDict.iteritems():
		    G.node[n]['pos'] = p
		plt.close('all')

	def snapshotHelper(self,dataGraph,algEdges, directory,alg):
		fig = plt.figure()
		for i in range(0,len(algEdges)):
		    G = nx.Graph()
		    G.add_nodes_from(dataGraph.nodeDict.keys())
		    nx.draw_networkx_nodes(G,dataGraph.nodeDict,node_size=10,nodelist = dataGraph.nodeDict.keys(),node_color='r')
		    #For Visualization of Convex Hull Paths formed by algorithm, visualTour[i]
		    if i != len(algEdges)- 1:
		    	edgelist = algEdges[:i]
		    else:
		    	edgelist = algEdges
		    nx.draw_networkx_edges(G,dataGraph.nodeDict, edgelist = edgelist)
		    dtry = "%s/%s%s.png" % (directory,alg,i)
		    plt.savefig(dtry)
		    plt.clf()
		for n, p in dataGraph.nodeDict.iteritems():
		    G.node[n]['pos'] = p
		plt.close('all')

	def snapshotChrisHelper(self,dataGraph,algEdges, directory,alg):
		portion = {0:"MST", 1:"MW", 2: "Tour", 3: "Answer"}
		fig = plt.figure()
		for t in range(len(algEdges)):
			newFolder = "%s/%s" % (directory,portion[t])
			if not os.path.exists(newFolder):
			    os.makedirs(newFolder)
			for i in range(0,len(algEdges[t])):
			    G = nx.Graph()
			    G.add_nodes_from(dataGraph.nodeDict.keys())
			    nx.draw_networkx_nodes(G,dataGraph.nodeDict,node_size=10,nodelist = dataGraph.nodeDict.keys(),node_color='r')
			    #For Visualization of Convex Hull Paths formed by algorithm, visualTour[i]
			    if i != len(algEdges[t])- 1:
			    	edgelist = algEdges[t][:i]
			    else:
			    	edgelist = algEdges[t]
			    nx.draw_networkx_edges(G,dataGraph.nodeDict, edgelist = edgelist)
			    dtry = "%s/%s/%s%s.png" % (directory,portion[t],portion[t],i)
			    plt.savefig(dtry)
			    plt.clf()
			for n, p in dataGraph.nodeDict.iteritems():
			    G.node[n]['pos'] = p
			plt.close('all')

