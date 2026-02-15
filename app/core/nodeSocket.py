from enum import Enum , auto
# from .link import Link

class SocketDirection(Enum):
    INPUT = auto()
    OUTPUT = auto()


class NodeSocket:
    def __init__(self, node, name, direction:SocketDirection, dataType):
        self.name = name
        self.node = node
        self.direction = direction
        self.dataType = dataType
        self.link = []
        self.value = None
        self._is_ready = False

    def write(self, value):
        if self.direction == SocketDirection.OUTPUT:
            self.value = value
            for link in self.link:
                link.socket_to._last_node_velue_write(value)
        else:
            raise Exception("Cannot write to an input socket")
        
    def _last_node_velue_write(self, value):
        self.value = value
        self._is_ready = True

    def read(self):
        return self.value