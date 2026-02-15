from .node import Node
from .link import Link
from uuid import uuid4

class NodesGroup:
    def __init__(self):
        self.uuid = str(uuid4())
        self.nodes = {}
        self.links = []

    def add_node(self, node:Node):
        self.nodes[node.uuid] = node
        return node
    
    def add_link(self, socket_from, socket_to):
        newLink = Link(socket_from, socket_to)
        self.links.append(newLink)
        return newLink
    
    def execute(self):
        """
        簡易的執行邏輯：目前先照加入順序執行
        未來可以在這裡加入拓撲排序
        """
        for node in self.nodes.values():
            node.execute()