import uuid
from .nodeSocket import NodeSocket, SocketDirection
from .link import Link


class Node:
    def __init__(self, name=None):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.inputSockets = {}
        self.outputSockets = {}
    
    def add_input_socket(self, name, dataType):
        s = NodeSocket(self, name, SocketDirection.INPUT, dataType)
        self.inputSockets[name] = s
        return s

    def add_output_socket(self, name, dataType):
        s = NodeSocket(self, name, SocketDirection.OUTPUT, dataType)
        self.outputSockets[name] = s
        return s
    
    def is_begin_node(self)-> bool:
        """判斷是否為起始節點：沒有任何輸入連結的節點"""
        for s in self.inputSockets.values():
            if s.link:
                return False
        return True

    def is_ready(self) -> bool:
        """判斷資料都已到達可以執行"""
        for s in self.inputSockets.values():
            if not s._is_ready:
                return False
        return True

    def execute(self):
        """子類實作"""
        pass

    def _serialize(self)-> dict:
        return {
            "uuid": self.uuid,
            "class": self.__class__.__name__,
            "name": self.name,
            "param": self.serialize_parm(),
        }
    
    def serialize_parm(self):
        """子類實作，回傳一個 dict，包含節點特有的參數"""
        return {}
    
    def load_parm(self, parm_dict):
        """子類實作，從 dict 載入節點特有的參數"""
        pass