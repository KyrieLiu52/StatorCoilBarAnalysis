# -*- coding: utf-8 -*-
from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import *


class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # SET INITIAL PARAMETERS
        MainWindow.resize(600, 400)
        # MainWindow.resize(self.settings["startup_size"][0], self.settings["startup_size"][1])
        # MainWindow.setMaximumSize(400, 300)
        
        # SET CENTRAL WIDGET
        # Add central widget to app
        # ///////////////////////////////////////////////////////////////
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setStyleSheet(f'''
                            font: {self.settings["font"]["text_size"]}pt "{self.settings["font"]["family"]}";
                            color: {self.themes["app_color"]["text_foreground"]};
                        ''')
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        if self.settings["custom_title_bar"]:
            self.central_widget_layout.setContentsMargins(10, 10, 10, 10)
        else:
            self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        # LOAD PY WINDOW CUSTOM WIDGET
        # Add inside PyWindow "layout" all Widgets
        # ///////////////////////////////////////////////////////////////
        self.window = PyWindow(
            MainWindow,
            bg_color=self.themes["app_color"]["bg_one"],
            border_color=self.themes["app_color"]["bg_two"],
            text_color=self.themes["app_color"]["text_foreground"]
        )
        # If disable custom title bar
        if not self.settings["custom_title_bar"]:
            self.window.set_stylesheet(border_radius=0, border_size=0)

        # ADD PY WINDOW TO CENTRAL WIDGET
        self.central_widget_layout.addWidget(self.window)
        
        self.login_frame = QFrame(self.window)
        self.login_frame.setObjectName(u"login_frame")
        self.login_frame.setFixedSize(QSize(400, 350))
        self.login_frame.setFrameShape(QFrame.NoFrame)
        self.login_frame.setFrameShadow(QFrame.Raised)
        self.login_content_layout = QVBoxLayout(self.login_frame)
        self.login_content_layout.setObjectName(u"login_content_layout")
        self.login_title_frame = QFrame(self.login_frame)
        self.login_title_frame.setObjectName(u"login_title_frame")
        self.login_title_frame.setFrameShape(QFrame.NoFrame)
        self.login_title_frame.setFrameShadow(QFrame.Raised)
        self.login_title_layout = QVBoxLayout(self.login_title_frame)
        self.login_title_layout.setObjectName(u"login_title_layout")

        self.login_content_layout.addWidget(self.login_title_frame)

        self.login_text_frame = QFrame(self.login_frame)
        self.login_text_frame.setObjectName(u"login_text_frame")
        self.login_text_frame.setFrameShape(QFrame.NoFrame)
        self.login_text_frame.setFrameShadow(QFrame.Raised)
        self.login_label_and_edit_layout = QHBoxLayout(self.login_text_frame)
        self.login_label_and_edit_layout.setObjectName(u"login_label_and_edit_layout")
        self.login_label_frame = QFrame(self.login_text_frame)
        self.login_label_frame.setObjectName(u"login_label_frame")
        self.login_label_frame.setFrameShape(QFrame.NoFrame)
        self.login_label_frame.setFrameShadow(QFrame.Raised)
        self.login_label_layout = QVBoxLayout(self.login_label_frame)
        self.login_label_layout.setObjectName(u"login_label_layout")
        self.label_username_frame = QFrame(self.login_label_frame)
        self.label_username_frame.setObjectName(u"label_username_frame")
        self.label_username_frame.setMinimumSize(QSize(100, 40))
        self.label_username_frame.setFrameShape(QFrame.NoFrame)
        self.label_username_frame.setFrameShadow(QFrame.Raised)
        self.label_username_layout = QVBoxLayout(self.label_username_frame)
        self.label_username_layout.setObjectName(u"label_username_layout")
        self.label_username_layout.setContentsMargins(-1, -1, -1, 0)

        self.login_label_layout.addWidget(self.label_username_frame)

        self.label_pwd_frame = QFrame(self.login_label_frame)
        self.label_pwd_frame.setObjectName(u"label_pwd_frame")
        self.label_pwd_frame.setMinimumSize(QSize(100, 40))
        self.label_pwd_frame.setFrameShape(QFrame.NoFrame)
        self.label_pwd_frame.setFrameShadow(QFrame.Raised)
        self.label_pwd_layout = QVBoxLayout(self.label_pwd_frame)
        self.label_pwd_layout.setObjectName(u"label_pwd_layout")
        self.label_pwd_layout.setContentsMargins(-1, 20, -1, -1)

        self.login_label_layout.addWidget(self.label_pwd_frame)

        self.login_label_and_edit_layout.addWidget(self.login_label_frame)

        self.login_text_input_frame = QFrame(self.login_text_frame)
        self.login_text_input_frame.setObjectName(u"login_text_input_frame")
        self.login_text_input_frame.setFrameShape(QFrame.NoFrame)
        self.login_text_input_frame.setFrameShadow(QFrame.Raised)
        self.login_edit_layout = QVBoxLayout(self.login_text_input_frame)
        self.login_edit_layout.setObjectName(u"login_edit_layout")
        self.input_username_frame = QFrame(self.login_text_input_frame)
        self.input_username_frame.setObjectName(u"input_username_frame")
        self.input_username_frame.setMinimumSize(QSize(0, 40))
        self.input_username_frame.setFrameShape(QFrame.NoFrame)
        self.input_username_frame.setFrameShadow(QFrame.Raised)
        self.input_username_layout = QVBoxLayout(self.input_username_frame)
        self.input_username_layout.setObjectName(u"input_username_layout")
        self.input_username_layout.setContentsMargins(-1, -1, -1, 0)

        self.login_edit_layout.addWidget(self.input_username_frame)

        self.input_pwd_frame = QFrame(self.login_text_input_frame)
        self.input_pwd_frame.setObjectName(u"input_pwd_frame")
        self.input_pwd_frame.setMinimumSize(QSize(0, 40))
        self.input_pwd_frame.setFrameShape(QFrame.NoFrame)
        self.input_pwd_frame.setFrameShadow(QFrame.Raised)
        self.input_pwd_layout = QVBoxLayout(self.input_pwd_frame)
        self.input_pwd_layout.setObjectName(u"input_pwd_layout")
        self.input_pwd_layout.setContentsMargins(-1, 20, -1, -1)

        self.login_edit_layout.addWidget(self.input_pwd_frame)

        self.login_label_and_edit_layout.addWidget(self.login_text_input_frame)

        self.login_content_layout.addWidget(self.login_text_frame)

        self.login_btn_frame = QFrame(self.login_frame)
        self.login_btn_frame.setObjectName(u"login_btn_frame")
        self.login_btn_frame.setFrameShape(QFrame.NoFrame)
        self.login_btn_frame.setFrameShadow(QFrame.Raised)
        self.login_btn_layout = QHBoxLayout(self.login_btn_frame)
        self.login_btn_layout.setObjectName(u"login_btn_layout")

        self.login_content_layout.addWidget(self.login_btn_frame)

        # ///////////////////////////////////////////////////////////////
        # LOGIN PAGE
        # ///////////////////////////////////////////////////////////////
        # LOGIN TITLE
        self.label_login_title = QLabel(
            text="东方电机"
        )
        self.label_login_title.setStyleSheet(
            "color: white;"
            "font: bold 32px"
        )
        self.label_login_title.setMinimumHeight(40)
        self.login_title_layout.addWidget(self.label_login_title, Qt.AlignCenter, Qt.AlignCenter)

        # USERNAME LABEL
        self.label_username = QLabel(
            text="用户名：",
        )
        self.label_username.setAlignment(Qt.AlignCenter)
        self.label_username.setStyleSheet(
            "font: bold 18px;"
        )
        self.label_username.setMinimumHeight(40)
        self.label_username_layout.addWidget(self.label_username)

        # PASSWORD LABEL
        self.label_pwd = QLabel(
            text="密码：",
        )
        self.label_pwd.setStyleSheet(
            "font: bold 18px;"
        )
        self.label_pwd.setAlignment(Qt.AlignCenter)
        self.label_pwd.setMinimumHeight(40)
        self.label_pwd_layout.addWidget(self.label_pwd)

        # USERNAME INPUT
        self.input_username = PyLineEdit()
        self.input_username.setMinimumHeight(40)
        self.input_username.setPlaceholderText("请输入用户名...")
        self.input_username.setText('admin')
        # self.input_username.returnPressed.connect(lambda: login_function.verify())  # 绑定回车按钮与登录函数
        self.input_username_layout.addWidget(self.input_username)

        # PASSWORD INPUT
        self.input_pwd = PyLineEdit()
        self.input_pwd.setMinimumHeight(40)
        self.input_pwd.setPlaceholderText("请输入密码...")
        self.input_pwd.setEchoMode(QLineEdit.Password)
        # self.input_pwd.returnPressed.connect(lambda: login_function.verify())  # 绑定回车按钮与登录函数
        self.input_pwd_layout.addWidget(self.input_pwd)

        # LOGIN BUTTON
        self.login_btn = PyPushButton(
            text="登录",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setMaximumWidth(200)
        self.login_btn.setContentsMargins(0, 0, 0, 0)
        # self.login_btn.clicked.connect(lambda: login_function.verify())
        self.login_btn_layout.addWidget(self.login_btn)

        # ///////////////////////////////////////////////////////////////
        # WINDOW
        # ///////////////////////////////////////////////////////////////
        # ADD RIGHT WIDGETS
        # Add here the right widgets
        # ///////////////////////////////////////////////////////////////
        self.app_frame = QFrame()

        # ADD RIGHT APP LAYOUT
        self.app_layout = QVBoxLayout(self.app_frame)
        self.app_layout.setContentsMargins(3, 3, 3, 3)
        self.app_layout.setSpacing(6)

        # ADD TITLE BAR FRAME
        # ///////////////////////////////////////////////////////////////
        self.title_bar_frame = QFrame()
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = QVBoxLayout(self.title_bar_frame)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # ADD CUSTOM TITLE BAR TO LAYOUT
        self.title_bar = PyLoginTitleBar(
            MainWindow,
            logo_width=300,
            app_parent=self.central_widget,
            logo_image="logo_dongfang.png",
            bg_color=self.themes["app_color"]["bg_two"],
            div_color=self.themes["app_color"]["bg_three"],
            btn_bg_color=self.themes["app_color"]["bg_two"],
            btn_bg_color_hover=self.themes["app_color"]["bg_three"],
            btn_bg_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            dark_one=self.themes["app_color"]["dark_one"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            radius=8,
            font_family=self.settings["font"]["family"],
            title_size=self.settings["font"]["title_size"],
            is_custom_title_bar=self.settings["custom_title_bar"]
        )
        self.title_bar_layout.addWidget(self.title_bar)
        # ADD CONTENT AREA
        # ///////////////////////////////////////////////////////////////
        self.content_area_frame = QFrame()
        # CREATE LAYOUT
        self.content_area_layout = QHBoxLayout(self.content_area_frame)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(0)

        self.content_area_layout.addWidget(self.login_frame)

        self.app_layout.addWidget(self.title_bar_frame)
        self.app_layout.addWidget(self.content_area_frame)
        # ///////////////////////////////////////////////////////////////
        # WINDOW
        # ///////////////////////////////////////////////////////////////

        # ADD WIDGETS TO "PyWindow"
        # ///////////////////////////////////////////////////////////////
        self.window.layout.addWidget(self.app_frame)

        # ADD CENTRAL WIDGET AND SET CONTENT MARGINS
        # ///////////////////////////////////////////////////////////////
        MainWindow.setCentralWidget(self.central_widget)
