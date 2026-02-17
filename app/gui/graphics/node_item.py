# node_item.py
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsTextItem, QGraphicsItem
from PySide6.QtGui import QColor, QPainterPath, QBrush
from PySide6.QtCore import Qt

from .node_socket import SocketUI 

class NodeUI(QGraphicsPathItem):
    def __init__(self, node_core):
        super().__init__()
        self.node_core = node_core
        
        # 尺寸常數（記得定義，否則 init_ui 會噴錯）
        self.width = 160
        self.header_height = 35
        self.socket_spacing = 30
        
        self.inputs_ui = []
        self.outputs_ui = []
        
        self.init_ui()
        
        # 基本設定
        self.setPos(*self.node_core.ui_data["pos"])
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
        )

    def init_ui(self):
        # 1. 畫主體框框
        content_height = max(len(self.node_core.inputSockets), len(self.node_core.outputSockets)) * self.socket_spacing
        total_height = self.header_height + content_height + 10
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width, total_height, 10, 10)
        self.setPath(path)
        self.setBrush(QColor("#2c3e50")) # 深藍灰
        
        # 2. 標題文字
        self.title = QGraphicsTextItem(self.node_core.name, self)
        self.title.setDefaultTextColor(Qt.lightGray) # 黃色更突出
        self.title.setPos(10, 5)
        
        # 3. 自動生成輸入 Socket (左側)
        for i, socket_data in enumerate(self.node_core.inputSockets):
            # --- 關鍵修正：使用你自定義的 SocketUI ---
            s_ui = SocketUI(self.node_core.inputSockets[socket_data], self) # 這裡會自動處理圓圈和輸入框
            y_pos = self.header_height + i * self.socket_spacing + 15
            s_ui.setPos(0, y_pos)
            self.inputs_ui.append(s_ui)

        # 4. 自動生成輸出 Socket (右側)
        for i, socket_data in enumerate(self.node_core.outputSockets):
            # --- 關鍵修正：輸出項不顯示輸入框，所以要多傳一個參數區分 (選配) ---
            s_ui = SocketUI(self.node_core.outputSockets[socket_data], self, is_input=False) 
            y_pos = self.header_height + i * self.socket_spacing + 15
            s_ui.setPos(self.width, y_pos)
            self.outputs_ui.append(s_ui)
