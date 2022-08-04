import os
import shutil
import time

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from gui.widgets import PyToAddImageLabel
from qt_core import *


class AddImagesFunctions:
    def __init__(self, _setup_main_window):
        self.setup_main_window = _setup_main_window
        self.images_url = []

    def choose_save_dir(self):
        save_dir = QFileDialog.getExistingDirectory(self.setup_main_window, "选择谱图保存路径", "./")
        if save_dir == "":
            return
        self.setup_main_window.data_save_dir_edit.setText(save_dir)

    def load_multiple_images(self):
        openfile_names = QFileDialog.getOpenFileNames(self.setup_main_window, "选择上传的图片", "./data",
                                                      "Image files(*.jpg *jpeg *.png *.jpe *.tif *.tiff *.bmp *.tbi *.jfif)")
        images_path = openfile_names[0]
        if len(images_path) == 0:
            return
        repeat_flag = False
        for image_path in images_path:
            tmp = self.load_image(image_path)
            if tmp == True and repeat_flag == False:
                repeat_flag = True
        self.add_btn_by_previous_nums(len(self.images_url))
        if repeat_flag:
            if len(images_path) == 1:
                img_exist_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '该图片已经读取，请选择其他图片!')
                img_exist_error_msg_box.exec_()
            else:
                img_exist_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '部分图片已读取过，未读取图片已添加!')
                img_exist_error_msg_box.exec_()

    def load_image(self, image_path=""):
        if image_path == "":
            return
        if image_path in self.images_url:
            # 如果该图片已经读取，直接返回True，表示发生了重复
            return True
        #  计算插入的位置
        added_images_nums = len(self.images_url)
        try:
            self.add_images_by_previous_nums(added_images_nums, image_path)
        except:
            img_read_error_msg_box = QMessageBox(QMessageBox.Warning, '图片读取失败', '图片读取失败，请重新读取!')
            img_read_error_msg_box.exec_()
        else:
            self.images_url.append(image_path)

    def add_images_by_previous_nums(self, previous_img_nums, image_path):
        row = previous_img_nums // 8
        col = previous_img_nums % 8
        to_add_image_label = PyToAddImageLabel(_img_path=image_path,
                                               _setup_main_window=self.setup_main_window)
        # Previous
        # to_add_image_label.setPixmap(
        #     QPixmap(image_path).scaled(100, 60, aspectMode=Qt.AspectRatioMode.IgnoreAspectRatio,
        #                                mode=Qt.SmoothTransformation))
        self.setup_main_window.ui.load_pages.add_images_grid_layout.addWidget(to_add_image_label, 3 + row, col * 2,
                                                                              1, 2,
                                                                              Qt.AlignLeft | Qt.AlignTop)
        to_add_image_label.del_btn.clicked.connect(lambda: self.delete_toadd_image(to_add_image_label))
        # to_add_image_label.del_btn.clicked.connect(lambda: self.delete_toadd_image(image_path))
        # 不需要删除，在新的位置加入按钮即可，同一个widget只可以存在一个
        # self.ui.load_pages.add_images_grid_layout.removeWidget(self.add_image_btn)
        # sip.delete(self.add_image_btn)

    def add_btn_by_previous_nums(self, previous_img_nums):
        row = previous_img_nums // 8
        col = previous_img_nums % 8
        self.setup_main_window.ui.load_pages.add_images_grid_layout.addWidget(self.setup_main_window.add_image_btn,
                                                                              3 + row, col * 2, 1, 2,
                                                                              Qt.AlignLeft | Qt.AlignTop)

    def delete_toadd_image(self, to_add_image_label):
        if to_add_image_label.img_path in self.images_url:
            self.images_url.remove(to_add_image_label.img_path)
        else:
            return
        to_del_img_index = self.setup_main_window.ui.load_pages.add_images_grid_layout.indexOf(to_add_image_label)
        self.clear_added_images_after_one(to_del_img_index)
        previous_img_nums = to_del_img_index - 10
        for i in range(previous_img_nums, len(self.images_url)):
            self.add_images_by_previous_nums(i, self.images_url[i])
        self.add_btn_by_previous_nums(len(self.images_url))

    def clear_added_images_after_one(self, index):
        previous_img_nums = index - 10
        for i in range(index, self.setup_main_window.ui.load_pages.add_images_grid_layout.count() - 1):
            self.setup_main_window.ui.load_pages.add_images_grid_layout.itemAt(i).widget().del_btn._tooltip.deleteLater()
            self.setup_main_window.ui.load_pages.add_images_grid_layout.itemAt(i).widget().deleteLater()
        self.add_btn_by_previous_nums(previous_img_nums)

    def back_to_main_page_in_add_page(self):
        if len(self.images_url) != 0:
            back_flag = QMessageBox.question(self.setup_main_window, '提示', '确定返回吗!', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
            if back_flag == QMessageBox.Yes:
                self.clear_added_images()
                self.images_url.clear()
                MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_home)
            else:
                return
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_home)
        self.setup_main_window.ui.left_menu.select_only_one("btn_home")

    def clear_added_images(self):
        for i in range(10, self.setup_main_window.ui.load_pages.add_images_grid_layout.count() - 1):
            self.setup_main_window.ui.load_pages.add_images_grid_layout.itemAt(
                i).widget().del_btn._tooltip.deleteLater()
            self.setup_main_window.ui.load_pages.add_images_grid_layout.itemAt(i).widget().deleteLater()
        self.add_btn_by_previous_nums(0)

    def upload_images(self, _home_page_functions):
        data_type = ""
        data_year = self.setup_main_window.data_year_edit.text().strip()
        data_save_dir = self.setup_main_window.data_save_dir_edit.text().strip()
        if self.setup_main_window.data_type_afm.isChecked():
            data_type = "AFM"
        elif self.setup_main_window.data_type_sem.isChecked():
            data_type = "SEM"
        elif self.setup_main_window.data_type_saxs.isChecked():
            data_type = "SAXS"
        elif self.setup_main_window.data_type_waxd.isChecked():
            data_type = "WAXD"
        if data_year not in ["0", "10", "13"]:
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '谱图年份可选为0,10,13!')
            upload_error_msg_box.exec_()
            return
        if data_type == "":
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '未选择谱图类型，请进行选择!')
            upload_error_msg_box.exec_()
            return
        if data_year == "":
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '未填写谱图年份，请进行填写!')
            upload_error_msg_box.exec_()
            return
        if data_save_dir == "":
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '未选择谱图保存路径，请进行选择!')
            upload_error_msg_box.exec_()
            return
        if len(self.images_url) == 0:
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '没有选择任何图片，请进行选择!')
            upload_error_msg_box.exec_()
            return
        if not os.path.isdir(data_save_dir):
            os.mkdir(data_save_dir)
        data_type_path = os.path.join(data_save_dir, data_type)
        if not os.path.isdir(data_type_path):
            os.mkdir(data_type_path)
        data_train_path = os.path.join(data_type_path, "train")
        if not os.path.isdir(data_train_path):
            os.mkdir(data_train_path)
        data_year_path = os.path.join(data_train_path, data_year)
        if not os.path.isdir(data_year_path):
            os.mkdir(data_year_path)
        try:
            count = 0
            for origin_img_url in self.images_url:
                localTime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
                img_format = origin_img_url.split(".")[-1]
                img_name = data_type + "_" + data_year + "_" + localTime + "_" + str(count) + "." + img_format
                count += 1
                target_img_url = os.path.join(data_year_path, img_name)
                shutil.copyfile(origin_img_url, target_img_url)
        except:
            upload_error_msg_box = QMessageBox(QMessageBox.Warning, '上传错误', '图片上传过程中发生错误，请重试!')
            upload_error_msg_box.exec_()
            return
        else:
            #  上传完成
            success_msg = "图片上传至:{}/{}/{}/{}目录下\n  {}:表示谱图类型\n  {}:表示用作模型训练\n  {}:表示谱图年份" \
                .format(data_save_dir, data_type, "train", data_year, data_type, "train", data_year)
            upload_success_msg_box = QMessageBox(QMessageBox.Information, '上传成功', success_msg)
            upload_success_msg_box.exec_()
            self.clear_added_images()
            self.images_url.clear()
            _home_page_functions.change_table_content(data_save_dir)
