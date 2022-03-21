
import Event as e
class SystemEvent:

    def __init__(self, eventType, matrix, originNode, event, message):
        self.eventType = eventType
        self.matrix = matrix
        self.originNode = originNode
        self.event = event
        self.message = message
