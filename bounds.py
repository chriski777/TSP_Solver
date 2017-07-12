import random
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

class Bounds:
	def __init__(self, nodeDict, adjMatrix):
		self.nodeDict = nodeDict
		self.adjMatrix = adjMatrix
		self.counts = len(nodeDict)
		self.edgeDict = {}
		for i in range(self.counts):
			for j in range(i+1, self.counts):
				vertices = (i,j)
				self.edgeDict[vertices] = self.adjMatrix[i,j]
	########
	####  Held-Karp Lower Bound 
	####  	An iterative estimation provided by the book "The Traveling Salesman Problem" (Reinhalt)
	####		1. 
	def calculateHKLB(self):
		#Input Parameters
		# U our upper bound target value is selected as 2* cost of the MST
		U = self.calculateMSTUpperBound
		iterationFactor = 0.015
		maxChanges = 100
		#initialize city weights as zeros (weights for vertices or node numbers)
		nodeNumbers= np.zeros(self.counts)
		hkBound = -10000000000
		tsmall = 0.001
		alpha = 2
		beta = 0.5
		numIterations = int(round(iterationFactor* self.counts))
		newAdjMat = self.adjMatrix.copy()
		result = self.calculateOTB(self.adjMatrix)
		ourTree = result[1]
		for i in range(0, maxChanges):
			for k in range(0, numIterations):
				tempMatrix = self.calcNewMatrix(newAdjMat,nodeNumbers)
				result = self.calculateOTB(tempMatrix)
				oneTreeBound = result[0]
				oneTreeEdges = result[1]
				if oneTreeBound > hkBound:
					hkBound = oneTreeBound	
				if self.isATour(oneTreeEdges):
					break
			if self.isATour(oneTreeEdges):
				break
		return hkBound
	def calcNewMatrix(self,adjMatrix,nodeNumbers):
		temp = adjMatrix.copy()
		m = len(temp)
		#i is the index
		for i in range(0,m):
			temp[i] -= nodeNumbers[i]
			temp[:,i] -= nodeNumbers[i]
			temp[i][i] = 0
		return temp

	def isATour(self,path):
		tour = True
		return tour
	########
	####  1-tree Bound 
	####  	A form of lower bound that utilizes the 1-tree based on Chapter 7 of The Traveling Salesman Problem: A Computational Study by Cook
	####		1. Pick a random node v0.
 	####		2. Get the length of the MST after disregarding the random node. 
 	####		3. Let S be the sum of the cheapest two edges incident with the random node v0. 
 	####		4. Output the sum of 2 and 3.
 	####	The 1-Tree bound should approximately be 90.5% of the optimal cost. The best 1-Tree lower bound will be the maximum cost of the many MSTs we get.
 	########
	def calculateOTB(self,adjMatrix):
		maxOTBLB = -10000000
		bestTree = []
		for initNode in range(0,self.counts):
			#Create an AdjMatrix without the row & col containing the initNode
			newAdjMat = adjMatrix
			newAdjMat = np.delete(newAdjMat,initNode,axis= 0)
			newAdjMat = np.delete(newAdjMat,initNode,axis = 1)
			#Calculate MST length without the initNode
			mst = minimum_spanning_tree(newAdjMat)
			MSTedges = []
			Z = mst.toarray().astype(float)
			for i in range(len(Z)):
				array = np.nonzero(Z[i])[0]
				for index in array:
					x = i
					y = index
					if i >= initNode:
						x +=1
					if index >= initNode:
						y +=1 
					tuplex = (x,y)
					MSTedges.append(tuplex)
			r = 0
			# r is the length of the MST we have without the initNode
			for edge in MSTedges:
				checkEdge = edge
				if (checkEdge not in self.edgeDict):
					checkEdge = (edge[1],edge[0])
				r += self.edgeDict[checkEdge]
			# s is the sum of the cheapest two edges incident with the random node v0.
			s = 0
			edgeLengths = adjMatrix[initNode]
			nodeNums = range(0,self.counts)
			twoNN = sorted(zip(edgeLengths, nodeNums))[1:3]	
			s = twoNN[0][0] + twoNN[1][0]
			temp = r + s
			if temp > maxOTBLB:
				maxOTBLB = temp
				oneTreeEdges = MSTedges[:]
				oneTreeEdges.append((initNode,twoNN[0][1]))
				oneTreeEdges.append((initNode,twoNN[1][1]))
				bestTree = oneTreeEdges
		return [maxOTBLB, oneTreeEdges]
	def calculateMSTUpperBound(self):
		mst = minimum_spanning_tree(self.adjMatrix)
		MSTedges = []
		Z = mst.toarray().astype(float)
		for i in range(len(Z)):
			array = np.nonzero(Z[i])[0]
			for index in array:
				tuplex = (i,index)
				MSTedges.append(tuplex)
		cost = 0
		for edge in MSTedges:
			checkEdge = edge
			if (checkEdge not in self.edgeDict):
				checkEdge = (edge[1],edge[0])
			cost += self.edgeDict[checkEdge]
		return 2*cost