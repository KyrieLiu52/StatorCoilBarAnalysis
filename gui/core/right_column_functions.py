import json
import os

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from qt_core import *


class RightColumnFunctions:
    def __init__(self, setup_main_window):
        self.setup_main_window = setup_main_window
        self.user_info = self.get_data()

    def get_data(self):
        # ///////////////////////////////////////////////////////////////
        json_file = "user_info.json"
        app_path = os.path.abspath(os.getcwd())
        user_info = os.path.normpath(os.path.join(app_path, json_file))
        if not os.path.isfile(user_info):
            print(f"WARNING: \"user_info.json\" not found! check in the folder {user_info}")

        with open(user_info, "r", encoding='utf-8') as reader:
            info = json.loads(reader.read())
        return info

    def check_data(self):
        username = self.setup_main_window.username_line_edit.text()
        old_password = self.setup_main_window.old_password_line_edit.text()
        new_password = self.setup_main_window.new_password_line_edit.text()
        check_new_password = self.setup_main_window.check_new_password_line_edit.text()
        print(username)
        print(old_password)
        print(new_password)
        print(check_new_password)
        print(self.user_info)
        if username == '':
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '用户名为空，请输入用户名！')
        elif old_password == '':
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '旧密码为空，请输入旧密码！')
        elif username != self.user_info['username'] or old_password != self.user_info['password']:
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '用户名或密码错误！')
        elif new_password == '':
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '新密码为空，请输入新密码！')
        elif check_new_password == '':
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '请确认新密码！')

        elif new_password != check_new_password:
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '两次新密码输入不一致！')
        else:
            self.user_info['password'] = new_password
            self.set_data()
            QMessageBox.about(
                self.setup_main_window,
                '成功',
                '密码修改成功！')
            MainFunctions.toggle_right_column(self.setup_main_window)
            self.setup_main_window.old_password_line_edit.setText("")
            self.setup_main_window.new_password_line_edit.setText("")
            self.setup_main_window.check_new_password_line_edit.setText("")
            # 重置信息
            self.user_info = self.get_data()

    def set_data(self):
        # ///////////////////////////////////////////////////////////////
        json_file = "user_info.json"
        app_path = os.path.abspath(os.getcwd())
        user_info = os.path.normpath(os.path.join(app_path, json_file))
        if not os.path.isfile(user_info):
            print(f"WARNING: \"user_info.json\" not found! check in the folder {user_info}")

        with open(user_info, "w", encoding='utf-8') as writer:
            json.dump(self.user_info, writer)

    def cancel(self):
        MainFunctions.toggle_right_column(self.setup_main_window)
