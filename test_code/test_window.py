from gui.widgets import PyPushButton
from qt_core import *
import sys

class Window(QWidget):
    def __init__(self):  # 对象的初始化方法
        super().__init__()  # 调用父类的初始化方法
        self.setUI()

    def setUI(self):  # 控件的各种配置的方法，如果需要修改控件的配置，只需要在该方法中修改即可
        self.resize(500, 500)
        self.move(400, 200)

        button = PyPushButton(
            text="注册",
            radius=8,
            color="red",
            bg_color="red",
            bg_color_hover="red",
            bg_color_pressed="red"
        )

        self.show()


# 用于驱动整个程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())