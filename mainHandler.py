
import Message as ms
import Event as e
import calendar as cal

def start():
    print("***** Welcome to the Calendar *****")
    print("* Commands:                       *")
    print("*  i - insert a new event         *")
    print("*  v - view calendar              *")
    print("*  z - exit                       *")
    print("***********************************")
    print("Please enter a command:")
    message = input("-> ")
    while True:
        if message == 'i':
            insertEvent()
        if message == 'v':
            print("lol")
        if message == 'z':
            break
            #view_calendar()
        message = input("-> ")

def insertEvent():
    print("******************** Entering New Event ********************")
    print("")
    print("What is the name of the appointment?")
    name = input("-> ")

    day = getDayInput()

    print("What is the appointment's start time?")
    start = input("-> ")

    print("Who are the participants (please separate by commas)?")
    print("1. node1         3. node3")
    print("2. node2         4. node4")
    participants = input("-> ")

    newEvent = e.Event(name, day, start, 0, participants)
    print(newEvent)

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


