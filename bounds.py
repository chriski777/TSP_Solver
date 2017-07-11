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
	####  	An iterative estimation provided by the book "The Traveling Salesman" (Reinhalt)
	####		1. 
	def calculateHKLB(self):
		#Start with first node
		currNode = 0
		#initialize city weights as zeros
		subgraph_HK = 0
		pi_vector = np.zeros(self.counts)
		#initialize 20 nearest neighbors to currNode
		nodeNums = range(0,self.counts )
		edgeLengths = self.adjMatrix[currNode]
		twentyNN = sorted(zip(edgeLengths, nodeNums))[1:21]
		return 5
	########
	####  1-tree Bound 
	####  	A form of lower bound that utilizes the 1-tree based on Chapter 7 of The Traveling Salesman Problem: A Computational Study by Cook
	####		1. Pick a random node v0.
 	####		2. Get the length of the MST after disregarding the random node. 
 	####		3. Let S be the sum of the cheapest two edges incident with the random node v0. 
 	####		4. Output the sum of 2 and 3.
 	####	The 1-Tree bound should approximately be 90.5% of the optimal cost. The best 1-Tree lower bound will be the maximum cost of the many MSTs we get.
 	########
	def calculateOTB(self):
		maxOTBLB = -10000000
		for initNode in range(0,self.counts):
			#Create an AdjMatrix without the row & col containing the initNode
			newAdjMat = self.adjMatrix.copy()
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
			edgeLengths = self.adjMatrix[initNode]
			nodeNums = range(0,self.counts)
			twoNN = sorted(zip(edgeLengths, nodeNums))[1:3]		
			s = twoNN[0][0] + twoNN[1][0]
			temp = r + s
			if temp > maxOTBLB:
				maxOTBLB = temp
		return maxOTBLB