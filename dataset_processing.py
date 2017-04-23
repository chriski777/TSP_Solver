import numpy as np
class dataset_processing:
	def __init__(self, folder, dsName):
		self.dataDir = "%s/%s" % (folder, dsName)
		self.dsName = dsName
		self.adjMatrix = np.loadtxt("%s/%s_d.txt" %(self.dataDir, self.dsName))
		self.nodeDict = {}
		counter = 0
		for node in np.loadtxt("%s/%s_xy.txt" %(self.dataDir, self.dsName)):
			self.nodeDict[counter] = node
			counter += 1
