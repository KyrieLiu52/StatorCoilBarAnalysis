import os
import sqlite3

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from qt_core import *


class LoginFunction:
    def __init__(self, setup_main_window):
        self.setup_main_window = setup_main_window

    def verify(self):
        # 读取数据库的时候不能使用./
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # db_path = os.path.join(BASE_DIR, "demo.db")
        db_path = "demo.db"
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        username = self.setup_main_window.input_username.text().strip()
        password = self.setup_main_window.input_pwd.text().strip()

        cur.execute("select * from tb_users where username=? and password=?", (username, password))
        if cur.fetchone() is not None:
            MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_main)
        else:
            login_error_msg_box = QMessageBox(QMessageBox.Warning, '登录失败', '用户名或密码输入有误!')
            login_error_msg_box.exec_()
        cur.close()
        con.close()
