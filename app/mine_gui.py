# mine_gui.py
import sys
from PySide6.QtWidgets import QApplication
from main_window import NodeEditorWindow

def main():
    # 建立應用程式實例
    app = QApplication(sys.argv)

    # 建立我們剛剛寫好的視窗
    window = NodeEditorWindow()
    
    window.show()

    # 啟動事件迴圈
    sys.exit(app.exec())

if __name__ == "__main__":
    main()