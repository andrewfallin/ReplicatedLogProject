import uuid
import Event as e
import SystemEvent as se
import DistributedDict as DD
import DistributedLog as DL

class myCalendar:

    def __init__(self):
        self.cal = {}
        self.initCal()

    def initCal(self):
        self.cal["monday"] = [None] * 10
        self.cal["tuesday"] = [None] * 10
        self.cal["wednesday"] = [None] * 10
        self.cal["thursday"] = [None] * 10
        self.cal["friday"] = [None] * 10
        self.cal["saturday"] = [None] * 10
        self.cal["sunday"] = [None] * 10
        # 0 = 10am
        # 1 = 10:30am
        # 2 = 11am
        # 3 = 11:30am
        # 4 = 12am
        # 5 = 12:30am
        # 6 = 13am
        # 7 = 13:30am
        # 8 = 14pm
        # 9 = 14:30

    def viewCalendar(self):
        for key in self.cal:
            print("***** " + key + " *****")
            timeSlots = self.cal[key]
            print("10:00am       " + self.getEventName(timeSlots[0]))
            print("10:30am       " + self.getEventName(timeSlots[1]))
            print("11:00am       " + self.getEventName(timeSlots[2]))
            print("11:30am       " + self.getEventName(timeSlots[3]))
            print("12:00pm       " + self.getEventName(timeSlots[4]))
            print("12:30pm       " + self.getEventName(timeSlots[5]))
            print(" 1:00pm       " + self.getEventName(timeSlots[6]))
            print(" 1:30am       " + self.getEventName(timeSlots[7]))
            print(" 2:00pm       " + self.getEventName(timeSlots[8]))
            print(" 2:30am       " + self.getEventName(timeSlots[9]))

    def getEventName(self, sevent):
        if sevent == None:
            return "Empty"
        else:
            event = sevent.event
            return event.name

    def set_Appointment(self, sysEvent):
        event = sysEvent.event
        #day = self.get_Day(event.day)
        incrementList = self.getAllIncrements(event.start, event.end)
        self.insertAppointmentIntoCorrectSpot(sysEvent, incrementList)

    def insertAppointmentIntoCorrectSpot(self, sysEvent, incrementList):
        event = sysEvent.event
        dayList = self.cal[event.day]
        startIndex= incrementList[0]
        endIndex = incrementList[1]
        dayList[startIndex] = sysEvent
        dayList[endIndex] = sysEvent
        for i in range(incrementList[2]):
            dayList[startIndex + i] = sysEvent

    @staticmethod
    def getIncrementIndex(increment):
        if increment == "10:00":
            return 0
        elif increment == "10:30":
            return 1
        elif increment == "11:00":
            return 2
        elif increment == "11:30":
            return 3
        if increment == "12:00":
            return 4
        elif increment == "12:30":
            return 5
        elif increment == "13:00" or increment == "1:00":
            return 6
        elif increment == "13:30" or increment == "1:30":
            return 7
        elif increment == "14:00" or increment == "2:00":
            return 8
        elif increment == "14:30" or increment == "2:30":
            return 9
        else:
            return None

    def getAllIncrements(self, startTime, endTime):
        startInc = self.getIncrementIndex(startTime)
        endInc = self.getIncrementIndex(endTime)
        endInc = endInc - 1
        if startInc != None and endInc != None:
            inBetweenInc = endInc - startInc
            return [startInc, endInc, inBetweenInc]
        return None

    def check_ifFree(self, day, start):
        day_dict = self.get_Day(day)

        try:
            day_dict[start]
            return False
        except:
            return True

    def checkIsConflict(self, sysEvent):
        # call from node before we log or add anything,
        event = sysEvent.event
        dayList = self.cal[event.day]
        incrementList = self.getAllIncrements(event.start, event.end)
        if dayList[incrementList[0]] != None:
            return True
        elif dayList[incrementList[1]] != None:
            return True
        else:
            for i in range(incrementList[2]):
                if dayList[i] != None:
                    return True
        return False

    def isInCal(self, event, dayList, incrementList):
        if incrementList[2] == 0:
            calEvent = dayList[incrementList[0]]
            if calEvent != None:
                if calEvent.event.eventID == event.eventID:
                    return True
        else:
            for i in range(incrementList[2]):
                calEvent = dayList[i]
                #print(calEvent)
                if calEvent != None:
                    if calEvent.eventID == event.eventID:
                        return True

        #print("No event in calendar")
        return False

    def deleteFromCal(self, sEvent):
        event = sEvent.event
        dayList = self.cal[event.day]
        incrementList = self.getAllIncrements(event.start, event.end)
        inCal = self.isInCal(event, dayList, incrementList)
        if inCal:
            if incrementList[2] == 0:
                dayList[incrementList[0]] = None
            else:
                for i in range(incrementList[2]):
                    dayList[i] = None
            #self.viewCalendar()
            print("Event deleted")








if __name__ == "__main__":
    eventId = uuid.uuid4()
    newCal = myCalendar()
    newEvent = e.Event(str(eventId), "Dentist", "monday", "12:00", "1:00", "Node_1, Node_2")
    newSEvent = se.SystemEvent("appointment", None, None, newEvent)
    newCal.set_Appointment(newSEvent)


