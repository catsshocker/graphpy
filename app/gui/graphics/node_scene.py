# gui/graphics/node_scene.py
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QTransform
from PySide6.QtCore import Qt

from .node_socket import SocketUI
from core.serializer import GraphSerializer

class NodeScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 實體化 Handler 並把自己傳進去
        from .link_handler import LinkHandler 
        self.parent = parent
        self.link_handler = LinkHandler(self,parent.group) # 把 group 傳給 link_handler，讓它能在建立連線時更新 group 的資料

    def mousePressEvent(self, event):
        # 1. 取得點擊位置的物件
        item = self.itemAt(event.scenePos(), QTransform())
        
        # 2. 直接找自家的 link_handler，不需要找 window
        if isinstance(item, SocketUI):
            self.link_handler.handle_click(item)
        elif item is None:
            self.link_handler.cancel()
            
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # 一樣，直接呼叫自家的 link_handler
        self.link_handler.update_drag(event.scenePos())
        super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F10:
            print("【Scene 測試】在畫布上偵測到 F10")
            print("生成節點圖json")
            self.parent.group._serialize()
            GraphSerializer.save_to_file(self.parent.group,"000.json")
            self.parent.group.execute()
            event.accept()
        else:
            super().keyPressEvent(event)