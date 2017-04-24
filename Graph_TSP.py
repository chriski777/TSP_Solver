import random
import operator
import numpy as np
import disjoint_sets as DS
class Graph_TSP:
	#Nodes should be a dictionary of key value pairing : node num to xy coordinates
	#Edges are implied in the adjacency matrix 
	#Adjacency matrix will be n x n; where n is the number of nodes
	def __init__(self, nodeDict, adjMatrix):
		self.nodeDict = nodeDict
		self.adjMatrix = adjMatrix
		self.counts = len(nodeDict)
		self.edgeDict = {}
		for i in range(self.counts):
		    for j in range(i+1, self.counts):
		    	vertices = (i,j)
		    	self.edgeDict[vertices] = self.adjMatrix[i,j]
	def randomSolution(self):
		unvisitedNodes = range(0,self.counts)
		random.shuffle(unvisitedNodes)
		return unvisitedNodes
	########
	#### NearestNeighbor
	#### 	Initialize visitedNodes to ensure no cycle is created 
	####	unvisitedNodes: list of unvisited nodes
	####	1. Pick a random node, then proceed to get that node's neighbors.
	####	2. Within that node's neighbors, select the minimum edge weight. 
	####	3. Based on the minimum edge weight, find the index of that weight in the original matrix.
	####  	4. If that index is NOT in the visitedNodes, remove it from the unvistedNodes list and add it 
	####	   to the visitedNodes.
	####	5. Else, remove the minIndex from the edges array and start over from step 2.
	####	6. Once you remove all the elements of unvisitedNode, terminate and return the sequence of 
	####	   vertices you will follow. 
	########
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
		edgePath = []
		for i in range(0,self.counts):
			if i < self.counts - 1:
				edgePath.append((visitedNodes[i],visitedNodes[i+1]))
			else:
				edgePath.append((visitedNodes[i],visitedNodes[0]))
		return edgePath
	########
	#### Greedy Search
	#### 	1. Sort the edges by weight values.
	####	2. Select the least-valued edge.
	####	3. Make sure it does not form a cycle if added. I do this by checking if both vertices are in
	####	   visitedNodes. This is accomplished with a small helper function isCycle. 
	####	4. Check also if the two nodes have less than degree 2. 
	####    5. If both constraints apply, add 1 to each degree and also change visitedNodes. Make sure to 
	####	   remove the edge that we added. 
	####    6. Start from the next least-value again and check each to make sure no cycle is formed and all degrees
	####       are less than 2. 
	########
	def greedy(self):
		allNodes = []
		edgePath = []
		for node in range(0,self.counts):
			allNodes.append(DS.disjoint_set(node))
		sorted_edges = sorted(self.edgeDict.items(), key=operator.itemgetter(1))
		degreeDict = {element: 0 for element in allNodes}
		numEdges = 0
		startNode = allNodes[sorted_edges[0][0][0]]
		while numEdges < self.counts - 1:
			for edge in sorted_edges:
				vertices = edge[0]
				ds1 = allNodes[vertices[0]]
				ds2 = allNodes[vertices[1]]
				if not(self.isCycle(ds1,ds2)) and self.nodeLessTwo(ds1,ds2,degreeDict):
					ds1.joinSets(ds2)
					degreeDict[ds1] += 1
					degreeDict[ds2] += 1
					numEdges += 1
					edgePath.append(vertices)
		lastTwo = [allNodes.index(x) for x in degreeDict.keys() if degreeDict[x] == 1]
		print degreeDict.values()
		edgePath.append((lastTwo[0],lastTwo[1]))
 		return edgePath
 	def isCycle(self,ds1,ds2):
 		return ds1.find() == ds2.find()
	def nodeLessTwo(self, d1, d2, degreeDict):
		return (degreeDict[d1] < 2) and (degreeDict[d2] < 2)
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
