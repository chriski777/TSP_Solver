import random
import numpy as np
class Graph_TSP:
	#Nodes should be a dictionary of key value pairing : node num to xy coordinates
	#Edges are implied in the adjacency matrix 
	#Adjacency matrix will be n x n; where n is the number of nodes
	def __init__(self, nodeDict, adjMatrix):
		self.nodeDict = nodeDict
		self.adjMatrix = adjMatrix
		self.counts = len(nodeDict)
	def randomSolution(self):
		unvisitedNodes = range(0,self.counts)
		random.shuffle(unvisitedNodes)
		return unvisitedNodes
	def nearestNeighbor(self):
		visitedNodes = []
		unvisitedNodes = range(0,self.counts)
		random.shuffle(unvisitedNodes)
		node = unvisitedNodes.pop()
		visitedNodes.append(node)
		while unvisitedNodes:
		    edges = np.copy(self.adjMatrix[node])
		    chosen = []
		    while not chosen:
		        minVal = np.min(edges)
		        minIndex = np.where(self.adjMatrix[node] == minVal)[0][0]
		        if minIndex not in visitedNodes:
		            chosen.append(minIndex)
		            node = minIndex
		            unvisitedNodes.remove(minIndex)
		            visitedNodes.append(minIndex)
		        else:
		            minEdgeIndex = np.where(edges == minVal)[0][0]
		            edges = np.delete(edges,minEdgeIndex)
		return visitedNodes
	#Consider same edge lengths
	def greedy(self):
		uniqueEdges = []
		for i in range(self.counts):
		    for j in range(i+1, self.counts):
		        uniqueEdges.append(self.adjMatrix[i,j])		
		return 1
	def convexhullInsert(self):
		return 1
	def HKLowerBoundCost(self):
		return 1
	def christoFides(self):
		return 1
	#Make sure to connect the first and last vertex to get a hamiltonian cycle!
	def pathEdges(self,visitedNodes):
		return list()
	def cost(self,path):
		return 1
