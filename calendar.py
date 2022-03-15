
import Event as e

class Calendar:

    def __init__(self):
        self.sunday = {}
        self.monday = {}
        self.tuesday = {}
        self.wednesday = {}
        self.thursday = {}
        self.friday = {}
        self.saturday = {}

    def set_Appointment(self, event):
        day_dict = self.get_Day(event.day)
        isFree = self.check_ifFree(event.day, event.start)

        if isFree:
            day_dict[event.start]

    def print_Cal(self):
        print("")

    def check_ifFree(self, day, start):
        day_dict = self.get_Day(day)

        try:
            day_dict[start]
            return False
        except:
            return True

    def get_Day(self, day):
        day = day.lower()

        if day == "sunday":
            return self.sunday

        elif day == "monday":
            return self.monday

        elif day == "tuesday":
            return self. tuesday

        elif day == "wednesday":
            return self.wednesday

        elif day == "thursday":
            return self.thursday

        elif day == "friday":
            return self.friday

        elif day == "saturday":
            return self.saturday

        else:
            return None


