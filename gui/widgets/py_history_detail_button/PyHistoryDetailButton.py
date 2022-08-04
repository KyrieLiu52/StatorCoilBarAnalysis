from gui.widgets import PyPushButton
from qt_core import *


class PyHistoryDetailButton(QWidget):

    def __init__(self, img_id):
        super(PyHistoryDetailButton, self).__init__()
        self.img_id = img_id

        self.col_btn = PyPushButton(
            text="查看",
            radius=8,
            color='#8a95aa',
            bg_color='#1b1e23',
            bg_color_hover='#21252d',
            bg_color_pressed='#3f6fd1'
        )
        self.col_btn.setFixedSize(100, 40)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.col_btn)
        self.btn_layout.setAlignment(self.col_btn, Qt.AlignCenter)
        self.setLayout(self.btn_layout)
