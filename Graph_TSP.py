import random
import operator
import numpy as np
import disjoint_sets as DS
from scipy.spatial import ConvexHull
from scipy.sparse.csgraph import minimum_spanning_tree
import networkx.algorithms as naa
import networkx as nx
import bounds
class Graph_TSP:
	#Nodes should be a dictionary of key value pairing : node num to xy coordinates
	#Edges are implied in the adjacency matrix 
	#Adjacency matrix will be n x n; where n is the number of nodes
	def __init__(self, nodeDict, adjMatrix,instanceName, solution):
		self.nodeDict = nodeDict
		self.adjMatrix = adjMatrix
		self.counts = len(nodeDict)
		self.edgeDict = {}
		self.instanceName = instanceName
		self.solution = solution
		for i in range(self.counts):
			for j in range(i+1, self.counts):
				vertices = (i,j)
				self.edgeDict[vertices] = self.adjMatrix[i,j]
		self.Bounds = bounds.Bounds(self.nodeDict, self.adjMatrix)
	def HKLowerBoundCost(self):
		return self.Bounds.calculateHKLB()
	def oneTreeBound(self):
		return self.Bounds.calculateOTB(self.adjMatrix)[0]
	def upperBound(self):
		return self.Bounds.calculateMSTUpperBound()
	#Random solution formed by shuffling nodes 
	#Meant to provide bad solutions
	def randomSolution(self):
		unvisitedNodes = range(0,self.counts)
		random.shuffle(unvisitedNodes)
		edgePath = []
		for i in range(0,len(unvisitedNodes)):
			if i < self.counts - 1:
				edgePath.append((unvisitedNodes[i],unvisitedNodes[i+1]))
			else:
				edgePath.append((unvisitedNodes[i],unvisitedNodes[0]))
		return self.listConverter(edgePath)
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
		edgePath = []
		unvisitedNodes = range(0,self.counts)
		random.shuffle(unvisitedNodes)
		node = unvisitedNodes.pop()
		visitedNodes.append(node)
		while unvisitedNodes:
			edges = np.copy(self.adjMatrix[node])
			chosen = []
			while not chosen:
				if len(edges) != 0:
					minVal = np.min(edges)
					minIndex = np.where(self.adjMatrix[node] == minVal)[0][0]
				if len(edges) == 0:
					edges = np.array([self.adjMatrix[node][x] for x in unvisitedNodes])
					minVal = np.min(edges)
					minIndex = -1
					for x in unvisitedNodes:
						if minVal == self.adjMatrix[node][x]:
							minIndex = x
				if minIndex not in visitedNodes:
					chosen.append(minIndex)
					node = minIndex
					unvisitedNodes.remove(minIndex)
					visitedNodes.append(minIndex)
				else:
					minEdgeIndex = np.where(edges == minVal)[0][0]
					edges = np.delete(edges,minEdgeIndex)
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
		edgePath.append((lastTwo[0],lastTwo[1]))
		return edgePath
	def isCycle(self,ds1,ds2):
		return ds1.find() == ds2.find()
	def nodeLessTwo(self, d1, d2, degreeDict):
		return (degreeDict[d1] < 2) and (degreeDict[d2] < 2)
	########
	#### Convex Hull Insertion
	####	1. Form a convex hull of our current graph. This forms our initial cycle.
	####	2. For each node not in our current convex hull, find an edge e_ij = {n_i, n_j} in our current convex hull such that w_i,r + w_r,j - w_i,j
	####	is minimal and keep track of this minimal triplet. 
	####	3. For all triplets, find the minimal triplet (n_i', n_j',n_r') such that (w_i,r' + w_r,j')/ w_i,j' is minimal.
	####	4. Insert n_r' between n_i' and n_j' by adding the edges e_r,i & e_r,j while removing edge e_i,j
	####	5. Repeat step 2-4 until all nodes have been added to our cycle. 
	########
	def convexhullInsert(self):
		#Initial Subtour composed of Convex Hull
		allPoints = np.array(self.nodeDict.values())
		convHull = ConvexHull(allPoints)
		listofHullEdges = convHull.simplices.tolist()
		listofHullIndices = convHull.vertices.tolist()
		allTours = [listofHullEdges]
		unvisitedNodes = [z for z in self.nodeDict.keys() if z not in listofHullIndices]
		visitedNodes = listofHullIndices[:]
		listOfCurrentEdges = listofHullEdges[:]
		while unvisitedNodes:
			triplets = []
			listOfCurrentEdges = listOfCurrentEdges[:]
			#Go through each node not in the current Cycle
			for node in unvisitedNodes:
				neighborVals = self.adjMatrix[node]
				minVal = 1000000000000
				triplet = (-10,-10,-10)
				#Find the minimal triplet for each node that adheres to the minimal w_ir + w_jr - w_ij
				for edge in listOfCurrentEdges:
					nodeI = edge[0]
					nodeJ = edge[1]
					cost = neighborVals[nodeI] + neighborVals[nodeJ] - self.adjMatrix[nodeI][nodeJ]
					if cost < minVal:
						minVal = cost
						triplet = (nodeI,nodeJ,node)
				triplets.append(triplet)
			#From all these triplets, find the most optimal one based on the ratio!
			minRatio = 1000000000000
			chosenTrip = (-10,-10,-10)
			for triple in triplets:
				ratio = (self.adjMatrix[triple[0]][triple[2]] + self.adjMatrix[triple[1]][triple[2]])/ self.adjMatrix[triple[0]][triple[1]]
				if minRatio > ratio:
					minRatio = ratio
					chosenTrip = triple
			#Insert node_r between node_i and node_j
			node_i = chosenTrip[0]
			node_j = chosenTrip[1]
			node_r = chosenTrip[2]
			currEdge = [x for x in listOfCurrentEdges if all([node_i in x,node_j in x])][0]
			listOfCurrentEdges.append([node_i,node_r])
			listOfCurrentEdges.append([node_j,node_r])
			listOfCurrentEdges.remove(currEdge)
			unvisitedNodes.remove(node_r)
			visitedNodes.append(node_r)
			#Alltours is for visualization Purposes
			allTours.append(listOfCurrentEdges)
		return self.listConverter(listOfCurrentEdges), allTours
	########
	#### Christofides Algorithm
	####	1. Form minimum spanning tree T of G. 
	####	2. Generate an Minimum perfect matching of the vertices in the MST that have odd degrees.
	####	3. Form an Eulerian path on the multigraph formed by the union (keep duplicates) of the MST and minimum weight perfect matching.
	####	4. Perform shortcutting and skip repeated vertices in the Eulerian path to get a Hamiltonian circuit.
	########
	def christoFides(self):
		#Create a minimum spanning Tree of Graph G
		Tcsr = minimum_spanning_tree(self.adjMatrix)
		MSTedges = []
		degreeDict = dict(zip(self.nodeDict.keys(),[0]*len(self.nodeDict.keys())))
		Z = Tcsr.toarray().astype(float)
		for i in range(len(Z)):
		    array = np.nonzero(Z[i])[0]
		    for index in array:
		        if index.size != 0:
		            degreeDict[i] += 1
		            degreeDict[index] +=1
		            tuplex = (i,index)
		            MSTedges.append(tuplex)
		#STEP 2: Isolate the vertices of the MST with odd degree
		OddVerts = [x for x in degreeDict.keys() if degreeDict[x] %2 != 0]
		#STEP 3: Only Consider the values in OddVerts and form a min-weight perfect matching
		H = nx.Graph()
		H.add_nodes_from(self.nodeDict.keys())
		for i in range(len(OddVerts)):
		    for j in range(len(OddVerts)):
		        if i != j:
		            H.add_edge(OddVerts[i],OddVerts[j],weight = -self.adjMatrix[OddVerts[i]][OddVerts[j]])
		edgeMWDict = naa.max_weight_matching(H, maxcardinality = True)
		minWeight = [(key,edgeMWDict[key]) for key in edgeMWDict.keys()]
		uniqueMW = []
		#Prune out redundant Tuples
		for edge in minWeight:
		    if edge not in uniqueMW and (edge[1],edge[0]) not in uniqueMW:
		        uniqueMW.append(edge)
		unionMW_MST = MSTedges[:]
		for tup in uniqueMW:
		    #Only add first index since both edges are returned for instance: (0,1) & (1,0) are returned
		    unionMW_MST.append(tup)
		    degreeDict[tup[0]] +=1
		    degreeDict[tup[1]] +=1
		#Retrieve the Eulerian Circuit
		eulerianCircuit = self.eulerianTour(unionMW_MST,self.nodeDict)
		shortCut = []
		unvisitedPath = []
		totalPath = [i for sub in eulerianCircuit for i in sub]
		for node in totalPath:
		    if node not in unvisitedPath:
		        shortCut.append(node)
		        unvisitedPath.append(node)
		return [MSTedges,minWeight, eulerianCircuit,self.pathEdges(shortCut)]
	#Make sure to connect the first and last vertex to get a hamiltonian cycle!
	def pathEdges(self,visitedNodes):
		solution = []
		for i in range(0,len(visitedNodes)):
		    if i < len(visitedNodes) - 1:
		        solution.append((visitedNodes[i],visitedNodes[i+1]))
		    else:
		        solution.append((visitedNodes[i],visitedNodes[0]))
		return solution
	def eulerianTour(self,setOfEdges,vertDict):
	    tempGraph = nx.MultiGraph()
	    tempGraph.add_nodes_from(vertDict.keys())
	    tempGraph.add_edges_from(setOfEdges)
	    return list(nx.eulerian_circuit(tempGraph))
	def cost(self,path):
		counter = 0
		for edge in path:
			checkEdge = edge
			if (checkEdge not in self.edgeDict):
				checkEdge = (edge[1],edge[0])
			counter += self.edgeDict[checkEdge]
		return counter
	def listConverter(self, edgeList):
		tupleSol = []
		for listElem in edgeList:
			tupleSol.append((listElem[0],listElem[1]))
		return tupleSol
