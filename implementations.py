import plotly 
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx
import Graph_TSP as G
import dataset_processing as D
import numpy as np
plotly.tools.set_credentials_file(username='chriski777', api_key='PE1PC0QMswvn4XZSZMHg')

#Data directory names
dataDir = "datasetTSP"
att48 = "att48"

######################
###Data Processing
######################
#Feed in a directory which has your xy coordinates and your adjacency matrices
att48_DS = D.dataset_processing(dataDir,att48)

######################
###Initialization
######################
att48_graph = G.Graph_TSP(att48_DS.nodeDict,att48_DS.adjMatrix)



