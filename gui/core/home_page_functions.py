import os

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from qt_core import *

class HomePageFunctions:
    def __init__(self, setup_main_window):
        self.setup_main_window = setup_main_window

    def to_page_inference(self, _inference_page_functions):
        _inference_page_functions.refresh()
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_inference)
        self.setup_main_window.ui.left_menu.select_only_one("btn_inference")

    def to_page_history(self, _history_page_functions):
        _history_page_functions.refresh(self.setup_main_window.history_table, self.setup_main_window.page_label)
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_history)
        self.setup_main_window.ui.left_menu.select_only_one("btn_history")

    def to_page_add_images(self):
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_add_images)
        self.setup_main_window.ui.left_menu.select_only_one("btn_add_images")

    def to_page_train(self):
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_train_base_setting)
        self.setup_main_window.ui.left_menu.select_only_one("btn_training")

    def open_user_info(self):
        MainFunctions.toggle_right_column(self.setup_main_window)

    def change_table_content(self, dataset_dir):
        # 清空并删除表格内容
        self.setup_main_window.dataset_table.clearContents()
        self.setup_main_window.dataset_table.setRowCount(0)
        # 加载新数据集
        self.load_dataset_info(dataset_dir)
        self.setup_main_window.dataset_dir_edit.setText(dataset_dir)

    def choose_dataset(self):
        open_dir = QFileDialog.getExistingDirectory(self.setup_main_window, "选择数据集所在路径", "./")
        if open_dir == "":
            return
        self.change_table_content(open_dir)

    def add_none_label_row(self, row_index):
        self.setup_main_window.dataset_table.insertRow(row_index)
        # 添加年份
        year_label_text = QTableWidgetItem()
        year_label_text.setTextAlignment(Qt.AlignCenter)
        year_label_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 2, year_label_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 添加每个年份图片的数量
        img_nums_text = QTableWidgetItem()
        img_nums_text.setTextAlignment(Qt.AlignCenter)
        img_nums_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 3, img_nums_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 每个年份文件的路径
        year_dir_text = QTableWidgetItem()
        year_dir_text.setTextAlignment(Qt.AlignCenter)
        year_dir_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 4, year_dir_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)

    def add_none_usage_type_row(self, row_index):
        self.setup_main_window.dataset_table.insertRow(row_index)
        # 每个类型谱图的子文件夹使用类型
        usage_type_text = QTableWidgetItem()
        usage_type_text.setTextAlignment(Qt.AlignCenter)
        usage_type_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 1, usage_type_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 每个类型谱图的子文件夹使用类型 下的 谱图数量
        usage_type_text = QTableWidgetItem()
        usage_type_text.setTextAlignment(Qt.AlignCenter)
        usage_type_text.setText(str(0))
        self.setup_main_window.dataset_table.setItem(row_index, 5, usage_type_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 添加年份
        year_label_text = QTableWidgetItem()
        year_label_text.setTextAlignment(Qt.AlignCenter)
        year_label_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 2, year_label_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 添加每个年份图片的数量
        img_nums_text = QTableWidgetItem()
        img_nums_text.setTextAlignment(Qt.AlignCenter)
        img_nums_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 3, img_nums_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)
        # 每个年份文件的路径
        year_dir_text = QTableWidgetItem()
        year_dir_text.setTextAlignment(Qt.AlignCenter)
        year_dir_text.setText("None")
        self.setup_main_window.dataset_table.setItem(row_index, 4, year_dir_text)
        self.setup_main_window.dataset_table.setRowHeight(row_index, 22)

    def load_dataset_info(self, dataset_dir):
        data_type_list = []
        if os.path.isdir(dataset_dir):
            data_type_list = os.listdir(dataset_dir)
        row_index_of_data_type = 0  # 下一个要插入的data_type所在行的index

        for data_type in data_type_list:
            data_type_dir = os.path.join(dataset_dir, data_type)
            usage_type_list = []
            if os.path.isdir(data_type_dir):
                usage_type_list = os.listdir(data_type_dir)
            row_index_of_usage_type = row_index_of_data_type  # 下一个要插入usage_type所在行index
            row_number_of_data_type = 0  # 当前数据类型下，所占的行数，用于span
            img_nums_of_data_type = 0  # 当前data_type的图片总量

            if len(usage_type_list) == 0:
                self.add_none_usage_type_row(row_index_of_usage_type)
                row_index_of_usage_type = row_index_of_usage_type + 1
                row_number_of_data_type = row_number_of_data_type + 1
                img_nums_of_data_type = img_nums_of_data_type + 0

            for usage_type in usage_type_list:
                usage_type_dir = os.path.join(data_type_dir, usage_type)
                year_list = []
                img_nums_of_usage_type = 0  # 当前usage_type的图片总量
                if os.path.isdir(usage_type_dir):
                    year_list = os.listdir(usage_type_dir)

                if len(year_list) == 0:
                    row_number = self.setup_main_window.dataset_table.rowCount()
                    self.add_none_label_row(row_number)

                for year_label in year_list:
                    year_dir = os.path.join(usage_type_dir, year_label)
                    img_list = []
                    if os.path.isdir(year_dir):
                        img_list = os.listdir(year_dir)
                    img_nums_of_label = 0 if len(img_list) == 0 else len(img_list)  # 当前label下的图片数量

                    row_number = self.setup_main_window.dataset_table.rowCount()  # 根据rowCount获取下一个要插入的label所在行index
                    self.setup_main_window.dataset_table.insertRow(row_number)
                    # 添加年份
                    year_label_text = QTableWidgetItem()
                    year_label_text.setTextAlignment(Qt.AlignCenter)
                    year_label_text.setText(year_label + " 年")
                    self.setup_main_window.dataset_table.setItem(row_number, 2, year_label_text)
                    self.setup_main_window.dataset_table.setRowHeight(row_number, 22)
                    # 添加每个年份图片的数量
                    img_nums_text = QTableWidgetItem()
                    img_nums_text.setTextAlignment(Qt.AlignCenter)
                    img_nums_text.setText(str(img_nums_of_label) + " 张")
                    self.setup_main_window.dataset_table.setItem(row_number, 3, img_nums_text)
                    self.setup_main_window.dataset_table.setRowHeight(row_number, 22)
                    # 每个年份文件的路径
                    year_dir_text = QTableWidgetItem()
                    year_dir_text.setTextAlignment(Qt.AlignCenter)
                    year_dir_text.setText("/" + os.path.join(data_type, usage_type, year_label).replace('\\', '/'))
                    self.setup_main_window.dataset_table.setItem(row_number, 4, year_dir_text)
                    self.setup_main_window.dataset_table.setRowHeight(row_number, 22)

                    img_nums_of_usage_type = img_nums_of_usage_type + img_nums_of_label

                # 每个类型谱图的子文件夹使用类型
                usage_type_text = QTableWidgetItem()
                usage_type_text.setTextAlignment(Qt.AlignCenter)
                usage_type_text.setText(usage_type)
                self.setup_main_window.dataset_table.setItem(row_index_of_usage_type, 1, usage_type_text)
                self.setup_main_window.dataset_table.setRowHeight(row_index_of_usage_type, 22)
                # 每个类型谱图的子文件夹使用类型 下的 谱图数量
                usage_type_text = QTableWidgetItem()
                usage_type_text.setTextAlignment(Qt.AlignCenter)
                usage_type_text.setText(str(img_nums_of_usage_type) + " 张")
                self.setup_main_window.dataset_table.setItem(row_index_of_usage_type, 5, usage_type_text)
                self.setup_main_window.dataset_table.setRowHeight(row_index_of_usage_type, 22)

                row_number_of_usage_type = 1 if len(year_list) == 0 else len(year_list)
                self.setup_main_window.dataset_table.setSpan(row_index_of_usage_type, 1, row_number_of_usage_type, 1)
                self.setup_main_window.dataset_table.setSpan(row_index_of_usage_type, 5, row_number_of_usage_type, 1)

                row_index_of_usage_type = row_index_of_usage_type + row_number_of_usage_type
                row_number_of_data_type = row_number_of_data_type + row_number_of_usage_type
                img_nums_of_data_type = img_nums_of_data_type + img_nums_of_usage_type

            # 每个类型谱图的类型名称
            data_type_text = QTableWidgetItem()
            data_type_text.setTextAlignment(Qt.AlignCenter)
            data_type_text.setText(data_type)
            self.setup_main_window.dataset_table.setItem(row_index_of_data_type, 0, data_type_text)
            self.setup_main_window.dataset_table.setRowHeight(row_index_of_data_type, 22)
            # 每个类型谱图的总数
            img_total_nums_text = QTableWidgetItem()
            img_total_nums_text.setTextAlignment(Qt.AlignCenter)
            img_total_nums_text.setText(str(img_nums_of_data_type) + " 张")
            self.setup_main_window.dataset_table.setItem(row_index_of_data_type, 6, img_total_nums_text)
            self.setup_main_window.dataset_table.setRowHeight(row_index_of_data_type, 22)

            self.setup_main_window.dataset_table.setSpan(row_index_of_data_type, 0, row_number_of_data_type, 1)
            self.setup_main_window.dataset_table.setSpan(row_index_of_data_type, 6, row_number_of_data_type, 1)
            row_index_of_data_type = row_index_of_data_type + row_number_of_data_type
