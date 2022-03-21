
import Message as ms
import Event as e
import uuid
import myCalendar as cal



def getEventDetails():
    print("******************** Entering New Event ********************")
    print("")
    print("What is the name of the appointment?")
    name = input("-> ")

    day = getDayInput()

    print("What is the appointment's start time? (from 10:00am to 1:30pm")
    start = input("-> ")

    print("What is the appointment's end time (half hour increments only)?")
    end = input("-> ")

    print("Who are the participants? (enter 1 per line and enter d when done)")
    print("1. Node_1         3. Node_3")
    print("2. Node_2         4. Node_4")
    participantList = []
    entry = input("-> ")
    participantList.append(entry)
    #entry = input("-> ")
    while entry != 'd':
        entry = input("-> ")
        if entry != 'd':
            participantList.append(entry)
    print(participantList)
    eventId = uuid.uuid4()
    print(eventId)
    newEvent = e.Event(str(eventId), name, day, start, end, participantList)

    return newEvent




def getDayInput():
    print("What day would you like to schedule the event?")
    print("Enter:")
    print("     m  - monday")
    print("     t  - tuesday")
    print("     w  - wednesday")
    print("     th - thursday")
    print("     f  - friday")
    print("     s  - saturday")
    print("     ss - sunday")
    day = input("-> ")
    day = getDay(day)
    return day

def getDay(input):
    if input == "m":
        return "monday"
    elif input == "t":
        return "tuesday"
    elif input == "w":
        return "wednesday"
    elif input == "th":
        return "thursday"
    elif input == "f":
        return "friday"
    elif input == "s":
        return "saturday"
    elif input == "ss":
        return "sunday"
    else:
        print ("Invalid Entry:")
        getDayInput()

    #def

    #def isLocalEvent(participants):
    #   if


