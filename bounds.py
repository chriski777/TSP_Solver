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
 	########
	def calculateOTB(self):
		initNode = random.randint(0,self.counts)
		#Create an AdjMatrix without the row & col containing the initNode
		newAdjMat = self.adjMatrix.copy()
		np.delete(newAdjMat,initNode,axis= 0)
		np.delete(newAdjMat,initNode,axis = 1)
		#Calculate MST length without the initNode
		return 32