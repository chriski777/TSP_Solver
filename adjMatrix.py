import numpy as np
import pandas as pd

def createAdjMatrixFile(fileName):
    dirName = "datasetTSP/%s/%s_xy.txt" % (fileName, fileName)
    data = pd.read_csv(dirName,header = None,  delimiter=r"\s+").as_matrix()
    newMatrix = np.zeros((len(data),len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            newMatrix[i][j] = np.linalg.norm(data[i]- data[j])
    saveDir = "datasetTSP/%s/%s_d.txt" % (fileName, fileName)
    np.savetxt(saveDir, newMatrix, delimiter=' ')