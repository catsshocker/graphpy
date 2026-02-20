# gui/graphics/link_handler.py

from core.group import NodesGroup
from core.nodeSocket import SocketInputMode, SocketDirection

class LinkHandler:
    def __init__(self, scene,group: NodesGroup):
        self.scene = scene
        self.group = group
        self.active_link = None  # 存放拉線中的 UI 物件

    def handle_click(self, socket_ui):
        if socket_ui.socket_core.inputMode == SocketInputMode.KEYIN_ONLY:
            print("這個 Socket 是 KEYIN_ONLY 模式，不能連線")
            return
        
        if socket_ui.socket_core.direction == SocketDirection.INPUT and socket_ui.links:
            print("這個輸入 Socket 已經有連線了，不能再連")
            return

        """核心狀態切換：第一次點擊 vs 第二次點擊"""
        if self.active_link is None:
            self._start_link(socket_ui)
        else:
            self._finish_link(socket_ui)

    def _start_link(self, socket_ui):
        print(f"開始連線：從 {socket_ui.socket_core} 開始")
        from gui.graphics.link_ui import LinkUI
        self.active_link = LinkUI(socket_ui)
        self.scene.addItem(self.active_link)
        self.active_link.pos_end = socket_ui.scene_pos

    def _finish_link(self, end_socket_ui):
        print(f"嘗試連線：{self.active_link.start_socket_ui.socket_core} -> {end_socket_ui.socket_core}")
        if self.active_link is None:
            print("錯誤❗：沒有正在連線的物件")
            return
        
        if end_socket_ui.socket_core.inputMode == SocketInputMode.KEYIN_ONLY:
            print("這個 Socket 是 KEYIN_ONLY 模式，不能連線")
            self.cancel()
            return
        
        if end_socket_ui.socket_core.direction == SocketDirection.INPUT and end_socket_ui.links:
            print("這個輸入 Socket 已經有連線了，不能再連")
            return

        start_socket_ui = self.active_link.start_socket_ui
        
        # 檢查是否點到同一個 Socket
        if start_socket_ui == end_socket_ui:
            return # 點到自己，不做事，繼續拉線
        
        # 封裝檢查規則 (Factory/Strategy Pattern 的味道)
        if self._can_connect(start_socket_ui, end_socket_ui):
            # 建立數據關聯
            
            if start_socket_ui.is_input:
                print("發現起點是輸入 Socket，交換起終點")
                start_socket_ui, end_socket_ui = end_socket_ui,start_socket_ui # 交換起終點，讓輸出 Socket 成為起點，符合我們的邏輯習慣 
            self.active_link.start_socket_ui = start_socket_ui
            self.active_link.end_socket_ui = end_socket_ui # 先把終點 UI 存到 LinkUI，讓它能更新路徑

            print(f"嘗試連線2：{start_socket_ui.socket_core} -> {end_socket_ui.socket_core}")

            print(f"建立連線✅：{start_socket_ui.socket_core} -> {end_socket_ui.socket_core}")
            # new_link_core = Link(start_socket_ui.socket_core, end_socket_ui.socket_core)
            # self.group.add_link(new_link_core) # 把 link 加到 group 裡，讓它能管理資料和計算
            
            new_link_core = self.group.add_link(start_socket_ui.socket_core, end_socket_ui.socket_core) # 把 link 加到 group 裡，讓它能管理資料和計算
            self.active_link.link_core = new_link_core # 把對應的 Link 資料物件存到 UI 物件裡，方便以後更新數據和計算

            # 固定 UI 線條
            self.active_link.end_socket_ui = end_socket_ui
            self.active_link.update_path()

            start_socket_ui = self.active_link.start_socket_ui
            end_socket_ui = self.active_link.end_socket_ui
    
            # 讓雙方的 Socket 都記住這條線
            start_socket_ui.add_link(self.active_link)
            end_socket_ui.add_link(self.active_link)
            
            self.active_link.update_path()
            self.active_link = None
        else:
            self.cancel()


    def _can_connect(self, s1, s2):
        """檢查兩個 Socket 是否可以連線的規則"""
        if (s1.is_input != s2.is_input and 
                s1.parent_node_ui != s2.parent_node_ui):
            return True
        return False

    def update_drag(self, scene_pos):
        """更新橡皮筋位置"""
        if self.active_link:
            self.active_link.pos_end = scene_pos
            self.active_link.update_path()

    def cancel(self):
        """取消操作"""
        if self.active_link:
            self.scene.removeItem(self.active_link)
            self.active_link = None

    def abort_link(self):
        """在外部強制終止連線，例如按下 Esc 鍵"""
        self.cancel()