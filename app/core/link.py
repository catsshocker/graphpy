from .nodeSocket import NodeSocket

class Link:
    def __init__(self, socket_from:NodeSocket, socket_to:NodeSocket):
        self.socket_from = socket_from
        self.socket_to = socket_to

        self.socket_from.link.append(self)
        self.socket_to.link.append(self)

    def __del__(self):
        self.socket_from.link.remove(self)
        self.socket_to.link.remove(self)