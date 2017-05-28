import networkx as nx
import Graph_TSP as Graph
import dataset_processing as D
import numpy as np
import matplotlib.pyplot as plt
import os
import adjMatrix as adj
import graph_visualizer as graphVis
#Data directory names
dataDir = "datasetTSP"

while (True):
	try:
		instanceName = raw_input("\nEnter the TSP directory you would like to approximate: ")
		adjMat_response = raw_input("Do you have an adjacency matrix .txt file for your instance?(Y/N):")
		if adjMat_response.lower() in ['n','no'] :
			print ("Calculating your adjacency matrix...")
			adj.createAdjMatrixFile(instanceName)
			print ("Done! Your adjMatrix has been created.")
		#Feed in a directory which has your xy coordinates and your adjacency matrices
		instance_DS = D.dataset_processing(dataDir,instanceName)
		vis_response = raw_input("Would you like visualizations for the algorithms? (Y/N): ")		
		break
	except (IOError, NameError):
		print("This is not a valid instance. Please put in a valid directory name!")
	except (IndexError):
		print("Please make sure your %s_s.txt's first and last value are the same.")
######################
###Initialization
######################
instance_graph = Graph.Graph_TSP(instance_DS.nodeDict,instance_DS.adjMatrix, instanceName)

optimal = instance_DS.solution
nearestNeighbor = instance_graph.nearestNeighbor()
nodeDict = instance_graph.nodeDict
greedy = instance_graph.greedy()
convHullTour, visualTour = instance_graph.convexhullInsert()
christoFides = instance_graph.christoFides()
print("Cost for nearestNeighbor: " + str(instance_graph.cost(nearestNeighbor)))
print("Cost for greedy: " + str(instance_graph.cost(greedy)))
print("Cost for Convex Hull Insertion : " + str(instance_graph.cost(convHullTour)))
print("Cost for Christofides : " + str(instance_graph.cost(christoFides)))
print("Optimal Cost : " + str(instance_graph.cost(optimal)))

if (vis_response.lower() in ['y','yes']):
	print("\nCreating your graph visualizations...")
	graph_visuals = graphVis.graph_visualizer()
	graph_visuals.snapshotMaker(instance_graph)