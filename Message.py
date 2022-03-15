import socket
from threading import Thread

'''
Array of all timeslots, each node has an init matrix at t = 0 where all timeslots are available for everyone
If a node creates an event, we insert the event details in that timeslot.
'''


def create_event(msg_send):
    return msg_send != 'conflict'


def view_calendar():
    pass


class Node:
    def __init__(self):
        self.host = '127.0.0.1'  # Server local private ip
        self.port = 4000
        self.name = 'Node_4'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))
        self.nodes = [
            ('Node_2', '127.0.0.1', 4001),
            ('Node_3', '127.0.0.1', 4002),
            ('Node_1', '127.0.0.1', 4003),
        ]
        print(self.name, "Started")

    def run(self):
        print('press i to insert a new event')
        print('press v to view calendar')
        message = input("-> ")
        while True:
            if message == 'i':
                self.send()
            if message == 'v':
                view_calendar()
            print('press i to insert a new event')
            print('press v to view calendar')
            message = input("-> ")

    def send(self):
        msg_send = input("Enter event details: ")
        if create_event(msg_send):
            msg = str(self.host) + ", " + str(self.port) + \
                      ": " + msg_send + "\n"
            self.log(msg)
            # broadcast the message
            for n in self.nodes:
                self.s.sendto(msg_send.encode('utf-8'), (n[1], n[2]))
        else:
            print('No available appointments at the requested time')

    def log(self, msg):
        with open("log.txt", "a") as f:
            f.write(msg)

    def receive(self):
        while True:
            data, address = self.s.recvfrom(1024)
            data = data.decode('utf-8')
            msg = str(address[0]) + ", " + str(address[1]) + ": " + data + "\n"
            self.log(msg)


node = Node()
print('Starting thread 1 (event listener):')
worker_2 = Thread(target=node.receive, args=())
worker_2.start()

print('Starting thread 2 (sender):')
worker_1 = Thread(target=node.run, args=())
worker_1.start()

