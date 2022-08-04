# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import getpass
import shutil
import time

from gui.core.history_page_functions import HistoryPageFunctions
from gui.core.inference_page_functions import InferencePageFunctions
from gui.core.json_settings import Settings
from gui.core.right_column_functions import RightColumnFunctions
from gui.core.training_page_functions import TrainingPageFunctions
from gui.uis.windows.main_window.functions_main_window import *
import os

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from util.common_function import *
from gui.core.add_images_functions import AddImagesFunctions
from gui.core.home_page_functions import HomePageFunctions

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *


# PY WINDOW
# ///////////////////////////////////////////////////////////////
from util.draw_best_model_hist import draw_best_model_hist


class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "主页",
            "btn_tooltip": "主页",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_inference.svg",
            "btn_id": "btn_inference",
            "btn_text": "谱图检测",
            "btn_tooltip": "谱图检测",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_history.svg",
            "btn_id": "btn_history",
            "btn_text": "历史记录",
            "btn_tooltip": "历史记录",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_add.svg",
            "btn_id": "btn_add_images",
            "btn_text": "新增谱图",
            "btn_tooltip": "新增谱图",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_train.svg",
            "btn_id": "btn_training",
            "btn_text": "训练模型",
            "btn_tooltip": "训练模型",
            "show_top": True,
            "is_active": False
        }
    ]

    # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon": "user.svg",
            "btn_id": "btn_user",
            "btn_tooltip": "修改密码",
            "is_active": False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        # 暂时将主页设置为main，等待集成或优化的时候恢复为login页面
        MainFunctions.set_page(self, self.ui.load_pages.page_home)
        MainFunctions.set_left_column_menu(
            self,
            menu=self.ui.left_column.menus.menu_1,
            title="Settings Left Column",
            icon_path=Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # ///////////////////////////////////////////////////////////////
        # 读取默认设置参数
        # ///////////////////////////////////////////////////////////////
        self.training_default_info = load_json_file("training_info.json")

        # RIGHT COLUMN
        # ///////////////////////////////////////////////////////////////
        right_column_functions = RightColumnFunctions(self)
        user_info = right_column_functions.user_info
        right_column_title_label = QLabel()
        right_column_title_label.setText('修改密码')
        right_column_title_label.setAlignment(Qt.AlignCenter)
        right_column_title_label.setStyleSheet(
            'color: white;'
            'font: bold 20px 微软雅黑'
        )

        username_label = QLabel()
        username_label.setText('用户名：')
        username_label.setAlignment(Qt.AlignCenter)

        self.username_line_edit = PyLineEdit(
            text=user_info['username'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.username_line_edit.setMinimumHeight(30)

        old_password_label = QLabel()
        old_password_label.setText('旧密码：')
        old_password_label.setAlignment(Qt.AlignCenter)

        self.old_password_line_edit = PyLineEdit(
            text='',
            place_holder_text="请输入旧密码",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.old_password_line_edit.setEchoMode(QLineEdit.Password)
        self.old_password_line_edit.setMinimumHeight(30)

        new_password_label = QLabel()
        new_password_label.setText('新密码：')
        new_password_label.setAlignment(Qt.AlignCenter)

        self.new_password_line_edit = PyLineEdit(
            text='',
            place_holder_text="请输入新密码",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.new_password_line_edit.setEchoMode(QLineEdit.Password)
        self.new_password_line_edit.setMinimumHeight(30)

        check_new_password_label = QLabel()
        check_new_password_label.setText('新密码：')
        check_new_password_label.setAlignment(Qt.AlignCenter)

        self.check_new_password_line_edit = PyLineEdit(
            text='',
            place_holder_text="确认密码",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.check_new_password_line_edit.setEchoMode(QLineEdit.Password)
        self.check_new_password_line_edit.setMinimumHeight(30)

        self.user_info_btn_frame = QFrame()
        self.user_info_btn_frame.setContentsMargins(0, 0, 0, 0)
        self.user_info_btn_layout = QHBoxLayout(self.user_info_btn_frame)
        self.user_info_btn_layout.setSpacing(20)

        user_info_enter_btn = PyPushButton(
            text="确定",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        user_info_enter_btn.setMinimumHeight(40)

        user_info_cancel_btn = PyPushButton(
            text="取消",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        user_info_cancel_btn.setMinimumHeight(40)

        user_info_enter_btn.clicked.connect(lambda: right_column_functions.check_data())
        user_info_cancel_btn.clicked.connect(lambda: right_column_functions.cancel())

        self.user_info_btn_layout.addWidget(user_info_enter_btn)
        self.user_info_btn_layout.addWidget(user_info_cancel_btn)

        self.exit_btn = PyPushButton(
            text="退出登录",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color="#DF0101",
            bg_color_hover="#8A0808",
            bg_color_pressed="#B40404"
        )
        self.exit_btn.setMinimumHeight(40)
        self.exit_btn.clicked.connect(self.exit)

        self.ui.right_column.user_info_grid.addWidget(right_column_title_label, 0, 0, 1, 2)
        self.ui.right_column.user_info_grid.addWidget(username_label, 1, 0, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(self.username_line_edit, 1, 1, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(old_password_label, 2, 0, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(self.old_password_line_edit, 2, 1, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(new_password_label, 3, 0, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(self.new_password_line_edit, 3, 1, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(check_new_password_label, 4, 0, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(self.check_new_password_line_edit, 4, 1, Qt.AlignCenter)
        self.ui.right_column.user_info_grid.addWidget(self.user_info_btn_frame, 5, 0, 1, 2)

        self.ui.right_column.user_info_grid.setColumnStretch(0, 1)
        self.ui.right_column.user_info_grid.setColumnStretch(1, 2)

        self.ui.right_column.space_layout.addWidget(self.exit_btn)
        self.ui.right_column.space_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.right_column.space_layout.setAlignment(Qt.AlignBottom)

        # ///////////////////////////////////////////////////////////////
        # PAGE MAIN
        # ///////////////////////////////////////////////////////////////

        home_page_functions = HomePageFunctions(setup_main_window=self)

        self.ui.load_pages.page_home_layout.setStretch(0, 1)
        self.ui.load_pages.page_home_layout.setStretch(1, 2)

        # ///////////////////////////////////////////////////////////////
        # 每个模型的best
        # ///////////////////////////////////////////////////////////////

        draw_best_model_hist(best_model_json_path="best_model.json", pic_save_dir="images")

        self.best_model_pic = QLabel("best_model_pic")
        self.best_model_pic.setPixmap(QPixmap("images/best_model_hist.png"))
        self.best_model_pic.setScaledContents(True)
        self.ui.load_pages.best_model_layout.addWidget(self.best_model_pic)

        self.best_model_info = load_json_file("best_model.json")

        self.best_model_path_grid = QGridLayout()
        self.best_model_path_grid.setContentsMargins(0,50,50,50)
        self.best_model_path_grid.setSpacing(0)

        self.best_model_path_title = QLabel("最佳模型路径")
        self.best_model_path_title.setStyleSheet("font:bold;font-size:16px;")
        self.best_model_path_grid.addWidget(self.best_model_path_title, 0, 0, 1, 2)

        self.best_afm_path_title = QLabel("AFM: ")
        self.best_afm_path_title.setStyleSheet("font-size:14px;")
        self.best_afm_path = QLabel(self.best_model_info["afm_model"]["best_model_path"])
        self.best_model_path_grid.addWidget(self.best_afm_path_title, 1, 0)
        self.best_model_path_grid.addWidget(self.best_afm_path, 1, 1)

        self.best_sem_path_title = QLabel("SEM: ")
        self.best_sem_path_title.setStyleSheet("font-size:14px;")
        self.best_sem_path = QLabel(self.best_model_info["sem_model"]["best_model_path"])
        self.best_model_path_grid.addWidget(self.best_sem_path_title, 2, 0)
        self.best_model_path_grid.addWidget(self.best_sem_path, 2, 1)

        self.best_saxs_path_title = QLabel("SAXS: ")
        self.best_saxs_path_title.setStyleSheet("font-size:14px;")
        self.best_saxs_path = QLabel(self.best_model_info["saxs_model"]["best_model_path"])
        self.best_model_path_grid.addWidget(self.best_saxs_path_title, 3, 0)
        self.best_model_path_grid.addWidget(self.best_saxs_path, 3, 1)

        self.best_waxd_path_title = QLabel("WAXD: ")
        self.best_waxd_path_title.setStyleSheet("font-size:14px;")
        self.best_waxd_path = QLabel(self.best_model_info["waxd_model"]["best_model_path"])
        self.best_model_path_grid.addWidget(self.best_waxd_path_title, 4, 0)
        self.best_model_path_grid.addWidget(self.best_waxd_path, 4, 1)

        self.best_model_path_grid.setColumnStretch(1,1)

        self.ui.load_pages.best_model_layout.addLayout(self.best_model_path_grid)

        # ///////////////////////////////////////////////////////////////
        # 功能区按钮
        # ///////////////////////////////////////////////////////////////
        self.ui.load_pages.page_home_row_1_layout.setStretch(1,1)

        self.to_page_detection_btn = PyPushButton(
            text="谱图\n检测",
            radius="60px",
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.to_page_detection_btn.setMinimumHeight(120)
        self.to_page_detection_btn.setMinimumWidth(120)
        self.to_page_detection_btn.setMaximumWidth(120)
        self.to_page_detection_btn.setStyleSheet(self.to_page_detection_btn.styleSheet()+"QPushButton{font:bold 16px 'Microsoft YaHei UI';color:white;}")
        self.ui.load_pages.main_func_layout.addWidget(self.to_page_detection_btn, 0, 0)
        self.to_page_detection_btn.clicked.connect(lambda : home_page_functions.to_page_inference(self.inference_page_functions))

        self.to_page_history_btn = PyPushButton(
            text="历史\n记录",
            radius="60px",
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.to_page_history_btn.setMinimumHeight(120)
        self.to_page_history_btn.setMinimumWidth(120)
        self.to_page_history_btn.setMaximumWidth(120)
        self.to_page_history_btn.setStyleSheet(
            self.to_page_history_btn.styleSheet() + "QPushButton{font:bold 16px 'Microsoft YaHei UI';color:white;}")
        self.ui.load_pages.main_func_layout.addWidget(self.to_page_history_btn, 0, 1)
        self.to_page_history_btn.clicked.connect(lambda : home_page_functions.to_page_history(self.history_page_functions))

        self.to_page_add_images_btn = PyPushButton(
            text="新增\n谱图",
            radius="60px",
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.to_page_add_images_btn.setMinimumHeight(120)
        self.to_page_add_images_btn.setMinimumWidth(120)
        self.to_page_add_images_btn.setMaximumWidth(120)
        self.to_page_add_images_btn.setStyleSheet(
            self.to_page_add_images_btn.styleSheet() + "QPushButton{font:bold 16px 'Microsoft YaHei UI';color:white;}")
        self.ui.load_pages.main_func_layout.addWidget(self.to_page_add_images_btn, 0, 3)

        self.to_page_add_images_btn.clicked.connect(lambda: home_page_functions.to_page_add_images())

        self.to_page_train_btn = PyPushButton(
            text="训练\n模型",
            radius="60px",
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.to_page_train_btn.setMinimumHeight(120)
        self.to_page_train_btn.setMinimumWidth(120)
        self.to_page_train_btn.setMaximumWidth(120)
        self.to_page_train_btn.setStyleSheet(
            self.to_page_train_btn.styleSheet() + "QPushButton{font:bold 16px 'Microsoft YaHei UI';color:white;}")
        self.ui.load_pages.main_func_layout.addWidget(self.to_page_train_btn, 1, 0)

        self.to_page_train_btn.clicked.connect(lambda: home_page_functions.to_page_train())

        self.to_page_personal_btn = PyPushButton(
            text="个人\n中心",
            radius="60px",
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.to_page_personal_btn.setMinimumHeight(120)
        self.to_page_personal_btn.setMinimumWidth(120)
        self.to_page_personal_btn.setMaximumWidth(120)
        self.to_page_personal_btn.setStyleSheet(
            self.to_page_personal_btn.styleSheet() + "QPushButton{font:bold 16px 'Microsoft YaHei UI';color:white;}")
        self.ui.load_pages.main_func_layout.addWidget(self.to_page_personal_btn, 1, 1)

        self.to_page_personal_btn.clicked.connect(lambda : home_page_functions.open_user_info())

        self.ui.load_pages.main_func_frame.setStyleSheet(
            "background:{}".format(self.themes["app_color"]["text_description"]))
        self.ui.load_pages.best_model_frame.setStyleSheet(
            "background:{}".format(self.themes["app_color"]["text_description"]))
        # self.ui.load_pages.metric_frame.setStyleSheet(
        #     "background:{}".format(self.themes["app_color"]["text_description"]))
        self.ui.load_pages.dataset_info_frame.setStyleSheet(
            "background:{}".format(self.themes["app_color"]["text_description"]))


        self.ui.load_pages.metric_frame.setMinimumWidth(500)  # 临时宽度

        # ///////////////////////////////////////////////////////////////
        # 指标图（loss and acc）
        # ///////////////////////////////////////////////////////////////

        home_tab = PyTabMetric()
        home_tab.setStyleSheet(
            "QTabWidget {border-top-color: rgba(255, 255, 255, 0);}"
            "QTabWidget::pane{top:-1px;}"
            "QTabBar::tab {"
            "min-width:100px;"
            "color: #8a95aa;"
            "background-color: #1e2229;"
            "border: 2px solid #1b1e23;"
            "border-top-left-radius: 10px;"
            "border-top-right-radius: 10px;padding:5px;"
            "padding-right: 5px;"
            "}"
            "QTabBar::tab:!selected {margin-top: 5px;} "
            "QTabBar::tab:selected {color: #568af2;}; "
        )
        self.ui.load_pages.home_metric_layout.addWidget(home_tab)


        # ///////////////////////////////////////////////////////////////
        # 数据集信息
        # ///////////////////////////////////////////////////////////////

        self.dataset_dir = "./data"

        self.dataset_table = PyTableWidget(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["context_color"],
            bg_color=self.themes["app_color"]["bg_two"],
            header_horizontal_color=self.themes["app_color"]["dark_two"],
            header_vertical_color=self.themes["app_color"]["bg_three"],
            bottom_line_color=self.themes["app_color"]["bg_three"],
            grid_line_color=self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color=self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color=self.themes["app_color"]["dark_four"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.dataset_table.setColumnCount(7)
        self.dataset_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dataset_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.dataset_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dataset_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dataset_table.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Columns / Header
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("谱图类型")

        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("使用类型")

        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("年份")

        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("谱图数量")

        self.column_5 = QTableWidgetItem()
        self.column_5.setTextAlignment(Qt.AlignCenter)
        self.column_5.setText("数据集\n内部路径")

        self.column_6 = QTableWidgetItem()
        self.column_6.setTextAlignment(Qt.AlignCenter)
        self.column_6.setText("不同使用类型下\n谱图数量")

        self.column_7 = QTableWidgetItem()
        self.column_7.setTextAlignment(Qt.AlignCenter)
        self.column_7.setText("谱图总数")

        # Set column
        self.dataset_table.setHorizontalHeaderItem(0, self.column_1)
        self.dataset_table.setHorizontalHeaderItem(1, self.column_2)
        self.dataset_table.setHorizontalHeaderItem(2, self.column_3)
        self.dataset_table.setHorizontalHeaderItem(3, self.column_4)
        self.dataset_table.setHorizontalHeaderItem(4, self.column_5)
        self.dataset_table.setHorizontalHeaderItem(5, self.column_6)
        self.dataset_table.setHorizontalHeaderItem(6, self.column_7)

        home_page_functions.load_dataset_info(self.dataset_dir)
        self.dataset_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dataset_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 还是设置成单选比较好看
        # 设置选取模式，一次选择一行
        self.dataset_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        # 设置表头在选中时不会高亮显示
        self.dataset_table.horizontalHeader().setHighlightSections(False)

        self.change_dataset_layout = QHBoxLayout()
        self.dataset_dir_label = QLabel("当前数据集路径:")
        self.dataset_dir_label.setStyleSheet("font:bold;font-size:14px;")
        self.dataset_dir_edit = PyLineEdit()
        self.dataset_dir_edit.setMinimumHeight(30)
        self.dataset_dir_edit.setText(self.dataset_dir)
        self.dataset_dir_edit.setReadOnly(True)
        self.choose_dataset_dir_btn = PyPushButton(
            text="更换",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.choose_dataset_dir_btn.setMinimumHeight(30)
        self.choose_dataset_dir_btn.setMinimumWidth(50)

        self.choose_dataset_dir_btn.clicked.connect(lambda: home_page_functions.choose_dataset())

        self.change_dataset_layout.addWidget(self.dataset_dir_label)
        self.change_dataset_layout.addWidget(self.dataset_dir_edit)
        self.change_dataset_layout.addWidget(self.choose_dataset_dir_btn)
        self.ui.load_pages.dataset_info_layout.addLayout(self.change_dataset_layout)
        self.ui.load_pages.dataset_info_layout.addWidget(self.dataset_table)

        # /////////////////////////////////////////////////////////////////////
        # INFERENCE PAGE
        # /////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////
        self.inference_page_functions = InferencePageFunctions(self)
        # 上半部分
        # 选择图片
        self.choose_img_btn = PyIconButton(
            icon_path=Functions.set_svg_icon("new_add.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="选择图片",
            width=150,
            height=180,
            radius=20,
            dark_one=self.themes["app_color"]["dark_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_active"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["green"]
        )

        self.choose_img_btn.clicked.connect(lambda: self.inference_page_functions.get_img_path())

        # /////////////////////////////////////////////////////////////////////
        # 下半部分
        # 从model_path.json获取路径
        model_path = self.inference_page_functions.get_path()
        label_1 = QLabel()
        label_1.setText('谱图存储路径：')
        label_1.setAlignment(Qt.AlignVCenter)
        label_1.setMaximumSize(120, 40)
        self.inference_result_path = PyLineEdit(
            text=model_path['inference_result_path'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.inference_result_path.setMaximumHeight(40)
        self.inference_result_path.setReadOnly(True)
        input_btn_1 = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        input_btn_1.setMaximumSize(100, 40)

        label_2 = QLabel()
        label_2.setText('AFM模型路径：')
        label_2.setAlignment(Qt.AlignVCenter)
        label_2.setMaximumSize(120, 40)
        self.afm_model_path = PyLineEdit(
            text=model_path['afm_model_path'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.afm_model_path.setMaximumHeight(40)
        self.afm_model_path.setReadOnly(True)
        input_btn_2 = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        input_btn_2.setMaximumSize(100, 40)

        label_3 = QLabel()
        label_3.setText('SEM模型路径：')
        label_3.setAlignment(Qt.AlignVCenter)
        label_3.setMaximumSize(120, 40)
        self.sem_model_path = PyLineEdit(
            text=model_path['sem_model_path'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.sem_model_path.setMaximumHeight(40)
        self.sem_model_path.setReadOnly(True)
        input_btn_3 = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        input_btn_3.setMaximumSize(100, 40)

        label_4 = QLabel()
        label_4.setText('2D-SAXS模型路径：')
        label_4.setAlignment(Qt.AlignVCenter)
        label_4.setMaximumSize(120, 40)
        self.saxs_model_path = PyLineEdit(
            text=model_path['saxs_model_path'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.saxs_model_path.setMaximumHeight(40)
        self.saxs_model_path.setReadOnly(True)
        input_btn_4 = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        input_btn_4.setMaximumSize(100, 40)

        label_5 = QLabel()
        label_5.setText('2D-WAXD模型路径：')
        label_5.setAlignment(Qt.AlignVCenter)
        label_5.setMaximumSize(120, 40)
        self.waxd_model_path = PyLineEdit(
            text=model_path['waxd_model_path'],
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.waxd_model_path.setMaximumHeight(40)
        self.waxd_model_path.setReadOnly(True)
        input_btn_5 = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        input_btn_5.setMaximumSize(100, 40)

        self.check_btn = PyPushButton(
            text="开始检测",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["darkgreen_one"],
            bg_color_hover=self.themes["app_color"]["darkgreen_two"],
            bg_color_pressed=self.themes["app_color"]["green"]
        )
        self.check_btn.setMaximumSize(300, 40)
        self.check_btn.setMinimumSize(200, 40)

        input_btn_1.clicked.connect(lambda: self.inference_page_functions.choose_data_path(self.inference_result_path))
        input_btn_2.clicked.connect(lambda: self.inference_page_functions.choose_model(self.afm_model_path))
        input_btn_3.clicked.connect(lambda: self.inference_page_functions.choose_model(self.sem_model_path))
        input_btn_4.clicked.connect(lambda: self.inference_page_functions.choose_model(self.saxs_model_path))
        input_btn_5.clicked.connect(lambda: self.inference_page_functions.choose_model(self.waxd_model_path))
        self.check_btn.clicked.connect(lambda: self.inference_page_functions.check())

        self.ui.load_pages.model_path_layout.setAlignment(Qt.AlignCenter)
        self.ui.load_pages.model_path_layout.addWidget(label_1, 0, 0)
        self.ui.load_pages.model_path_layout.addWidget(self.inference_result_path, 0, 1)
        self.ui.load_pages.model_path_layout.addWidget(input_btn_1, 0, 2)
        self.ui.load_pages.model_path_layout.addWidget(label_2, 1, 0)
        self.ui.load_pages.model_path_layout.addWidget(self.afm_model_path, 1, 1)
        self.ui.load_pages.model_path_layout.addWidget(input_btn_2, 1, 2)
        self.ui.load_pages.model_path_layout.addWidget(label_3, 2, 0)
        self.ui.load_pages.model_path_layout.addWidget(self.sem_model_path, 2, 1)
        self.ui.load_pages.model_path_layout.addWidget(input_btn_3, 2, 2)
        self.ui.load_pages.model_path_layout.addWidget(label_4, 3, 0)
        self.ui.load_pages.model_path_layout.addWidget(self.saxs_model_path, 3, 1)
        self.ui.load_pages.model_path_layout.addWidget(input_btn_4, 3, 2)
        self.ui.load_pages.model_path_layout.addWidget(label_5, 4, 0)
        self.ui.load_pages.model_path_layout.addWidget(self.waxd_model_path, 4, 1)
        self.ui.load_pages.model_path_layout.addWidget(input_btn_5, 4, 2)
        self.ui.load_pages.model_path_layout.addWidget(self.check_btn, 5, 1, alignment=Qt.AlignCenter)
        self.ui.load_pages.model_path_layout.setColumnStretch(0, 1)
        self.ui.load_pages.model_path_layout.setColumnStretch(1, 3)
        self.ui.load_pages.model_path_layout.setColumnStretch(2, 1)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(0, 40)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(1, 40)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(2, 40)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(3, 40)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(4, 40)
        self.ui.load_pages.model_path_layout.setRowMinimumHeight(5, 60)
        self.ui.load_pages.model_path_layout.setHorizontalSpacing(10)
        self.ui.load_pages.model_path_layout.setVerticalSpacing(10)
        self.ui.load_pages.model_path_layout.setContentsMargins(200, 0, 200, 0)
        # self.ui.load_pages.model_path_layout.set
        # 添加widgets
        self.ui.load_pages.inference_layout.addWidget(self.choose_img_btn)

        # /////////////////////////////////////////////////////////////////////
        # INFERENCE PAGE
        # /////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////
        # INFERENCE PAGE 2
        # /////////////////////////////////////////////////////////////////////
        # 从随便那读取后生成

        # /////////////////////////////////////////////////////////////////////
        # INFERENCE PAGE 2
        # /////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////
        # HISTORY PAGE
        # /////////////////////////////////////////////////////////////////////

        # 历史记录表格
        self.history_table = PyTableWidget(
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["context_color"],
            bg_color=self.themes["app_color"]["bg_two"],
            header_horizontal_color=self.themes["app_color"]["dark_two"],
            header_vertical_color=self.themes["app_color"]["bg_three"],
            bottom_line_color=self.themes["app_color"]["bg_three"],
            grid_line_color=self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color=self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color=self.themes["app_color"]["dark_four"],
            context_color=self.themes["app_color"]["context_color"]
        )

        # 表格属性设置
        # 设置行列数
        self.history_table.setRowCount(7)
        self.history_table.setColumnCount(5)
        # 设置自适应列宽
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置单元格不可编辑
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置多选，和setSelectionBehavior组合起来可以选取多行
        # self.history_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 还是设置成单选比较好看
        # 设置选取模式，一次选择一行
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置自适应行高
        self.history_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏滚动条
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 禁用滚动条
        self.history_table.verticalScrollBar().setDisabled(True)

        # 表格头部
        # 表格头部可以用一下一行实现
        self.history_table.setHorizontalHeaderLabels(["谱图", "谱图类型", "检测时间", "检测结果", "查看详情"])
        # 设置表头在选中时不会高亮显示
        self.history_table.horizontalHeader().setHighlightSections(False)

        # /////////////////////////////////////////////////////////////////////
        # 数据操作
        # /////////////////////////////////////////////////////////////////////
        self.history_page_functions = HistoryPageFunctions(self, 'history.db')
        # 添加表格内容 初始内容查询数据库最新7条数据
        data = self.history_page_functions.init_data
        for d in data:
            row_number = self.history_table.rowCount()
            self.history_table.insertRow(row_number)  # Insert row
            # 所有内容设置居中
            col_img = QLabel()
            col_img.setPixmap(QPixmap(d[1]))
            col_img.setMaximumSize(100, 100)
            col_img.setScaledContents(True)
            img_layout = QHBoxLayout()
            img_layout.addWidget(col_img)
            img_layout.setAlignment(col_img, Qt.AlignCenter)
            img_widget = QWidget()
            img_widget.setLayout(img_layout)

            col_2 = QTableWidgetItem(d[2])
            col_2.setTextAlignment(Qt.AlignCenter)
            col_3 = QTableWidgetItem(d[3])
            col_3.setTextAlignment(Qt.AlignCenter)
            col_4 = QTableWidgetItem(d[4])
            col_4.setTextAlignment(Qt.AlignCenter)
            col_btn = PyPushButton(
                text="查看",
                radius=8,
                color=self.themes["app_color"]["text_foreground"],
                bg_color=self.themes["app_color"]["dark_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["blue"]
            )
            col_btn.setFixedSize(100, 40)

            btn_layout = QHBoxLayout()
            btn_layout.addWidget(col_btn)
            btn_layout.setAlignment(col_btn, Qt.AlignCenter)
            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)

            self.history_table.setCellWidget(row_number, 0, img_widget)  # Add
            self.history_table.setItem(row_number, 1, col_2)  # Add
            self.history_table.setItem(row_number, 2, col_3)  # Add
            self.history_table.setItem(row_number, 3, col_4)  # Add
            self.history_table.setCellWidget(row_number, 4, btn_widget)  # Add

        # 页面翻转按钮
        turn_page_left_btn = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_arrow_left.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="上一页",
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
            bg_color_pressed=self.themes["app_color"]["blue"]
        )

        # 当前页面Label
        self.page_label = QLabel(None)
        self.page_label.setText(f'第 {self.history_page_functions.current}/{self.history_page_functions.max_page_num} 页')
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setMaximumWidth(100)

        turn_page_right_btn = PyIconButton(
            icon_path=Functions.set_svg_icon("icon_arrow_right.svg"),
            parent=self,
            app_parent=self.ui.central_widget,
            tooltip_text="下一页",
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
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        # 跳转输入框
        jump_line_edit = PyLineEdit(
            text="",
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        jump_line_edit.setAlignment(Qt.AlignHCenter)
        # 根据数据库里数据的数量设置最大输入长度
        jump_line_edit.setMaxLength(len(str(self.history_page_functions.max_page_num)))
        jump_line_edit.setMinimumHeight(30)
        jump_line_edit.setMaximumWidth(50)

        jump_page_btn = PyPushButton(
            text="跳转",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["blue"]
        )
        jump_page_btn.setMaximumHeight(40)
        jump_page_btn.setMaximumWidth(60)

        # 翻页功能
        turn_page_right_btn.clicked.connect(
            lambda: self.history_page_functions.next_page(self.history_table, self.page_label))
        turn_page_left_btn.clicked.connect(
            lambda: self.history_page_functions.pre_page(self.history_table, self.page_label))
        # 跳转功能
        jump_page_btn.clicked.connect(
            lambda: self.history_page_functions.jump_to(self.history_table, self.page_label, jump_line_edit))
        # 回车响应跳转功能
        jump_line_edit.returnPressed.connect(
            lambda: self.history_page_functions.jump_to(self.history_table, self.page_label, jump_line_edit))

        # 添加widgets到页面中
        self.ui.load_pages.table_layout.addWidget(self.history_table)
        self.ui.load_pages.turn_page_btn_layout.addWidget(turn_page_left_btn)
        self.ui.load_pages.turn_page_btn_layout.addWidget(self.page_label)
        self.ui.load_pages.turn_page_btn_layout.addWidget(turn_page_right_btn)
        self.ui.load_pages.turn_page_btn_layout.addWidget(jump_line_edit)
        self.ui.load_pages.turn_page_btn_layout.addWidget(jump_page_btn)

        # /////////////////////////////////////////////////////////////////////
        # HISTORY PAGE
        # /////////////////////////////////////////////////////////////////////

        # /////////////////////////////////////////////////////////////////////
        # HISTORY PAGE 2
        # /////////////////////////////////////////////////////////////////////
        # 从HISTORY数据库中读取后生成

        # /////////////////////////////////////////////////////////////////////
        # HISTORY PAGE 2
        # /////////////////////////////////////////////////////////////////////



        # ///////////////////////////////////////////////////////////////
        # PAGE ADD IMAGES
        # ///////////////////////////////////////////////////////////////

        add_images_functions = AddImagesFunctions(_setup_main_window=self)

        self.data_type_label = QLabel(
            text="谱图类型:"
        )
        self.data_type_label.setStyleSheet("font:16px")
        self.data_type_afm = QRadioButton("AFM")
        self.data_type_afm.setChecked(True)
        self.data_type_afm.setStyleSheet("font:16px")
        self.data_type_sem = QRadioButton("SEM")
        self.data_type_sem.setStyleSheet("font:16px")
        self.data_type_saxs = QRadioButton("2D-SAXS")
        self.data_type_saxs.setStyleSheet("font:16px")
        self.data_type_waxd = QRadioButton("2D-WAXD")
        self.data_type_waxd.setStyleSheet("font:16px")

        self.data_year_label = QLabel(
            text="谱图年份:"
        )
        self.data_year_label.setStyleSheet("font:16px")
        self.data_year_edit = PyLineEdit()
        self.data_year_edit.setMinimumHeight(50)
        self.data_year_edit.setText(str(0))

        self.data_save_dir_label = QLabel(
            text="谱图保存路径:"
        )
        self.data_save_dir_label.setStyleSheet("font:16px")
        self.data_save_dir_edit = PyLineEdit()
        self.data_save_dir_edit.setText("./data")
        self.data_save_dir_edit.setMinimumHeight(50)
        self.choose_save_dir_btn = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.choose_save_dir_btn.setMinimumHeight(50)
        self.choose_save_dir_btn.setMinimumWidth(80)
        self.choose_save_dir_btn.setMaximumWidth(80)

        self.choose_save_dir_btn.clicked.connect(lambda: add_images_functions.choose_save_dir())

        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_type_label, 0, 0, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_type_afm, 0, 2, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_type_sem, 0, 4, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_type_saxs, 0, 6, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_type_waxd, 0, 8, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_year_label, 1, 0, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_year_edit, 1, 2, 1, 12)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_save_dir_label, 2, 0, 1, 2)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.data_save_dir_edit, 2, 2, 1, 12)
        self.ui.load_pages.add_images_grid_layout.addWidget(self.choose_save_dir_btn, 2, 14, 1, 2)
        self.ui.load_pages.add_images_grid_layout.setVerticalSpacing(20)  # 设置网格内部每个格子之间的垂直间距
        self.ui.load_pages.add_images_grid_layout.setHorizontalSpacing(10)
        self.ui.load_pages.add_images_grid_layout.setContentsMargins(200, 0, 200, 0)

        self.add_image_btn = PyPushButton(
            text="",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.add_image_btn.setMinimumHeight(60)
        self.add_image_btn.setMinimumWidth(100)
        self.add_image_btn.setMaximumHeight(60)
        self.add_image_btn.setMaximumWidth(100)
        self.add_image_btn.setIcon(QIcon("./qt_images/iconmonstr-plus-6-240.png"))
        self.add_image_btn.setIconSize(QSize(40, 40))

        self.add_image_btn.clicked.connect(lambda: add_images_functions.load_multiple_images())

        self.ui.load_pages.add_images_grid_layout.addWidget(self.add_image_btn, 3 + 0, 0 * 2, 1, 2,
                                                            Qt.AlignLeft | Qt.AlignTop)


        self.back_btn_in_add_page = PyPushButton(
            text="返回",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.back_btn_in_add_page.setMinimumHeight(50)
        self.back_btn_in_add_page.setMinimumWidth(80)
        self.back_btn_in_add_page.setMaximumHeight(50)
        self.back_btn_in_add_page.setMaximumWidth(80)
        self.back_btn_in_add_page.clicked.connect(lambda: add_images_functions.back_to_main_page_in_add_page())

        self.upload_images_btn = PyPushButton(
            text="上传",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.upload_images_btn.setMinimumHeight(50)
        self.upload_images_btn.setMinimumWidth(80)
        self.upload_images_btn.setMaximumHeight(50)
        self.upload_images_btn.setMaximumWidth(80)
        self.upload_images_btn.clicked.connect(lambda: add_images_functions.upload_images(_home_page_functions=home_page_functions))
        self.ui.load_pages.add_btn_layout.addStretch(1)
        self.ui.load_pages.add_btn_layout.setSpacing(20)
        self.ui.load_pages.add_btn_layout.setContentsMargins(0, 0, 20, 0)
        self.ui.load_pages.add_btn_layout.addWidget(self.back_btn_in_add_page)
        self.ui.load_pages.add_btn_layout.addWidget(self.upload_images_btn)

        # ///////////////////////////////////////////////////////////////
        # PAGE TRAIN BASE SETTING
        # ///////////////////////////////////////////////////////////////
        training_page_functions = TrainingPageFunctions(_setup_main_window=self)

        self.training_data_type_label = QLabel(
            text="谱图类型:"
        )
        self.training_data_type_label.setStyleSheet("font:16px")
        self.training_data_type_label.setMinimumHeight(50)
        self.training_data_type_afm = QRadioButton("AFM")
        self.training_data_type_afm.setChecked(True)
        self.training_data_type_afm.setStyleSheet("font:16px")
        self.training_data_type_sem = QRadioButton("SEM")
        self.training_data_type_sem.setStyleSheet("font:16px")
        self.training_data_type_saxs = QRadioButton("2D-SAXS")
        self.training_data_type_saxs.setStyleSheet("font:16px")
        self.training_data_type_waxd = QRadioButton("2D-WAXD")
        self.training_data_type_waxd.setStyleSheet("font:16px")

        self.training_data_type_afm.toggled.connect(
            lambda: training_page_functions.change_dataset_dir_by_data_type(self.training_data_type_afm, "AFM"))
        self.training_data_type_sem.toggled.connect(
            lambda: training_page_functions.change_dataset_dir_by_data_type(self.training_data_type_sem, "SEM"))
        self.training_data_type_saxs.toggled.connect(
            lambda: training_page_functions.change_dataset_dir_by_data_type(self.training_data_type_saxs, "SAXS"))
        self.training_data_type_waxd.toggled.connect(
            lambda: training_page_functions.change_dataset_dir_by_data_type(self.training_data_type_waxd, "WAXD"))

        self.training_data_dir_label = QLabel(
            text="数据集路径:"
        )
        self.training_data_dir_label.setStyleSheet("font:16px")
        self.training_data_dir_label.setMinimumHeight(50)
        self.training_data_dir_edit = PyLineEdit()
        self.training_data_dir_edit.setText(training_page_functions.get_training_data_dir_by_data_type("AFM"))
        self.training_data_dir_edit.setMinimumHeight(50)
        self.choose_training_data_dir_btn = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.choose_training_data_dir_btn.setMinimumHeight(50)
        self.choose_training_data_dir_btn.setMinimumWidth(80)
        self.choose_training_data_dir_btn.setMaximumWidth(80)

        self.is_split_test_set_label = QLabel("是否划分测试集:")
        self.is_split_test_set_label.setStyleSheet("font:16px")
        self.is_split_test_set_label.setMinimumHeight(50)
        self.is_split_test_set_toggle = PyToggle(
            width=50,
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["context_color"]
        )

        self.is_split_test_set_toggle.stateChanged.connect(lambda: training_page_functions.is_split_out_change())

        self.split_out_rate_label = QLabel("划出比例:")
        self.split_out_rate_label.setStyleSheet("font:16px")
        self.split_out_rate_edit = PyLineEdit()
        self.split_out_rate_edit.setText(str(self.training_default_info["test_set_rate"]))
        self.split_out_rate_edit.setMinimumHeight(50)
        self.split_out_rate_edit.setMaximumWidth(80)

        self.split_out_tip_label = QLabel("从训练集\"{}\"中\n随机划出{}%的数据\n到测试集\"{}\"中".
                                          format(training_page_functions.get_training_data_dir_by_data_type("AFM"),
                                                 self.training_default_info["test_set_rate"] * 100,
                                                 training_page_functions.get_split_out_test_dir(
                                                     training_page_functions.get_training_data_dir_by_data_type("AFM"))))
        self.split_out_tip_label.setStyleSheet("font:12px")

        self.choose_training_data_dir_btn.clicked.connect(lambda: training_page_functions.choose_training_data_dir())

        self.model_save_dir_label = QLabel(
            text="模型保存路径:"
        )
        self.model_save_dir_label.setStyleSheet("font:16px")
        self.model_save_dir_label.setMinimumHeight(50)
        self.model_save_dir_edit = PyLineEdit()
        self.model_save_dir_edit.setText(self.training_default_info["model_save_dir"])
        self.model_save_dir_edit.setMinimumHeight(50)
        self.choose_model_save_dir_btn = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.choose_model_save_dir_btn.setMinimumHeight(50)
        self.choose_model_save_dir_btn.setMinimumWidth(80)
        self.choose_model_save_dir_btn.setMaximumWidth(80)

        self.choose_model_save_dir_btn.clicked.connect(lambda: training_page_functions.choose_model_save_dir())

        self.split_out_rate_edit.textChanged.connect(lambda: training_page_functions.change_split_out_tip_info())
        self.training_data_dir_edit.textChanged.connect(lambda: training_page_functions.change_split_out_tip_info())

        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_type_label, 0, 0, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_type_afm, 0, 2, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_type_sem, 0, 4, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_type_saxs, 0, 6, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_type_waxd, 0, 8, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_dir_label, 1, 0, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.training_data_dir_edit, 1, 2, 1, 12)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.choose_training_data_dir_btn, 1, 14, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.is_split_test_set_label, 2, 0, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.is_split_test_set_toggle, 2, 2, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.split_out_rate_label, 2, 4, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.split_out_rate_edit, 2, 6, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.split_out_tip_label, 2, 8, 1, 8)
        self.split_out_rate_label.hide()
        self.split_out_rate_edit.hide()
        self.split_out_tip_label.hide()
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.model_save_dir_label, 3, 0, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.model_save_dir_edit, 3, 2, 1, 12)
        self.ui.load_pages.train_base_setting_grid_out.addWidget(self.choose_model_save_dir_btn, 3, 14, 1, 2)
        self.ui.load_pages.train_base_setting_grid_out.setVerticalSpacing(20)  # 设置网格内部每个格子之间的垂直间距
        self.ui.load_pages.train_base_setting_grid_out.setHorizontalSpacing(10)
        self.ui.load_pages.train_base_setting_grid_out.setContentsMargins(200, 0, 200, 0)

        self.back_btn_in_train_base_setting_page = PyPushButton(
            text="返回",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.back_btn_in_train_base_setting_page.setMinimumHeight(50)
        self.back_btn_in_train_base_setting_page.setMinimumWidth(80)
        self.back_btn_in_train_base_setting_page.setMaximumHeight(50)
        self.back_btn_in_train_base_setting_page.setMaximumWidth(80)
        self.back_btn_in_train_base_setting_page.clicked.connect(
            lambda: training_page_functions.back_in_base_setting_page())

        self.next_btn_in_train_base_setting_page = PyPushButton(
            text="下一步",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.next_btn_in_train_base_setting_page.setMinimumHeight(50)
        self.next_btn_in_train_base_setting_page.setMinimumWidth(80)
        self.next_btn_in_train_base_setting_page.setMaximumHeight(50)
        self.next_btn_in_train_base_setting_page.setMaximumWidth(80)
        self.next_btn_in_train_base_setting_page.clicked.connect(
            lambda: training_page_functions.next_in_train_base_setting_page())
        self.ui.load_pages.train_base_setting_btn_layout.addStretch(1)
        self.ui.load_pages.train_base_setting_btn_layout.setSpacing(20)
        self.ui.load_pages.train_base_setting_btn_layout.setContentsMargins(0, 0, 20, 0)
        self.ui.load_pages.train_base_setting_btn_layout.addWidget(self.back_btn_in_train_base_setting_page)
        self.ui.load_pages.train_base_setting_btn_layout.addWidget(self.next_btn_in_train_base_setting_page)

        # ///////////////////////////////////////////////////////////////
        # PAGE TRAIN NET SETTING
        # ///////////////////////////////////////////////////////////////

        # 初始化 训练相关参数
        self.epochs_label = QLabel(
            text="训练轮数:"
        )
        self.epochs_label.setStyleSheet("font:16px")
        self.epochs_edit = PyLineEdit()
        self.epochs_edit.setText(str(self.training_default_info["epochs"]))
        self.epochs_edit.setMinimumHeight(50)

        self.batchsize_label = QLabel(
            text="批大小:"
        )
        self.batchsize_label.setStyleSheet("font:16px")
        self.batchsize_edit = PyLineEdit()
        self.batchsize_edit.setText(str(self.training_default_info["batchsize"]))
        self.batchsize_edit.setMinimumHeight(50)

        self.validation_set_rate_label = QLabel(
            text="验证集比例:"
        )
        self.validation_set_rate_label.setStyleSheet("font:16px")
        self.validation_set_rate_edit = PyLineEdit()
        self.validation_set_rate_edit.setText(str(self.training_default_info["val_set_rate"]))
        self.validation_set_rate_edit.setMinimumHeight(50)

        self.learning_rate_label = QLabel(
            text="学习率:"
        )
        self.learning_rate_label.setStyleSheet("font:16px")
        self.learning_rate_edit = PyLineEdit()
        self.learning_rate_edit.setText(str(self.training_default_info["learning_rate"]))
        self.learning_rate_edit.setMinimumHeight(50)

        self.is_lr_decay_label = QLabel(
            text="是否进行学习率衰减:"
        )
        self.is_lr_decay_label.setStyleSheet("font:16px")
        self.is_lr_decay_label.setMinimumHeight(50)
        self.is_lr_decay_toggle = PyToggle(
            width=50,
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["context_color"]
        )

        self.is_lr_decay_toggle.stateChanged.connect(lambda: training_page_functions.lr_decay_change())

        self.lr_decay_rate_label = QLabel(
            text="衰减比率:"
        )
        self.lr_decay_rate_label.setStyleSheet("font:16px")
        self.lr_decay_rate_edit = PyLineEdit()
        self.lr_decay_rate_edit.setText(str(self.training_default_info["lr_decay_rate"]))
        self.lr_decay_rate_edit.setMinimumHeight(50)

        self.lr_decay_steps_label = QLabel(
            text="衰减步长:"
        )
        self.lr_decay_steps_label.setStyleSheet("font:16px")
        self.lr_decay_steps_edit = PyLineEdit()
        self.lr_decay_steps_edit.setText(str(self.training_default_info["lr_decay_steps"]))
        self.lr_decay_steps_edit.setMinimumHeight(50)

        self.is_incremental_train_label = QLabel(
            text="是否加载预训练模型:"
        )
        self.is_incremental_train_label.setStyleSheet("font:16px")
        self.is_incremental_train_label.setMinimumHeight(50)
        self.is_incremental_train_toggle = PyToggle(
            width=50,
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["context_color"]
        )

        self.is_incremental_train_toggle.stateChanged.connect(lambda: training_page_functions.incremental_train_change())

        self.pretrained_model_label = QLabel(
            text="预训练模型路径:"
        )
        self.pretrained_model_label.setStyleSheet("font:16px")
        self.pretrained_model_edit = PyLineEdit()
        self.pretrained_model_edit.setText(self.training_default_info["pretrained_afm_model_path"])
        self.pretrained_model_edit.setMinimumHeight(50)

        self.choose_pretrained_model_btn = PyPushButton(
            text="浏览",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.choose_pretrained_model_btn.setMinimumHeight(50)
        self.choose_pretrained_model_btn.setMinimumWidth(80)
        self.choose_pretrained_model_btn.setMaximumWidth(80)

        self.choose_pretrained_model_btn.clicked.connect(lambda: training_page_functions.choose_pretrained_model())

        self.dropout_rate_label = QLabel(
            text="Dropout比率:"
        )
        self.dropout_rate_label.setStyleSheet("font:16px")
        self.dropout_rate_edit = PyLineEdit()
        self.dropout_rate_edit.setText(str(self.training_default_info["dropout_rate"]))
        self.dropout_rate_edit.setMinimumHeight(50)

        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.epochs_label, 0, 0, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.epochs_edit, 0, 1, 1, 7)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.batchsize_label, 1, 0, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.batchsize_edit, 1, 1, 1, 7)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.validation_set_rate_label, 2, 0, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.validation_set_rate_edit, 2, 1, 1, 7)

        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.learning_rate_label, 3, 0, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.learning_rate_edit, 3, 1, 1, 7)

        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.is_lr_decay_label, 4, 0, 1, 3)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.is_lr_decay_toggle, 4, 3, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.lr_decay_rate_label, 4, 4, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.lr_decay_rate_edit, 4, 5, 1, 3)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.lr_decay_steps_label, 4, 9, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.lr_decay_steps_edit, 4, 10, 1, 3)
        #
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.is_incremental_train_label, 5, 0, 1, 3)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.is_incremental_train_toggle, 5, 3, 1, 3)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.pretrained_model_label, 5, 4, 1, 2)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.pretrained_model_edit, 5, 6, 1, 6)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.choose_pretrained_model_btn, 5, 12, 1, 2)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.dropout_rate_label, 5, 4, 1, 1)
        self.ui.load_pages.train_net_setting_grid_layout.addWidget(self.dropout_rate_edit, 5, 5, 1, 3)
        self.lr_decay_rate_label.hide()
        self.lr_decay_rate_edit.hide()
        self.lr_decay_steps_label.hide()
        self.lr_decay_steps_edit.hide()
        self.pretrained_model_label.hide()
        self.pretrained_model_edit.hide()
        self.choose_pretrained_model_btn.hide()
        self.ui.load_pages.train_net_setting_grid_layout.setVerticalSpacing(20)  # 设置网格内部每个格子之间的垂直间距
        self.ui.load_pages.train_net_setting_grid_layout.setHorizontalSpacing(20)
        self.ui.load_pages.train_net_setting_grid_layout.setContentsMargins(300, 0, 300, 0)

        self.back_btn_in_train_net_setting_page = PyPushButton(
            text="上一步",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.back_btn_in_train_net_setting_page.setMinimumHeight(50)
        self.back_btn_in_train_net_setting_page.setMinimumWidth(80)
        self.back_btn_in_train_net_setting_page.setMaximumHeight(50)
        self.back_btn_in_train_net_setting_page.setMaximumWidth(80)
        self.back_btn_in_train_net_setting_page.clicked.connect(
            lambda: training_page_functions.back_in_train_net_setting_page())

        self.next_btn_in_train_net_setting_page = PyPushButton(
            text="开始训练",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.next_btn_in_train_net_setting_page.setMinimumHeight(50)
        self.next_btn_in_train_net_setting_page.setMinimumWidth(80)
        self.next_btn_in_train_net_setting_page.setMaximumHeight(50)
        self.next_btn_in_train_net_setting_page.setMaximumWidth(80)
        self.next_btn_in_train_net_setting_page.clicked.connect(
            lambda: training_page_functions.next_in_train_net_setting_page(_home_page_functions=home_page_functions))
        self.ui.load_pages.train_net_setting_btn_layout.addStretch(1)
        self.ui.load_pages.train_net_setting_btn_layout.setSpacing(20)
        self.ui.load_pages.train_net_setting_btn_layout.setContentsMargins(0, 0, 20, 0)
        self.ui.load_pages.train_net_setting_btn_layout.addWidget(self.back_btn_in_train_net_setting_page)
        self.ui.load_pages.train_net_setting_btn_layout.addWidget(self.next_btn_in_train_net_setting_page)

        # ///////////////////////////////////////////////////////////////
        # PAGE TRAIN INFO
        # ///////////////////////////////////////////////////////////////

        self.select_data_type = QLabel()
        self.select_data_type.setMinimumHeight(20)
        self.select_data_dir = QLabel()
        self.select_data_dir.setMinimumHeight(20)
        self.select_test_set_rate = QLabel("测试集比例: 未划分测试集")
        self.select_test_set_rate.setMinimumHeight(20)
        self.select_model_save_dir = QLabel()
        self.select_model_save_dir.setMinimumHeight(20)
        self.select_epochs = QLabel()
        self.select_epochs.setMinimumHeight(20)
        self.select_batchsize = QLabel()
        self.select_batchsize.setMinimumHeight(20)
        self.select_val_set_rate = QLabel("验证集比例: 未划分验证集")
        self.select_val_set_rate.setMinimumHeight(20)
        self.select_learning_rate = QLabel()
        self.select_learning_rate.setMinimumHeight(20)
        self.select_dacay_rate = QLabel()
        self.select_dacay_rate.setMinimumHeight(20)
        self.select_decay_steps = QLabel()
        self.select_decay_steps.setMinimumHeight(20)
        self.select_dropout_rate = QLabel()
        self.select_dropout_rate.setMinimumHeight(20)
        self.select_pretrained_model_dir = QLabel()
        self.select_pretrained_model_dir.setMinimumHeight(20)

        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_data_type, 0, 0, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_data_dir, 0, 1, 1, 5)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_test_set_rate, 1, 0, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_model_save_dir, 1, 1, 1, 5)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_epochs, 2, 0, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_batchsize, 2, 1, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_val_set_rate, 2, 2, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_learning_rate, 2, 3, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_dacay_rate, 2, 4, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_decay_steps, 2, 5, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_dropout_rate, 3, 0, 1, 1)
        self.ui.load_pages.train_select_info_grid_layout.addWidget(self.select_pretrained_model_dir, 3, 0, 1, 6)
        if training_page_functions.is_incremental_train is True:
            self.select_pretrained_model_dir.show()
            self.select_dropout_rate.hide()
        else:
            self.select_pretrained_model_dir.hide()
            self.select_dropout_rate.show()

        self.train_text_edit = self.ui.load_pages.train_info_text_edit

        self.ui.load_pages.train_info_content_frame.setMinimumHeight(300)
        self.ui.load_pages.train_info_content_frame.setMaximumHeight(500)
        self.ui.load_pages.test_result_frame.hide()
        self.ui.load_pages.train_result_frame.hide()

        self.stop_training_btn = PyPushButton(
            text="中止训练",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.stop_training_btn.setMinimumHeight(50)
        self.stop_training_btn.setMinimumWidth(80)
        self.stop_training_btn.setMaximumHeight(50)
        self.stop_training_btn.setMaximumWidth(80)
        self.stop_training_btn.clicked.connect(lambda : training_page_functions.stop_training_btn_event())

        self.back_btn_in_train_info_page = PyPushButton(
            text="上一步",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.back_btn_in_train_info_page.setMinimumHeight(50)
        self.back_btn_in_train_info_page.setMinimumWidth(80)
        self.back_btn_in_train_info_page.setMaximumHeight(50)
        self.back_btn_in_train_info_page.setMaximumWidth(80)
        self.back_btn_in_train_info_page.clicked.connect(lambda : training_page_functions.back_to_net_setting())

        self.retraining_btn = PyPushButton(
            text="重新训练",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.retraining_btn.setMinimumHeight(50)
        self.retraining_btn.setMinimumWidth(80)
        self.retraining_btn.setMaximumHeight(50)
        self.retraining_btn.setMaximumWidth(80)
        self.retraining_btn.clicked.connect(lambda : training_page_functions.re_training())

        self.back_home_in_train_info_page = PyPushButton(
            text="返回主页",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        self.back_home_in_train_info_page.setMinimumHeight(50)
        self.back_home_in_train_info_page.setMinimumWidth(80)
        self.back_home_in_train_info_page.setMaximumHeight(50)
        self.back_home_in_train_info_page.setMaximumWidth(80)
        self.back_home_in_train_info_page.clicked.connect(
            lambda: training_page_functions.back_to_main_in_page_train_info())

        self.ui.load_pages.train_info_btn_layout.addStretch(1)
        self.ui.load_pages.train_info_btn_layout.setSpacing(20)
        self.ui.load_pages.train_info_btn_layout.setContentsMargins(0, 0, 20, 0)
        self.ui.load_pages.train_info_btn_layout.addWidget(self.stop_training_btn)
        self.ui.load_pages.train_info_btn_layout.addWidget(self.back_btn_in_train_info_page)
        self.ui.load_pages.train_info_btn_layout.addWidget(self.retraining_btn)
        self.back_btn_in_train_info_page.hide()
        self.retraining_btn.hide()
        self.ui.load_pages.train_info_btn_layout.addWidget(self.back_home_in_train_info_page)

    # 刷新谱图检测页面
    def refresh_inference_page(self):
        self.inference_page_functions.refresh()

    # 刷新历史记录页面
    def refresh_history_page(self):
        self.history_page_functions.refresh(self.history_table, self.page_label)

    # 检测在 C:\Users\用户名\.keras\models 下有没有ImageNet的预训练模型
    #   如果有：就跳过
    #   如果没有：就将系统中保存的pretrained model复制到特定的目录下
    def check_imagenet_pretrained_model(self):
        imagenet_model_dir = "C:/Users/{}/.keras/models".format(getpass.getuser())
        imagenet_model_name = "mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5"
        saved_model_path = os.path.join("resource", imagenet_model_name)
        imagenet_model_path = os.path.join(imagenet_model_dir, imagenet_model_name)
        if os.path.isdir(imagenet_model_dir) and os.path.exists(saved_model_path):
            if not os.path.exists(imagenet_model_path):
                shutil.copy(saved_model_path, imagenet_model_path)
        else:
            return


        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////


    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
