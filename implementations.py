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
		sol_response = raw_input("Do you have a solution .txt file for your instance?(Y/N): ")
		solExist = True
		if sol_response.lower() in ['n', 'no'] :
			print("That's alright! The 1-tree LB or the HKLB can be used as reference points for comparisons across the 4 algorithms. ")
			solExist = False
		hklb_response = raw_input("Would you like the Held-Karp Lower Bound to be included? The computation for this may take awhile and will increase the waiting time.(Y/N): ")
		hklbExist = True
		if hklb_response.lower() in ['n', 'no']:
			hklbExist = False
		#Feed in a directory which has your xy coordinates and your adjacency matrices
		instance_DS = D.dataset_processing(dataDir,instanceName, solExist)
		vis_response = raw_input("Would you like visualizations for the algorithms? (Y/N): ")		
		break
	except (IOError, NameError):
		print("This is not a valid instance. Please put in a valid directory name! Please also make sure the  %s_s.txt file exists in the directory.")
	except (IndexError):
		print("Please make sure your %s_s.txt's first and last value are the same. ")
######################
###Initialization
######################
instance_graph = Graph.Graph_TSP(instance_DS.nodeDict,instance_DS.adjMatrix, instanceName, instance_DS.solution)
nodeDict = instance_graph.nodeDict

randomSol = instance_graph.randomSolution()
nearestNeighbor = instance_graph.nearestNeighbor()
greedy = instance_graph.greedy()
convHullTour, visualTour = instance_graph.convexhullInsert()
oneTreeLB= instance_graph.oneTreeBound()
christoFides = instance_graph.christofides()
upperBound = instance_graph.upperBound()

print("Cost for random Solution: " + str(instance_graph.cost(randomSol)))
print("Cost for nearestNeighbor: " + str(instance_graph.cost(nearestNeighbor)))
print("Cost for greedy: " + str(instance_graph.cost(greedy)))
print("Cost for Convex Hull Insertion : " + str(instance_graph.cost(convHullTour)))
print("Cost for Christofides : " + str(instance_graph.cost(christoFides)))
print("The one-tree Lower Bound is: " + str(oneTreeLB))
if hklbExist:
	HKLB = instance_graph.HKLowerBoundCost()
	print("The HK Lower Bound is: " + str(HKLB))
print("The Upper Bound (Calculated by 2*cost of MST) is: "  + str(upperBound))
if solExist:
	optimal = instance_DS.solution
	print("Optimal Cost : " + str(instance_graph.cost(optimal)))
if (vis_response.lower() in ['y','yes']):
	print("\nCreating your graph visualizations...")
	graph_visuals = graphVis.graph_visualizer(solExist)
	graph_visuals.snapshotMaker(instance_graph)