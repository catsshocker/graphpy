import uuid
from .nodeSocket import NodeSocket, SocketDirection
from .link import Link


class Node:
    def __init__(self, name=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.inputSockets = []
        self.outputSockets = []
    
    def add_input_socket(self, name, dataType):
        s = NodeSocket(self, name, SocketDirection.INPUT, dataType)
        self.inputSockets.append(s)
        return s

    def add_output_socket(self, name, dataType):
        s = NodeSocket(self, name, SocketDirection.OUTPUT, dataType)
        self.outputSockets.append(s)
        return s
    
    def is_begin_node(self)-> bool:
        """判斷是否為起始節點：沒有任何輸入連結的節點"""
        for s in self.inputSockets:
            if s.link:
                return False
        return True

    def is_ready(self) -> bool:
        """判斷資料都已到達可以執行"""
        for s in self.inputSockets:
            if not s._is_ready:
                return False
        return True

    def execute(self):
        """子類實作"""
        pass

