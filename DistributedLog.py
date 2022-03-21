
import numpy as np
from datetime import datetime
DATETIMEFORMAT = "%H:%M:%S"

class DistributedLog:

    def __init__(self, nodeNumber):
        self.nodeNumber = nodeNumber
        self.currentEventNumber = 0
        self.distributedLog = []
        self.timeMatrix = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

    def logInternalEvent(self, event):
        if not self.distributedLog.__contains__(event):
            self.currentEventNumber = self.currentEventNumber + 1
            self.updateTimeMatrix(self.currentEventNumber, self.nodeNumber)
            self.distributedLog.append(event)

    def logExternalEvent(self, event):
        if not self.distributedLog.__contains__(event):
            self.distributedLog.append(event)

    def updateTimeMatrix(self, currentEventNumber, nodeNumber):
        self.timeMatrix[nodeNumber][nodeNumber] = currentEventNumber

    def mergeTimeMatrices(self, matrix):
        for i in range(len(matrix)):
            for j in range(4):
                self.timeMatrix[i][j] = max(self.timeMatrix[i][j], matrix[i][j])
                #if matrix[i][j] != 0 and self.timeMatrix[i][j] != 0:
                #    x = datetime.strptime(matrix[i][j], DATETIMEFORMAT)
                  #  y = datetime.strptime(self.timeMatrix[i][j], DATETIMEFORMAT)
                 #   if x >= y:
                  #      self.timeMatrix[i][j] = x.strftime(DATETIMEFORMAT)
                #elif matrix[i][j] != 0 and self.timeMatrix[i][j] == 0:
                   # self.timeMatrix[i][j] = matrix[i][j]

