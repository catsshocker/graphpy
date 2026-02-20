from .node import Node
from .link import Link
from uuid import uuid4
import threading

class NodesGroup:
    def __init__(self):
        self.uuid = str(uuid4())
        self.nodes = {}
        self.links = {}

    def add_node(self, node:Node):
        self.nodes[node.uuid] = node
        return node
    
    def add_link(self, socket_from, socket_to):
        newLink = Link(socket_from, socket_to)
        self.links[newLink.uuid] = newLink
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
            "links": [link._serialize() for link in self.links.values()],
        }
    
    def delete_node(self, node_uuid):
        if node_uuid in self.nodes:
            # 刪除相關連線
            node = self.nodes[node_uuid]
            all_sockets = list(node.inputSockets.values()) + list(node.outputSockets.values())
            for socket in all_sockets:
                for link in socket.link[:]:  # 使用 [:] 避免在迭代中修改列表
                    self.delete_link(link)
            # 從 group 裡刪除節點
            del self.nodes[node_uuid]

    def delete_link(self, link_core):
        if link_core.uuid in self.links:
            link_core.disconnect() # ⬅️ 關鍵：手動解除核心 Socket 與 Link 的引用
            del self.links[link_core.uuid]