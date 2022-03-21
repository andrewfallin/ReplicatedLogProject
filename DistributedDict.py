import jsonpickle
import json
import numpy as np
from datetime import datetime
DATETIMEFORMAT = "%H:%M:%S"
import Event as e

class DistributedDict:

    def __init__(self, nodeNum):
        self.nodeNumber = nodeNum
        self.currentEventNum = 0
        self.DD = {}
        self.partialLog = []
        self.timeMatrix = [[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]

    def insertIntoDict(self, sysEvent):
        event = sysEvent.event
        self.updateTimeMatrix()
        if not self.partialLog.__contains__(event):
            self.partialLog.append(sysEvent)
        if not self.HasKey(event.eventID, self.DD):
            self.DD[event.eventID] = event

    # need to update to a system event
    def deleteFromDict(self, sysEvent):
        event = sysEvent.event
        self.updateTimeMatrix()
        if not self.partialLog.__contains__(sysEvent):
            self.partialLog.append(sysEvent)
        if self.HasKey(event.eventID, self.DD):
            del(self.DD[event.eventID])



    # using uuid to log events
    # going to need to check both logs to see if there is a conflict
    def HasKey(self, findKey, dictionary):
        if findKey in dictionary:
            return True
        return False

    def updateTimeMatrix(self):
        self.currentEventNum = self.currentEventNum + 1
        self.timeMatrix[self.nodeNumber][self.nodeNumber] = self.currentEventNum

    def mergeTimeMatrices(self, matrix):
        for i in range(len(matrix)):
            for j in range(4):
                self.timeMatrix[i][j] = max(self.timeMatrix[i][j], matrix[i][j])

    def mergeTheLogs(self, newLog):
        for sysEvent2 in newLog:
            containsEvent = False
            event2 = sysEvent2.event
            for sysEvent1 in self.partialLog:
                event1 = sysEvent1.event
                if event1.eventID == event2.eventID:
                    containsEvent = True
            if not containsEvent:
                self.partialLog.append(sysEvent2)

    def receiveFromNode(self, message):
        #message[4]: DD
        #message[5]: partialLog
        #message[6]: time matrix
        newSysEvent = jsonpickle.decode(message[1])
        senderPL = jsonpickle.decode(message[5])
        newEvents = self.getNewEvents(senderPL)
        self.addNewEventstoDict(newEvents)
        self.mergeTheLogs(newEvents)


    def addNewEventstoDict(self, newEvents):
        for sysEvent in newEvents:
            event = sysEvent.event
            if sysEvent.eventType == 'delete':
                self.deleteFromDict(sysEvent)
            else:
                if not self.HasKey(event.eventID, self.DD):
                    self.DD[event.eventID] = sysEvent


    def getNewEvents(self, partialLog):
        newEvents = []
        for sysevent in partialLog:
            inLocalPL = False
            event1 = sysevent.event
            for sysevent2 in self.partialLog:

                event2 = sysevent2.event
                if event1.eventID == event2.eventID:
                    inLocalPL = True
            if not inLocalPL:
                newEvents.append(sysevent)

        return newEvents