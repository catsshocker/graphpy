import uuid
from .nodeSocket import NodeSocket, SocketDirection, SocketInputMode
from .link import Link
from .registry import NodeRegistry


class Node:
    def __init_subclass__(cls):
        NodeRegistry.register(cls)
    def __init__(self, name=None):
        self.uuid = str(uuid.uuid4())
        self.name = name if name is not None else self.__class__.__name__
        self.group = None 
        self.inputSockets = {}
        self.outputSockets = {}
        self.ui_data = {"pos": [0, 0]} # 用來儲存 UI 相關的資料，例如位置
    
    def add_input_socket(self, name, dataType, inputMode=SocketInputMode.DEFAULT):
        s = NodeSocket(self, name, SocketDirection.INPUT, dataType, inputMode=inputMode)
        self.inputSockets[name] = s
        return s

    def add_output_socket(self, name, dataType):
        s = NodeSocket(self, name, SocketDirection.OUTPUT, dataType)
        self.outputSockets[name] = s
        return s
    
    def is_begin_node(self)-> bool:
        """判斷是否為起始節點：沒有任何輸入連結的節點"""
        for s in self.inputSockets.values():  # 只要有一個輸入插槽有連結，就算起始節點 沒有其他依賴
            if not s.is_begin_socket():
                return False
        return True

    def is_ready(self) -> bool:
        """判斷資料都已到達可以執行"""
        for s in self.inputSockets.values():
            if not s.is_ready():
                return False
        return True

    def execute(self):
        """子類實作"""
        pass

    def _execute(self, *args):
        """子類實作"""
        pass

    def _serialize(self)-> dict:
        return {
            "uuid": self.uuid,
            "class": self.__class__.__name__,
            "name": self.name,
            "ui_data": self.ui_data,
            "param": self.serialize_parm(),
        }
    
    def serialize_parm(self):
        """子類實作，回傳一個 dict，包含節點特有的參數"""
        return {s.name: s.value for s in self.inputSockets.values()}
    
    def load_parm(self, parm_dict):
        """子類實作，從 dict 載入節點特有的參數"""
        for name, value in parm_dict.items():
            if name in self.inputSockets:
                self.inputSockets[name].value = value

    def _reset(self):
        """重置節點狀態，通常在執行前呼叫，確保節點回到初始狀態"""
        for s in self.inputSockets.values():
            s._reset()
        for s in self.outputSockets.values():
            s._reset()

    def destroy(self):
        self.group.delete_node(self.uuid)