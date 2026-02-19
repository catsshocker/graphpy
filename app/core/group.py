from .node import Node
from .link import Link
from uuid import uuid4
import threading

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
        node_queue = [node for node in self.nodes.values() if node.is_begin_node()]
        print(f"Initial node queue: {[node.name for node in node_queue]}")
        while node_queue:
            node = node_queue.pop(0)
            node.execute()
            for output_socket in node.outputSockets.values():
                for link in output_socket.link:
                    next_node = link.socket_to.node
                    if next_node.is_ready() and next_node not in node_queue:
                        node_queue.append(next_node)
        
        for node in self.nodes.values():
            node._reset() # 執行完後重置節點狀態，確保下次執行時從乾淨狀態開始

    def _test_async_execute(self):
        node_queue = [node for node in self.nodes.values() if node.is_begin_node()]
        nodes_threads = []
        while node_queue:
            for node in node_queue:
                thread = threading.Thread(target=node.execute)
                thread.start()
                nodes_threads.append(thread)
            for thread in nodes_threads:
                thread.join()
            nodes_threads.clear()
            node_queue_buf = node_queue.copy()
            node_queue.clear()
            for node in node_queue_buf:
                for output_socket in node.outputSockets:
                    for link in output_socket.link:
                        next_node = link.socket_to.node
                        if next_node.is_ready() and next_node not in node_queue:
                            node_queue.append(next_node)

        for node in self.nodes.values():
            node._reset() # 執行完後重置節點狀態，確保下次執行時從乾淨狀態開始
    
    def _serialize(self):
        return {
            "group_uuid": self.uuid,
            "nodes": [node._serialize() for node in self.nodes.values()],
            "links": [link._serialize() for link in self.links]
        }