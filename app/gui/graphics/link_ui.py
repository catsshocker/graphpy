from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QPainterPath, QColor
from PySide6.QtCore import Qt,QPointF

class LinkUI(QGraphicsPathItem):
    def __init__(self, start_socket_ui, end_socket_ui=None):
        super().__init__()
        self.start_socket_ui = start_socket_ui
        self.end_socket_ui = end_socket_ui # 如果是拖曳中，這可能是 None
        self.pos_end = None # 拖曳中的滑鼠位置
        self.link_core = None # 這裡可以存放對應的 Link 資料物件，方便更新數據和計算
        
        # 設定線條外觀 (Blender 風格：橘色或白色粗線)
        self.setPen(QPen(QColor("#ffffff"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setZValue(-1) # 讓線條在節點下方

    def update_path(self):
        """核心：根據起點和終點計算貝茲曲線"""
        path = QPainterPath()
        
        # 起點位置 (世界座標)
        p1 = self.start_socket_ui.scene_pos
        
        # 終點位置：如果是已連線，取 Socket 位置；如果是拖曳中，取滑鼠位置
        if self.end_socket_ui:
            p4 = self.end_socket_ui.scene_pos
        else:
            p4 = self.pos_end if self.pos_end else p1

        # 計算貝茲曲線的控制點 (控制點決定曲線的「弧度」)
        dx = abs(p4.x() - p1.x()) * 0.5

        # 計算偏移量
        offset = dx if dx > 50 else 50
        
        # 使用 QPointF 進行加減運算
        if not self.start_socket_ui.is_input:
            # 如果是輸出 Socket (往右長)
            p2 = p1 + QPointF(offset, 0)
            p3 = p4 - QPointF(offset, 0)
        else:
            # 如果是輸入 Socket (往左長)
            p2 = p1 - QPointF(offset, 0)
            p3 = p4 + QPointF(offset, 0)

        path.moveTo(p1)
        path.cubicTo(p2, p3, p4)
        self.setPath(path)