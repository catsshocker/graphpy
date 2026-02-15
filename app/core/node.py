import uuid
from .nodeSocket import Socket, SocketDirection
from .link import Link


class Node:
    def __init__(self, name=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.inputSockets = []
        self.outputSockets = []
    
    def add_input_socket(self, name, dataType):
        s = Socket(self, name, SocketDirection.INPUT, dataType)
        self.inputSockets.append(s)
        return s

    def add_output_socket(self, name, dataType):
        s = Socket(self, name, SocketDirection.OUTPUT, dataType)
        self.outputSockets.append(s)
        return s

    def execute(self):
        """子類實作"""
        pass

