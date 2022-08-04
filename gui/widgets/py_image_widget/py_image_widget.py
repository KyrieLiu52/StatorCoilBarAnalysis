from qt_core import *
from gui.widgets.py_push_button import PyPushButton

# IMPORT THEMES
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes


class PyImageWidget(QWidget):
    # SIGNALS
    clicked = Signal(object)

    def __init__(self, image_path):
        super().__init__()

        self.image_path = image_path

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # SETUP UI
        self.setup_ui()
        self.setMaximumSize(200, 250)

    def change_btn_clicked(self):
        self.clicked.emit(self.change_btn)

    def delete_btn_clicked(self):
        self.clicked.emit(self.delete_btn)

    def printLine(self, i):
        print(i)

    def setup_ui(self):
        # ADD MENU LAYOUT
        self.image_widget_layout = QVBoxLayout(self)
        self.image_widget_layout.setContentsMargins(5, 0, 5, 0)

        # ADD BG
        self.bg = QFrame()

        # ADD BG LAYOUT
        self.bg_layout = QVBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_layout.setSpacing(0)

        # SET IMAGE
        self.image = QLabel()
        self.image.setMaximumSize(200, 180)
        self.image_layout = QVBoxLayout()
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_layout.addWidget(self.image)
        self.image.setPixmap(QPixmap(self.image_path))
        self.image.setScaledContents(True)  # 图片自适应label大小

        self.combox = QComboBox()
        self.combox.setMaximumSize(200, 30)
        self.combox_layout = QVBoxLayout()
        self.combox_layout.setContentsMargins(0, 3, 0, 3)
        self.combox_layout.addWidget(self.combox)
        self.combox.addItems(['表面AFM谱图', '表面SEM谱图', '2D-SAXS谱图', '2D-WAXD谱图'])

        self.combox.setEditable(False)
        self.combox.setPlaceholderText('选择谱图类型')
        self.combox.setStyleSheet(
            'QComboBox {font-size: 10pt;font-family: 微软雅黑,宋体; color: #8a95aa; selection-color:#8a95aa; '
            'background-color: #1b1e23; selection-background-color: #1b1e23;} '
            'QComboBox:hover {background-color: #21252d;}'
            'QComboBox {text-align:center; border: 0}'
            "QComboBox::down-arrow{image:url('gui/images/svg_icons/icon_arrow_down.png');}"
            "QComboBox:drop-down {outline:0px;border:0px; background-color: #1b1e23;}"
            "QComboBox:drop-down {"  # 选择箭头样式
            "width:30px;  "
            "height:30px; "
            "border: none;  "
            "subcontrol-position: right; "  # 位置
            "subcontrol-origin: padding;}"
            "QComboBox QAbstractItemView {"  # 下拉选项样式
            "color:#8a95aa; "
            "background: #1b1e23; "
            "selection-color:#8a95aa;"
            "selection-background-color: #21252d;}"
        )

        # CUSTOM BUTTONS LAYOUT
        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_buttons_layout.setSpacing(3)
        self.change_btn = PyPushButton(
            text="更换",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.delete_btn = PyPushButton(
            text="删除",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.change_btn.setMaximumSize(100, 40)
        self.delete_btn.setMaximumSize(100, 40)
        self.change_btn.clicked.connect(self.change_btn_clicked)
        self.delete_btn.clicked.connect(self.delete_btn_clicked)
        self.custom_buttons_layout.addWidget(self.change_btn)
        self.custom_buttons_layout.addWidget(self.delete_btn)

        # EXTRA BTNS LAYOUT
        self.bg_layout.addLayout(self.image_layout)
        self.bg_layout.addLayout(self.combox_layout)
        self.bg_layout.addLayout(self.custom_buttons_layout)

        # ADD TO LAYOUT
        self.image_widget_layout.addWidget(self.bg)
