from .nodeSocket import NodeSocket
from uuid import uuid4

class Link:
    def __init__(self, socket_from:NodeSocket, socket_to:NodeSocket):
        self.uuid = str(uuid4())
        self.socket_from = socket_from
        self.socket_to = socket_to

        self.socket_from.link.append(self)
        self.socket_to.link.append(self)

    def disconnect(self):
        self.socket_from.link.remove(self)
        self.socket_to.link.remove(self)

    def _serialize(self):
        return {
            "uuid": self.uuid,
            "node_from": self.socket_from.node.uuid,
            "socket_from": self.socket_from.name,
            "node_to": self.socket_to.node.uuid,
            "socket_to": self.socket_to.name,
        }