import socket
from threading import Thread
import mainHandler as mh
import numpy as np
import DistributedLog as DL
import Event as e
import json
import Parser as p
from collections import namedtuple
import uuid
import jsonpickle
import SystemEvent as se
import DistributedDict as DD
import myCalendar

'''
Array of all timeslot
s, each node has an init matrix at t = 0 where all timeslots are available for everyone
If a node creates an event, we insert the event details in that timeslot.
'''

DELIMITER = '$'
def create_event(msg_send):
    return msg_send != 'conflict'


def view_calendar():
    pass


class Node:
    def __init__(self, name, prio, ip, id, port, nodes):
        self.host = ip  # Server local private ip
        self.port = port
        self.id = id
        self.name = name
        self.priority = prio
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))
        self.log = []
        self.dl = DL.DistributedLog(id)
        self.dd = DD.DistributedDict(id)
        self.node1Cal = myCalendar.myCalendar()
        self.node2Cal = myCalendar.myCalendar()
        self.node3Cal = myCalendar.myCalendar()
        self.node4Cal = myCalendar.myCalendar()

        self.insertRandomEvents()
        #self.timeMatrix = np.zeros(4,4)
        self.nodes = nodes
        """[
        ('Node_2', '127.0.0.1', 4001),
        ('Node_3', '127.0.0.1', 4002),
        ('Node_1', '127.0.0.1', 4003),
        ]"""
        print(self.name, "Started")

    def insertRandomEvents(self):
        if self.name == "Node_1":
            eventId = uuid.uuid4()
            newEvent = e.Event(str(eventId), "Dentist", "monday", "12:00", "12:30", ["Node_1", "Node_2"])
            newSEvent = se.SystemEvent("insert", self.dl.timeMatrix, self.name, newEvent, "")
            self.dl.logInternalEvent(newSEvent)
            self.dd.insertIntoDict(newSEvent)
            self.node1Cal.set_Appointment(newSEvent)



    def run(self):
        #mh.start()

        while True:
            print("***** Welcome to the Calendar *****")
            print("* Commands:                       *")
            print("*  i - insert a new event         *")
            print("*  v - view calendar              *")
            print("*  d - delete event               *")
            print("*  z - exit                       *")
            print("***********************************")
            print("Please enter a command:")
            message = input("-> ")
            if message == 'i':
                newEvent = mh.getEventDetails()
                newSEvent = se.SystemEvent("insert", self.dl.timeMatrix, self.name, newEvent, "")
                self.runInsert(newSEvent, 's')


            if message == 'v':
                cal = self.getCorrectCalendar(self.name)
                #cal.viewCalendar()
            if message == "d":
                print("Enter the day of the event you wish to delete: ")
                deleteDay = input("-> ")
                print("Enter the start time of the event you wish to delete: ")
                deleteTime = input("-> ")
                self.runDelete(deleteTime, deleteDay)
            if message == 'z':
                break

    def runDelete(self, startTime, day):
        cal = self.getCorrectCalendar(self.name)
        sevent = self.findEvent(startTime, day, cal)

        if sevent != None:
            self.deleteFromNodeCal(sevent)
            self.dd.deleteFromDict(sevent)
            deleteEvent = sevent.event
            deleteSEvent = se.SystemEvent("delete", self.dl.timeMatrix, self.name, deleteEvent,
                                          "Event Cancelled by participant")

            self.send(deleteSEvent)
        else:
            print("Event not found in calendar")

    def findEvent(self, startTime, day, cal):

        dayList = cal.cal[day]
        startIndex = cal.getIncrementIndex(startTime)
        event = dayList[startIndex]
        return event

    def runInsert(self, newSEvent, sendOrReceive):
        newEvent = newSEvent.event
        participantList = newEvent.participants
        participantCalList = []
        conflict = False
        if newSEvent.eventType == "insert":

            for participant in participantList:
                parCal = self.getCorrectCalendar(participant)
                participantCalList.append(parCal)
                if participantList.__contains__(self.name):
                    conflict = self.checkIsConflictLocal(parCal, newSEvent)
                    if conflict:
                        break
            if conflict:

                if sendOrReceive == 's':
                    #delete event and move on, don't send anything life is dandy
                    print("Event already scheduled for that time.")
                elif sendOrReceive == 'r':
                    # we've received an event that conflicts with something
                    if participantList.__contains__(self.name):
                        self.conflictResolutionProtocol(newSEvent)

            else:
                for cal in participantCalList:
                    cal.set_Appointment(newSEvent)
                if sendOrReceive == 's':
                    self.send(newSEvent)


        else:
            #it is a delete and shouldn't be added to the calendar
            self.deleteFromNodeCal(newSEvent)


    def deleteFromNodeCal(self, newSEvent):
        participantCalList = []
        event = newSEvent.event
        for par in event.participants:
            participantCalList.append(self.getCorrectCalendar(par))
        for parCal in participantCalList:
            parCal.deleteFromCal(newSEvent)
        self.dd.deleteFromDict(newSEvent)

    def conflictResolutionProtocol(self, newSEvent):
        print("Conflict Detected")

        deleteEvent = newSEvent.event
        deleteSEvent = se.SystemEvent("delete", self.dl.timeMatrix, self.name, deleteEvent, "Event conflict: Delete event")

        self.send(deleteSEvent)
        print("Resolution message Sent")


    def send(self, newSEvent):
        #msg_send = input("Enter event details: ")
        newEventJson = self.sendNewEvent(newSEvent)
            #self.log(msg)
            # broadcast the messagei
        for n in self.nodes:
            self.s.sendto(newEventJson.encode('utf-8'), (n[1], n[2]))
        else:
            print('No available appointments at the requested time')


    def receive(self):
        while True:
            data, address = self.s.recvfrom(10000)
            data = data.decode('utf-8')
            msg = str(address[0]) + ", " + str(address[1]) + ": " + data + "\n"
            # call parser
            parsedList = p.splitJson(data)
            self.receiveNewEvent(parsedList)
            #self.log(msg)

    def getSendString(self):
        #sendDL = json.dumps([myevent.__dict__ for myevent in self.dl.distributedLog])
        sendDL = jsonpickle.encode(self.dl.distributedLog)
        sendTimeMatrix = json.dumps(self.dl.timeMatrix)
        sendDD = jsonpickle.encode(self.dd.DD)
        sendPartialLog = jsonpickle.encode(self.dd.partialLog)
        sendDDTimeMatrix = json.dumps(self.dd.timeMatrix)
        return sendDL + DELIMITER + sendTimeMatrix + DELIMITER + sendDD + DELIMITER + sendPartialLog + DELIMITER + sendDDTimeMatrix

    def mergeTheLogs(self, newLog):
        for sysEvent2 in newLog:
            containsEvent = False
            event2 = sysEvent2.event
            for sysEvent1 in self.dl.distributedLog:
                event1 = sysEvent1.event
                if event1.eventID == event2.eventID:
                    containsEvent = True
            if not containsEvent:
                self.dl.distributedLog.append(sysEvent2)

    def receiveNewEvent(self, parsedList):

        newEvent = jsonpickle.decode(parsedList[1])
       # senderLog = self.decodeListofEvents(parsedList[2])
        #print(newEvent.message)
        senderLog = jsonpickle.decode(parsedList[2])
        self.addNewAppointmentsToCal(senderLog)
        self.mergeTheLogs(senderLog)

        # merge the matrices
        senderTimeMatrix = json.loads(parsedList[3])
        self.dl.mergeTimeMatrices(senderTimeMatrix)
        # self.dl.logExternalEvent(msg)
        self.dd.receiveFromNode(parsedList)
        dlfile = open("distributedLog.json", "w")
        ddfile = open("distributedDict.json", "w")
        node1cal = open("node1Cal.json", "w")
        node2cal = open("node2Cal.json", "w")
        node3cal = open("node3Cal.json", "w")
        node4cal = open("node4Cal.json", "w")

        dlfile.write(jsonpickle.encode(self.dl))
        ddfile.write(jsonpickle.encode(self.dd))
        node1cal.write(jsonpickle.encode(self.node1Cal))
        node2cal.write(jsonpickle.encode(self.node2Cal))
        node3cal.write(jsonpickle.encode(self.node3Cal))
        node4cal.write(jsonpickle.encode(self.node4Cal))



    def addNewAppointmentsToCal(self, senderLog):
        senderLog = self.orgSenderLog(senderLog)
        for sevent in senderLog:

            eventInLog = False
            for levent in self.dl.distributedLog:
                event1 = sevent.event
                event2 = levent.event
                if event1.eventID == event2.eventID:
                    if sevent.eventType != "delete":
                        eventInLog = True
                        break

            if not eventInLog:
                self.runInsert(sevent, 'r')


    def orgSenderLog(self, senderLog):
        orgLog = []
        tempLog = []
        for sEvent in senderLog:
            if sEvent.eventType == "delete":
                orgLog.append(sEvent)
            else:
                tempLog.append(sEvent)
        for item in tempLog:
            orgLog.append(item)
        return orgLog

    def sendNewEventTest(self, event):
        #check for conflict here
        eventId = uuid.uuid4()
        newEvent = e.Event(str(eventId), "Dentist", "monday", "12:00", "12:30", "Node_1, Node_2")
        newSEvent = se.SystemEvent("appointment", self.dl.timeMatrix, self.name, newEvent, "Test")
        self.dl.logInternalEvent(newSEvent)
        self.dd.insertIntoDict(newSEvent)
        newEventJson = jsonpickle.encode(newSEvent)
        newEventJson = str(self.id) + DELIMITER + newEventJson + DELIMITER + self.getSendString()
        # newEventJson = self.getSendString(newEvent)

        return newEventJson

    def sendNewEvent(self, sEvent):
        #check for conflict here
        # eventId = uuid.uuid4()
        # newEvent = e.Event(str(eventId), "Dentist", "monday", "12:00", "12:30", "Node_1, Node_2")
        # newSEvent = se.SystemEvent("appointment", self.dl.timeMatrix, self.name, newEvent)
        self.dl.logInternalEvent(sEvent)
        self.dd.insertIntoDict(sEvent)
        newEventJson = jsonpickle.encode(sEvent)
        newEventJson = str(self.id) + DELIMITER + newEventJson + DELIMITER + self.getSendString()
        # newEventJson = self.getSendString(newEvent)

        return newEventJson

    def checkIsConflictLocal(self, cal, sysEvent):
        # call from node before we log or add anything,
        mycal = cal.cal
        event = sysEvent.event
        dayList = mycal[event.day]
        incrementList = self.getAllIncrements(event.start, event.end, cal)
        if dayList[incrementList[0]] != None:
            return True
        elif dayList[incrementList[1]] != None:
            return True
        else:
            for i in range(incrementList[2]):
                if dayList[i] != None:
                    return True
        return False


    def getAllIncrements(self, startTime, endTime, calendar):
        startInc = calendar.getIncrementIndex(startTime)
        endInc = calendar.getIncrementIndex(endTime)
        endInc = endInc - 1
        if startInc != None and endInc != None:
            inBetweenInc = endInc - startInc
            return [startInc, endInc, inBetweenInc]
        return None

    def getCorrectCalendar(self, nodeName):
        if nodeName == "Node_1":
            return self.node1Cal
        if nodeName == "Node_2":
            return self.node2Cal
        if nodeName == "Node_3":
            return self.node3Cal
        if nodeName == "Node_4":
            return self.node4Cal
        return None









