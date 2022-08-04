from gui.core.functions import Functions
from gui.core.json_themes import Themes
from qt_core import *
from gui.widgets import *


class PyToAddImageLabel(QWidget):
    def __init__(self, _img_path, _setup_main_window):
        super(PyToAddImageLabel, self).__init__()

        self.img_path = _img_path
        self.setup_main_window = _setup_main_window

        themes = Themes()
        self.themes = themes.items

        self.setup_ui()
        self.setMaximumSize(100, 60)

    def setup_ui(self):
        self.toadd_image_widget_layout = QVBoxLayout(self)
        self.toadd_image_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.bg_frame = QFrame()
        self.bg_frame.setMinimumSize(QSize(100, 60))
        self.bg_frame.setMaximumSize(QSize(100, 60))
        self.bg_frame.setFrameShape(QFrame.NoFrame)
        self.bg_frame.setFrameShadow(QFrame.Raised)

        self.bg_frame_layout = QStackedLayout(self.bg_frame)
        self.bg_frame_layout.setSpacing(0)
        self.bg_frame_layout.setContentsMargins(0, 0, 0, 0)

        img_pixmap = QPixmap(self.img_path).scaled(100, 60, aspectMode=Qt.AspectRatioMode.IgnoreAspectRatio,
                                      mode=Qt.SmoothTransformation)

        self.to_add_image_label = QLabel()
        self.to_add_image_label.setMinimumHeight(60)
        self.to_add_image_label.setMinimumWidth(100)
        self.to_add_image_label.setMaximumHeight(60)
        self.to_add_image_label.setMaximumWidth(100)
        self.to_add_image_label.setPixmap(img_pixmap)

        self.btn_frame = QFrame()
        self.btn_frame.setMinimumSize(QSize(100, 60))
        self.btn_frame.setMaximumSize(QSize(100, 60))
        self.btn_frame.setFrameShape(QFrame.NoFrame)

        self.btn_frame_layout = QVBoxLayout(self.btn_frame)
        self.btn_frame_layout.setSpacing(0)
        self.btn_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.del_btn = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_my_delete.svg"),
            parent=self.setup_main_window,
            app_parent=self.setup_main_window.ui.central_widget,
            tooltip_text="删除谱图",
            width=40,
            height=40,
            radius=20,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_active"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["pink"]
        )

        self.del_btn.setMaximumWidth(40)
        self.del_btn.setMaximumHeight(40)
        self.btn_frame_layout.addWidget(self.del_btn, Qt.AlignCenter, Qt.AlignCenter)

        # self.btn_frame.setStyleSheet("border-image: url({});".format(self.img_path))

        # self.btn_frame.setGraphicsEffect(self.blur_effect)

        # Palette不起作用
        # self.palette = self.btn_frame.palette()
        # self.brush = QBrush(img_pixmap)
        # self.palette.setBrush(self.btn_frame.backgroundRole(), self.brush)
        # # self.palette.setColor(self.btn_frame.backgroundRole(), QColor(192,253,123))
        # self.btn_frame.setPalette(self.palette)
        # self.btn_frame.setAutoFillBackground(True)
        # self.btn_frame.hide()

        self.bg_frame_layout.addWidget(self.to_add_image_label)
        self.bg_frame_layout.addWidget(self.btn_frame)
        self.bg_frame_layout.setCurrentIndex(0)
        self.bg_frame_layout.setStackingMode(QStackedLayout.StackingMode.StackAll) # 0：只展示一个，1：展示全部

        self.toadd_image_widget_layout.addWidget(self.bg_frame)

    def enterEvent(self, e):  # 鼠标移入label
        self.bg_frame_layout.setCurrentIndex(1)
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(3)
        self.to_add_image_label.setGraphicsEffect(self.blur_effect)

    def leaveEvent(self, e):  # 鼠标离开label
        self.bg_frame_layout.setCurrentIndex(0)
        self.to_add_image_label.setGraphicsEffect(None)