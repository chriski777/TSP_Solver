class Graph_TSP:
	#Nodes should be a dictionary of key value pairing : node num to xy coordinates
	#Edges are implied in the adjacency matrix 
	#Adjacency matrix will be n x n; where n is the number of nodes
	def __init__(self, nodes, adjacency_matrix):
		self.nodes = nodes
		self.adjacency_matrix = adjacency_matrix
	
