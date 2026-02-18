from enum import Enum , auto
# from .link import Link

class SocketDirection(Enum):
    INPUT = auto()
    OUTPUT = auto()

class SocketInputMode(Enum):
    DEFAULT = auto() # 預設模式：輸入框，除非接線了才隱藏
    KEYIN_ONLY = auto() # 只能輸入框，永遠不顯示連線狀態
    LINK_ONLY = auto() # 只能連線，永遠不顯示輸入框


class NodeSocket:
    def __init__(self, node, name, direction:SocketDirection, dataType, inputMode=SocketInputMode.DEFAULT):
        self.name = name
        self.node = node
        self.direction = direction
        self.dataType = dataType
        self.inputMode = inputMode # 預設輸入模式
        self.link = []
        self.value = dataType() # 預設值，例如 float 就是 0.0
        self._is_ready = False if self.inputMode == SocketInputMode.LINK_ONLY else True

    def write(self, value):
        if self.direction == SocketDirection.OUTPUT:
            self.value = value
            for link in self.link:
                link.socket_to._last_node_velue_write(value)
        else:
            raise Exception("Cannot write to an input socket")
        
    def is_ready(self):
        """已經收到前一級的資料了"""
        if self.is_linked() or self.inputMode != SocketInputMode.LINK_ONLY:
            return self._is_ready
        else:
            raise Exception("This socket is link-only but has no link")
            return False
    
    def is_linked(self):
        """有沒有連接線"""
        return len(self.link) > 0
    
    def is_begin_socket(self):
        """判斷是否為起始插槽：沒有任何連結的輸入插槽"""
        return self.direction == SocketDirection.INPUT and not self.is_linked() or self.inputMode == SocketInputMode.KEYIN_ONLY
    

    def _last_node_velue_write(self, value):
        self.value = value
        self._is_ready = True

    def read(self):
        return self.value