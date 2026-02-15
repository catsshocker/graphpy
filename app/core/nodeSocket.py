from enum import Enum , auto
# from .link import Link

class SocketDirection(Enum):
    INPUT = auto()
    OUTPUT = auto()


class Socket:
    def __init__(self, node, name, direction:SocketDirection, dataType):
        self.name = name
        self.node = node
        self.direction = direction
        self.dataType = dataType
        self.link: list[Link] = []
        self.value = None

    def read(self):
        if self.direction == SocketDirection.INPUT:
            if self.link:
                return self.link[0].socket_from.read()
            else:
                return None
        else:
            return self.value
        
    def write(self, value):
        if self.direction == SocketDirection.OUTPUT:
            self.value = value
        else:
            raise Exception("Cannot write to an input socket")