# gui/graphics/node_scene.py
from PySide6.QtWidgets import QGraphicsScene, QMenu
from PySide6.QtGui import QTransform
from PySide6.QtCore import Qt

from .node_socket import SocketUI
from core.serializer import GraphSerializer
from .link_handler import LinkHandler 
from core.registry import NodeRegistry
from gui.graphics.node_item import NodeUI

from gui.graphics.factory import NodeFactory
from .link_ui import LinkUI

class NodeScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 實體化 Handler 並把自己傳進去
        
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
            print(NodeRegistry.registry())
            self.parent.group.execute()
            event.accept()

        elif event.key() == Qt.Key.Key_Escape:
            self.cancel_ongoing_actions()
            event.accept()

        elif event.key() == Qt.Key.Key_Delete:
            # 取得目前選中的所有物件 (QGraphicsScene.selectedItems)
            selected_items = self.selectedItems()
            
            for item in selected_items:
                # 確保我們只對 NodeUI 進行刪除
                if isinstance(item, NodeUI):
                    item.destroy()
                # 如果使用者單獨選中了線段 Link，也可以在這邊處理
                elif isinstance(item, LinkUI):
                    print("刪除連線")
                    item.destroy()
            event.accept()

        else:
            super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        # 取得點擊位置是否有物件
        item = self.itemAt(event.scenePos(), self.parent.view.transform())
        
        # 如果點在空白處，彈出「新增節點」選單
        if item is None:
            print("【Scene 測試】在畫布上偵測到右鍵")
            self.show_add_node_menu(event)
        else:
            super().contextMenuEvent(event)


    def show_add_node_menu(self, event):
        menu = QMenu()
        # 這裡 registry() 是一個簡單的字典：{"AddNode": class, "MulNode": class}
        for node_name, node_class in NodeRegistry.registry().items():
            # 直接把節點加在主選單，不需要子選單
            action = menu.addAction(node_name)
            
            # 綁定點擊事件
            action.triggered.connect(
                lambda checked=False, nc=node_class, pos=event.scenePos(): 
                NodeFactory.spawn_node(nc, self, self.parent.group, pos.toTuple())
            )

        menu.exec(event.screenPos())

    def cancel_ongoing_actions(self):
        """取消當前進行中的所有互動動作"""
        # 1. 處理連線中的狀態
        if hasattr(self, 'link_handler'):
            # 假設你的 link_handler 有一個方法來處理取消
            self.link_handler.abort_link()
            print("【Scene】連線動作已取消")