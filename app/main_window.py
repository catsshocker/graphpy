#maim_window.py
import sys
from PySide6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt

# 導入你的新類別 (路徑請根據你的資料夾調整)
from gui.graphics.factory import NodeFactory

from core.group import NodesGroup 

from base_lib import add_node
from base_lib import mul_node
from base_lib import const_node

class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GraphPy - Blender Style Node Editor")
        self.resize(800, 600)
        self.group = NodesGroup()

        # 1. 畫布
        self.scene = QGraphicsScene(0, 0, 1800, 1600)
        self.scene.setBackgroundBrush(QColor("#1A1C1F")) # 更接近 Blender 的深色

        # 2. 檢視器
        self.view = QGraphicsView(self.scene)
        # 在 __init__ 的 QGraphicsView 設定後加入：
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # 按住左鍵可平移畫布 (非節點區域)
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse) # 以滑鼠為中心縮放
        self.view.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        
        # 設定為主視窗中心
        self.setCentralWidget(self.view)

        # 3. 測試：使用「靈魂+身體」模式產生節點
        self.create_test_node(add_node)
        self.create_test_node(add_node)
        self.create_test_node(mul_node)
        self.create_test_node(const_node)

        

    def create_test_node(self,node_class=add_node):
        # # 這裡模擬原本應該由 Factory 或 Core 產生的資料
        NodeFactory.spawn_node(node_class, self.scene, self.group)

        # # 建立靈魂 (暫時先寫在這邊測試)
        # class DummySocket:
        #     def __init__(self, label, value=0.0):
        #         self.label = label
        #         self.value = value
        #         self.link = None

        # class DummyCore:
        #     def __init__(self):
        #         self.name = "ADD NODE"
        #         self.pos = [200, 200]
        #         self.inputs = [DummySocket("Value A", 10), DummySocket("Value B", 5)]
        #         self.outputs = [DummySocket("Result")]

        # core = DummyCore()
        
        # # 建立身體 (NodeUI) 並綁定靈魂
        # node_item = NodeUI(core)
        
        # # 加入畫布
        # self.scene.addItem(node_item)