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
from gui.uis.windows.login_window.ui_login_window import Ui_LoginWindow
from gui.uis.windows.main_window.functions_main_window import *
from gui.uis.windows.main_window.setup_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
from util.draw_best_model_hist import draw_best_model_hist

os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOW
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        # self.ui = UI_LoginWindow()
        # self.ui.setup_ui(self)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.login_btn.clicked.connect(self.check_data)
        self.ui.input_pwd.returnPressed.connect(self.check_data)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        # SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    def check_data(self):
        # ///////////////////////////////////////////////////////////////
        json_file = "user_info.json"
        app_path = os.path.abspath(os.getcwd())
        user_info = os.path.normpath(os.path.join(app_path, json_file))
        if not os.path.isfile(user_info):
            print(f"WARNING: \"user_info.json\" not found! check in the folder {user_info}")

        with open(user_info, "r", encoding='utf-8') as reader:
            info = json.loads(reader.read())

        username = self.ui.input_username.text()
        password = self.ui.input_pwd.text()

        if username == '':
            QMessageBox.warning(
                self,
                '警告',
                '用户名为空，请输入用户名！')
        elif password == '':
            QMessageBox.warning(
                self,
                '警告',
                '旧密码为空，请输入旧密码！')
        elif username != info['username'] or password != info['password']:
            QMessageBox.warning(
                self,
                '警告',
                '用户名或密码错误！')
        else:
            self.close()
            main_window = MainWindow()
            main_window.show()
            self.ui.input_pwd.setText('')

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)
        SetupMainWindow.check_imagenet_pretrained_model(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # 退出登录
    def exit(self):
        close_msg = QMessageBox.question(self, "提示", "确认退出?", QMessageBox.Yes, QMessageBox.No)
        if close_msg == QMessageBox.Yes:
            self.close()
            login_window = LoginWindow()
            login_window.show()
        else:
            return

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # OPEN PAGE 3
        # ///////////////////////////////////////////////////////////////

        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one("btn_home")
            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_home)

        # INFERENCE BTN
        if btn.objectName() == "btn_inference":
            # Select Menu
            self.ui.left_menu.select_only_one('btn_inference')
            # 刷新界面
            SetupMainWindow.refresh_inference_page(self)
            # Load Page Inference
            MainFunctions.set_page(self, self.ui.load_pages.page_inference)

        # HISTORY BTN
        if btn.objectName() == "btn_history":
            # Select Menu
            self.ui.left_menu.select_only_one("btn_history")
            # 刷新界面
            SetupMainWindow.refresh_history_page(self)
            # Load Page History
            MainFunctions.set_page(self, self.ui.load_pages.page_history)

        if btn.objectName() == "btn_add_images":
            #select menu
            self.ui.left_menu.select_only_one("btn_add_images")
            # load page
            MainFunctions.set_page(self, self.ui.load_pages.page_add_images)

        if btn.objectName() == "btn_training":
            #select menu
            self.ui.left_menu.select_only_one("btn_training")
            # load page
            MainFunctions.set_page(self, self.ui.load_pages.page_train_base_setting)

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_user":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                # btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                # btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
                # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon_blue.ico"))
    window = LoginWindow()

    # EXEC APP
    # ////////////////////////////////////  ///////////////////////////
    sys.exit(app.exec())
