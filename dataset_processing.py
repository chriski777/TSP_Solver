import numpy as np
#######################
####Data Processing####
#######################
class dataset_processing:
	def __init__(self, folder, dsName, solExist):
		self.dataDir = "%s/%s" % (folder, dsName)
		self.dsName = dsName
		self.adjMatrix = np.loadtxt("%s/%s_d.txt" %(self.dataDir, self.dsName))
		self.nodeDict = {}
		if solExist:
			self.solution = self.converter(np.loadtxt("%s/%s_s.txt" %(self.dataDir, self.dsName)))
		else:
			self.solution = -1
		counter = 0
		for node in np.loadtxt("%s/%s_xy.txt" %(self.dataDir, self.dsName)):
			self.nodeDict[counter] = node
			counter += 1
	def converter(self,pathlist):
		converted = []
		numNodes = len(self.adjMatrix)
		for i in range(numNodes):
			tupAdd = (int(pathlist[i]) - 1,int(pathlist[i+1]) -1)
			converted.append(tupAdd)
		return converted