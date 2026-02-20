#node_socket.py
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsProxyWidget, QLineEdit,QGraphicsTextItem
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt

from core.nodeSocket import SocketDirection, SocketInputMode

class SocketUI(QGraphicsEllipseItem):
    def __init__(self, socket_core, parent_node_ui, is_input=True):
        super().__init__(-6, -6, 12, 12, parent_node_ui)
        self.socket_core = socket_core
        # self.parent_node_ui = parent_node_ui
        self._is_input = is_input

        self.links = [] # 這裡存 LinkUI 的實例，方便更新外觀
        
        self.setBrush(QBrush(QColor("#f1c40f")))
        self.setZValue(1)
        
        # 畫標籤
        label_text = self.socket_core.name if len(self.socket_core.name) < 10 else self.socket_core.name[:7] + "..."
        self.label = QGraphicsTextItem(label_text, self)
        self.label.setDefaultTextColor(Qt.lightGray)

        self.label.setAcceptedMouseButtons(Qt.NoButton)

        if self._is_input:
            # 輸入項：圓圈在左，文字在圓圈右邊
            self.label.setPos(12, -12) 
        else:
            # 輸出項：圓圈在右，文字在圓圈左邊
            # 我們要把文字往左推，這裡可以根據標籤長度微調，通常 -50 左右
            self.label.setPos(-50, -12)

        # 只有「輸入型」的 Socket 且「沒接線」時才需要輸入框
        self.proxy_widget = None
        if self._is_input:
            self.init_input_widget()

    def init_input_widget(self):
        # 1. 建立真實的 PySide 控件
        self.line_edit = QLineEdit()
        self.line_edit.setText(str(self.socket_core.value))
        self.line_edit.setFixedWidth(40)
        self.line_edit.setStyleSheet("background: #1e1e1e; color: white; border: 1px solid #555;")
        
        # 2. 建立代理，把控件塞進畫布
        self.proxy_widget = QGraphicsProxyWidget(self)
        self.proxy_widget.setWidget(self.line_edit)
        
        # 3. 調整位置 (放在圓圈旁邊)
        self.proxy_widget.setPos(45, -10) 
        
        # 4. 監聽數值改變，回傳給靈魂
        self.line_edit.textChanged.connect(self.on_value_change)
        
        # 初始檢查：如果已經接線，就隱藏
        self.update_appearance()

    def on_value_change(self, text):
        try:
            self.socket_core.value = float(text)
            print(f"Socket {self.socket_core.name} 的值更新為 {self.socket_core.value}")
        except ValueError:
            pass

    def update_appearance(self):
        """根據核心數據狀態同步 UI"""
        linked = self.socket_core.is_linked()
        if self.socket_core.inputMode == SocketInputMode.LINK_ONLY:
            self.proxy_widget.hide() # 連線專用，永遠不顯示輸入框
        if self.socket_core.inputMode == SocketInputMode.KEYIN_ONLY:
            self.setBrush(QBrush(QColor("#1c263b")))
        else:
            if linked:
                self.setBrush(QBrush(QColor("#27ae60"))) # 綠色
                if self.proxy_widget: self.proxy_widget.hide() # 接線了，隱藏輸入框
            else:
                self.setBrush(QBrush(QColor("#f1c40f"))) # 黃色
                if self.proxy_widget: self.proxy_widget.show() # 沒線，顯示輸入框


    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    @property
    def scene_pos(self):
        """回傳 Socket 圓心的世界座標 (Scene Position)"""
        # mapToScene(0, 0) 會把本地座標的中心點轉為畫布座標
        return self.mapToScene(0, 0)
    
    # 順便檢查這兩個屬性是否也有定義，因為 LinkHandler 會用到
    @property
    def is_input(self):
        return self.socket_core.direction == SocketDirection.INPUT

    @property
    def parent_node_ui(self):
        # 這裡回傳它的父物件，也就是 NodeUI
        return self.parentItem()
    
    def update_links(self):
        for link in self.links:
            link.update_path()

    def add_link(self, link_ui):
        self.links.append(link_ui)
        self.update_appearance()

    def delete_link(self, link_ui):
        if link_ui in self.links:
            self.links.remove(link_ui)
            self.update_appearance()

    def destroy(self):
        # 刪除相關連線
        for link in self.links[:]:
            link.destroy() # 這裡會從畫布和資料結構中刪除連線
        self.links.clear()
        # 從畫布上刪除自己
        scene = self.scene()
        if scene:
            scene.removeItem(self)