import sqlite3

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from gui.widgets.py_history_detail_page.py_history_detail_page import PyHistoryDetailPage
from qt_core import *
from gui.widgets.py_push_button import PyPushButton
from gui.widgets.py_history_detail_button import PyHistoryDetailButton


class HistoryPageFunctions:
    def __init__(self, setup_main_window, database):
        self.setup_main_window = setup_main_window
        self.history_detail_page = None
        # 连接数据库(如果不存在则创建)
        try:
            self.conn = sqlite3.connect(database)
            print(f"Opened {database} successfully")
            # 创建游标
            self.cursor = self.conn.cursor()
            self.current = 1
            self.data_num = len(self.select_all_id())
            self.init_data = self.select(self.current)
            self.max_page_num = self.data_num // 7 + (0 if self.data_num%7 == 0 else 1)
        except sqlite3.DatabaseError as e:
            print(e)

    # 统计数据库中数据条数
    def select_all_id(self):
        try:
            sql = f'SELECT id FROM HISTORY'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)

    # 根据当前页面查询：start = (current - 1) * 7 + 1; end = start + 6
    # 倒序查询: start = data_num - current * 7 + 1; end = start + 6
    def select(self, current):
        try:
            nums = 7
            start = (current - 1) * nums  # 倒序
            # start = (current - 1) * 7 + 1  # 正序
            sql = f'SELECT id, img_path, img_type, infer_time, predict_result FROM HISTORY ORDER BY id DESC limit {start},{nums}'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)

    # 下一页
    def next_page(self, table, label):
        # 如果下一页<=最大页数，则查询下一页数据，并更新表格
        if self.current + 1 <= self.max_page_num:
            next_data = self.select(self.current + 1)
            self.current += 1
            self.update(next_data, table, label)
            print(f'当前页面： {self.current}')
        else:
            return self.select(self.current)

    # 上一页
    def pre_page(self, table, label):
        # 如果上一页>=1，则查询上一页数据，并更新表格
        if self.current - 1 >= 1:
            pre_data = self.select(self.current - 1)
            self.current -= 1
            self.update(pre_data, table, label)
            print(f'当前页面： {self.current}')

    # 跳转功能
    def jump_to(self, table, label, line_edit):
        # 如果要跳转的页面在(1, max_page_num)范围内，则查询跳转页面的数据，并更新表格
        if line_edit.text() and int(line_edit.text()) != self.current:
            if 1 <= int(line_edit.text()) <= self.max_page_num:
                self.current = int(line_edit.text())
                data = self.select(self.current)
                self.update(data, table, label)
                print(f'当前页面： {self.current}')

    # 更新数据
    def update(self, data, table, label):
        # 更新页面的页码
        label.setText(f'第 {self.current}/{self.max_page_num} 页')
        # 清空原有数据
        table.clearContents()
        if len(data) <= 7:
            table.setRowCount(7)
        # 添加数据
        for i, d in enumerate(data):
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

            def return_history_detail_btn(img_id):
                btn_widget = PyHistoryDetailButton(img_id)
                btn_widget.col_btn.clicked.connect(lambda: self.history_detail(btn_widget))
                return btn_widget

            table.setCellWidget(i, 0, img_widget)  # 谱图
            table.setItem(i, 1, col_2)  # 谱图类型
            table.setItem(i, 2, col_3)  # 检测时间
            table.setItem(i, 3, col_4)  # 检测结果
            table.setCellWidget(i, 4, return_history_detail_btn(d[0]))  # 查看详情

    # 根据id查询历史详情
    def history_detail(self, btn_widget):
        sql = f'SELECT * FROM HISTORY WHERE id = {btn_widget.img_id}'
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        self.history_detail_page = PyHistoryDetailPage(data)
        self.setup_main_window.ui.load_pages.history_detail_layout.addWidget(self.history_detail_page)

        # 跳转到详情页面
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_history_2)

    # 刷新界面
    def refresh(self, table, label):
        self.current = 1
        data = self.select(1)

        self.current = 1
        self.data_num = len(self.select_all_id())
        self.init_data = self.select(self.current)
        self.max_page_num = self.data_num // 7 + (0 if self.data_num % 7 == 0 else 1)

        self.update(data, table, label)
        if self.history_detail_page is not None:
            self.history_detail_page.deleteLater()
            self.history_detail_page = None
        print('History Page is refreshed! ')
