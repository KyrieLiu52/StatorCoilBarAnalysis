import ctypes
import os
import shutil
import sys

from gui.uis.windows.main_window.functions_main_window import MainFunctions
from gui.widgets import PyTabMetric
from test_model import test_model
from util.data_split_out import data_set_split_out
from util.draw_best_model_hist import draw_best_model_hist
from util.my_callback import My_Callback
from util.common_function import *
from qt_core import *
from util.console_to_gui import Stream, TrainThread, IncrementalTrainThread, TestModelThread


class TrainingPageFunctions:
    def __init__(self, _setup_main_window):
        self.setup_main_window = _setup_main_window
        self.training_default_info = load_json_file("training_info.json")
        self.best_model_info = load_json_file("best_model.json")

        self.training_data_type = ""
        self.training_data_dir = self.training_default_info["dataset_dir"]
        self.model_save_dir = self.training_default_info["model_save_dir"]
        self.is_split_test_set = False
        self.split_out_rate = self.training_default_info["test_set_rate"]
        self.test_data_dir = ""

        self.epochs = self.training_default_info["epochs"]
        self.batchsize = self.training_default_info["batchsize"]
        self.validation_set_rate = self.training_default_info["val_set_rate"]
        self.learning_rate = self.training_default_info["learning_rate"]
        self.lr_decay_steps = self.training_default_info["lr_decay_steps"]
        self.lr_decay_rate = self.training_default_info["lr_decay_rate"]

        self.is_incremental_train = False
        # 加载预训练模型，即增量训练，需要pretrained_model参数，Dropout不可用（因为使用的模型是之前的模型，不需要指定模型相关的参数）
        self.pretrained_model = ""
        # 如果不加载预训练模型，则需要Dropout，不需要pretrained_model
        self.dropout_rate = self.training_default_info["dropout_rate"]

        # 正常训练的线程
        self.train_thread = TrainThread()
        self.train_thread.finished.connect(self.training_finish_process)    # 线程运行结束后，调用函数(无论正常结束或强制结束)
        self.train_thread.callback = My_Callback()
        # 增量训练的线程
        self.incremental_thread = IncrementalTrainThread()
        self.incremental_thread.finished.connect(self.training_finish_process)    # 线程运行结束后，调用函数(无论正常结束或强制结束)
        self.incremental_thread.callback = My_Callback()
        # 测试模型的线程
        self.test_model_thread = TestModelThread()
        self.test_model_thread.finished.connect(self.test_model_finish_process)

        # 是否被中止训练，用于线程结束后的判断
        self.is_stop_training = False

        self.home_page_functions = None

    # ////////////////////////////////////////////////
    # Train Base Setting
    # ////////////////////////////////////////////////

    def get_training_data_dir_by_data_type(self, data_type):
        sub_folder = ""
        if data_type == "AFM":
            sub_folder = "afm"
        elif data_type == "SEM":
            sub_folder = "sem"
        elif data_type == "SAXS":
            sub_folder = "saxs"
        elif data_type == "WAXD":
            sub_folder = "waxd"
        return os.path.join(self.training_default_info["dataset_dir"], sub_folder, "train").replace("\\", "/")

    def change_dataset_dir_by_data_type(self, radiobutton, data_type):
        if not radiobutton.isChecked():
            return
        correspond_dataset_dir = self.get_training_data_dir_by_data_type(data_type)
        self.setup_main_window.training_data_dir_edit.setText(correspond_dataset_dir)

    def is_split_out_change(self):
        # 在下一步的时候，根据check状态决定decay_rate的值
        if self.setup_main_window.is_split_test_set_toggle.isChecked():
            self.setup_main_window.split_out_rate_label.show()
            self.setup_main_window.split_out_rate_edit.show()
            self.setup_main_window.split_out_tip_label.show()
            self.is_split_test_set = True
        else:
            self.setup_main_window.split_out_rate_label.hide()
            self.setup_main_window.split_out_rate_edit.hide()
            self.setup_main_window.split_out_tip_label.hide()
            self.is_split_test_set = False

    def get_split_out_test_dir(self, src_dir):
        # 去除最后一个文件或文件夹：/data/afm/train/ -> /data/afm
        if src_dir[-1] == "\\" or src_dir[-1] == "/":
            src_dir = src_dir[:-1]
        parent_dir = os.path.dirname(src_dir)
        split_out_test_dir = os.path.join(parent_dir, "test").replace("\\", "/")
        return split_out_test_dir

    def choose_training_data_dir(self):
        data_dir = QFileDialog.getExistingDirectory(self.setup_main_window, "选择数据集路径", "./")
        if data_dir == "":
            return
        self.setup_main_window.training_data_dir_edit.setText(data_dir)

    def choose_model_save_dir(self):
        save_dir = QFileDialog.getExistingDirectory(self.setup_main_window, "选择模型保存路径", "./")
        if save_dir == "":
            return
        self.setup_main_window.model_save_dir_edit.setText(save_dir)

    def change_split_out_tip_info(self):
        tmp_training_data_dir = self.setup_main_window.training_data_dir_edit.text()
        str_split_out_rate = self.setup_main_window.split_out_rate_edit.text()
        tmp_test_data_dir = self.get_split_out_test_dir(tmp_training_data_dir)
        float_split_out_rate = 0.0
        if str_split_out_rate == "":
            return
        try:
            float_split_out_rate = float(str_split_out_rate)
        except:
            value_error_msg_box = QMessageBox(QMessageBox.Warning, '输入错误', '请输入数值格式的内容')
            value_error_msg_box.exec_()
            return
        else:
            if float_split_out_rate >= 0.0 and float_split_out_rate <= 1.0:
                self.setup_main_window.split_out_tip_label.setText("从训练集\"{}\"中\n随机划出{}%的数据\n到测试集\"{}\"中".
                                                                   format(tmp_training_data_dir,
                                                                          float_split_out_rate * 100,
                                                                          tmp_test_data_dir))
            else:
                scope_error_msg_box = QMessageBox(QMessageBox.Warning, '输入错误', '请输入0~1的数值')
                scope_error_msg_box.exec_()
                return

    def back_in_base_setting_page(self):
        back_flag = QMessageBox.question(self.setup_main_window, '提示', '确定返回吗!', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if back_flag == QMessageBox.Yes:
            MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_home)
            self.setup_main_window.ui.left_menu.select_only_one("btn_home")
        else:
            return

    def next_in_train_base_setting_page(self):
        # 处理本页
        if self.setup_main_window.training_data_type_afm.isChecked():
            self.training_data_type = "AFM"
        elif self.setup_main_window.training_data_type_sem.isChecked():
            self.training_data_type = "SEM"
        elif self.setup_main_window.training_data_type_saxs.isChecked():
            self.training_data_type = "SAXS"
        elif self.setup_main_window.training_data_type_waxd.isChecked():
            self.training_data_type = "WAXD"
        else:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '没有选择谱图类型')
            next_error_msg_box.exec_()
            return
        tmp_training_data_dir = self.setup_main_window.training_data_dir_edit.text()
        tmp_model_save_dir = self.setup_main_window.model_save_dir_edit.text()
        if tmp_training_data_dir == "":
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '未选择数据集路径')
            next_error_msg_box.exec_()
            return
        if tmp_model_save_dir == "":
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '信息遗漏提示', '未选择模型保存路径')
            next_error_msg_box.exec_()
            return
        if not os.path.exists(tmp_training_data_dir):
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '路径错误提示', '该数据集路径不存在')
            next_error_msg_box.exec_()
            return
        # 判断是否是正常的数据集：这里的依据是/datadir/labeldir/imgs
        if not os.path.exists(tmp_model_save_dir):
            os.mkdir(tmp_model_save_dir)
        self.training_data_dir = tmp_training_data_dir
        self.model_save_dir = tmp_model_save_dir
        if self.setup_main_window.is_split_test_set_toggle.isChecked() is True:
            self.split_out_rate = float(self.setup_main_window.split_out_rate_edit.text())
            self.test_data_dir = self.get_split_out_test_dir(self.training_data_dir)
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_train_net_setting)
        # 处理下一页
        if self.training_data_type == "AFM":
            self.setup_main_window.pretrained_model_edit.setText("./models/afm.h5")
        elif self.training_data_type == "SEM":
            self.setup_main_window.pretrained_model_edit.setText("./models/sem.h5")
        elif self.training_data_type == "SAXS":
            self.setup_main_window.pretrained_model_edit.setText("./models/saxs.h5")
        elif self.training_data_type == "WAXD":
            self.setup_main_window.pretrained_model_edit.setText("./models/waxd.h5")

    # Train Net Setting

    def lr_decay_change(self):
        # 在下一步的时候，根据check状态决定decay_rate的值
        if self.setup_main_window.is_lr_decay_toggle.isChecked() == True:
            self.setup_main_window.lr_decay_rate_label.show()
            self.setup_main_window.lr_decay_rate_edit.show()
            self.setup_main_window.lr_decay_steps_label.show()
            self.setup_main_window.lr_decay_steps_edit.show()
        else:
            self.setup_main_window.lr_decay_rate_label.hide()
            self.setup_main_window.lr_decay_rate_edit.hide()
            self.setup_main_window.lr_decay_steps_label.hide()
            self.setup_main_window.lr_decay_steps_edit.hide()

    def incremental_train_change(self):
        if self.setup_main_window.is_incremental_train_toggle.isChecked() is True:
            self.setup_main_window.pretrained_model_label.show()
            self.setup_main_window.pretrained_model_edit.show()
            self.setup_main_window.choose_pretrained_model_btn.show()
            self.setup_main_window.dropout_rate_label.hide()
            self.setup_main_window.dropout_rate_edit.hide()
            self.is_incremental_train = True
        else:
            self.setup_main_window.pretrained_model_label.hide()
            self.setup_main_window.pretrained_model_edit.hide()
            self.setup_main_window.choose_pretrained_model_btn.hide()
            self.setup_main_window.dropout_rate_label.show()
            self.setup_main_window.dropout_rate_edit.show()
            self.is_incremental_train = False

    def choose_pretrained_model(self):
        openfile_name = QFileDialog.getOpenFileName(self.setup_main_window, "选择预训练模型", "./models",
                                                    "Model files(*.h5)")
        model_path = openfile_name[0]
        if model_path == "":
            return
        self.setup_main_window.pretrained_model_edit.setText(model_path)

    def back_in_train_net_setting_page(self):
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_train_base_setting)

    def next_in_train_net_setting_page(self, _home_page_functions):
        # self.print_all_value()
        self.home_page_functions = _home_page_functions
        self.epochs = int(float(self.setup_main_window.epochs_edit.text()))
        self.batchsize = int(float(self.setup_main_window.batchsize_edit.text()))
        self.validation_set_rate = float(self.setup_main_window.validation_set_rate_edit.text())
        self.learning_rate = float(self.setup_main_window.learning_rate_edit.text())

        if self.epochs < 1:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '轮数至少为1')
            next_error_msg_box.exec_()
            return
        if self.batchsize <= 0:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '批大小至少为1')
            next_error_msg_box.exec_()
            return
        if self.validation_set_rate < 0 or self.validation_set_rate > 1:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '验证集比例必须在0到1之间')
            next_error_msg_box.exec_()
            return
        if self.learning_rate < 0 or self.learning_rate > 1:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '学习率建议在0到1之间')
            next_error_msg_box.exec_()
            return

        if self.setup_main_window.is_lr_decay_toggle.isChecked():
            self.lr_decay_rate = float(self.setup_main_window.lr_decay_rate_edit.text())
        else:
            self.lr_decay_rate = 1

        if self.lr_decay_rate < 0 or self.lr_decay_rate > 1:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '衰减比率必须在0到1之间')
            next_error_msg_box.exec_()
            return

        self.lr_decay_steps = int(float(self.setup_main_window.lr_decay_steps_edit.text()))
        self.dropout_rate = float(self.setup_main_window.dropout_rate_edit.text())
        self.pretrained_model = self.setup_main_window.pretrained_model_edit.text()

        if self.lr_decay_steps < 1:
            next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', '衰减步长至少为1')
            next_error_msg_box.exec_()
            return

        # 如果划分测试集为true，在此处划分 ###################################################################

        if self.setup_main_window.is_incremental_train_toggle.isChecked():
            # 在之前的模型上增量训练
            if not os.path.exists(self.pretrained_model):
                QMessageBox.warning(self.setup_main_window, "数据错误", "所选预训练模型不存在")
                return
            print("增量训练:", self.training_data_type, self.training_data_dir, self.model_save_dir, self.epochs,
                  self.batchsize, self.learning_rate, self.lr_decay_rate, self.lr_decay_steps,
                  self.pretrained_model)
        else:
            if self.dropout_rate < 0 or self.dropout_rate > 1:
                next_error_msg_box = QMessageBox(QMessageBox.Warning, '提示', 'Dropout比率必须在0到1之间')
                next_error_msg_box.exec_()
                return
            # 在imagenet权重上重新训练
            print("重新训练:", self.training_data_type, self.training_data_dir, self.model_save_dir, self.epochs,
                  self.batchsize, self.learning_rate, self.lr_decay_rate, self.lr_decay_steps,
                  self.dropout_rate)
        MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_train_info)

        self.setup_main_window.select_data_type.setText("谱图类型: {}".format(self.training_data_type))
        self.setup_main_window.select_data_dir.setText("数据集路径: {}".format(self.training_data_dir))
        if self.is_split_test_set is True:
            self.setup_main_window.select_test_set_rate.setText("测试集比例: {}".format(self.split_out_rate))
        self.setup_main_window.select_model_save_dir.setText("模型保存路径: {}".format(self.model_save_dir))
        self.setup_main_window.select_epochs.setText("训练轮数: {}".format(self.epochs))
        self.setup_main_window.select_batchsize.setText("批大小: {}".format(self.batchsize))
        if self.validation_set_rate > 0:
            self.setup_main_window.select_val_set_rate.setText("验证集比例: {}".format(self.validation_set_rate))
        self.setup_main_window.select_learning_rate.setText("学习率: {}".format(self.learning_rate))
        self.setup_main_window.select_dacay_rate.setText("衰减比率: {}".format(self.lr_decay_rate))
        self.setup_main_window.select_decay_steps.setText("衰减步长: {}".format(self.lr_decay_steps))
        if self.is_incremental_train is True:
            self.setup_main_window.select_pretrained_model_dir.setText("预训练模型: {}".format(self.pretrained_model))
            self.setup_main_window.select_pretrained_model_dir.show()
            self.setup_main_window.select_dropout_rate.hide()
        else:
            self.setup_main_window.select_dropout_rate.setText("Dropout比率: {}".format(self.dropout_rate))
            self.setup_main_window.select_pretrained_model_dir.hide()
            self.setup_main_window.select_dropout_rate.show()
        self.setup_main_window.back_btn_in_train_info_page.hide()
        self.setup_main_window.retraining_btn.hide()
        self.setup_main_window.stop_training_btn.show()
        self.begin_training()

    def re_training(self):
        retrain_flag = QMessageBox.question(self.setup_main_window, '提示', '确定重新训练吗!',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if retrain_flag == QMessageBox.Yes:
            self.clear_test_and_train_result()
            self.next_in_train_net_setting_page(_home_page_functions=self.home_page_functions)

    def begin_training(self):
        self.clear_test_and_train_result()
        if self.is_incremental_train is True:
            self.begin_incremental_training()
        else:
            self.begin_normal_training()

    def print_all_value(self):
        print("谱图类型:{}, 数据集路径:{}, 模型保存路径:{},\n"
              " 是否划分测试集:{}, 划分比例:{}, 测试集路径:{},\n"
              "epochs:{}, batchsize:{}, 验证集比例:{},\n"
              "学习率:{}, 衰退步长:{}, 衰退比率:{},\n"
              "是否增强:{}, 预训练模型路径:{}, Dropout比率:{}".
              format(self.training_data_type, self.training_data_dir, self.model_save_dir,
                     self.is_split_test_set, self.split_out_rate, self.test_data_dir,
                     self.epochs, self.batchsize, self.validation_set_rate,
                     self.learning_rate, self.lr_decay_steps, self.lr_decay_rate,
                     self.is_incremental_train, self.pretrained_model, self.dropout_rate))

    def training_finish_process(self):
        # 如果是因为中止训练而结束的，则跳过处理
        if self.is_stop_training is True:
            return
        self.setup_main_window.back_btn_in_train_info_page.show()
        self.setup_main_window.retraining_btn.show()
        self.setup_main_window.stop_training_btn.hide()
        if self.is_incremental_train is True:
            self.incremental_training_finished()
        else:
            self.normal_training_finished()
        # 如果未划分测试集，在此处结束，并提示
        # 如果划分了，在测试结束处进行提示
        if self.is_split_test_set is False:
            QMessageBox.about(self.setup_main_window, '提示', '训练完成!')
            sys.stdout = sys.__stdout__

    def normal_training_finished(self):
        train_result_pic_path = self.train_thread.train_result_pic_path
        highest_acc = self.train_thread.highest_acc
        highest_val_acc = self.train_thread.highest_val_acc
        best_model_path = self.train_thread.best_model_path

        train_result_pic = QLabel()
        train_result_pic.setPixmap(QPixmap(train_result_pic_path))
        train_result_pic.setScaledContents(True)
        train_result_pic.setMaximumSize(450, 450)
        train_result_pic.setAlignment(Qt.AlignCenter)
        train_result_pic_title = QLabel("训练结果(Accuracy and Loss)")
        train_result_pic_title.setAlignment(Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.train_result_pic_layout.addWidget(train_result_pic, Qt.AlignCenter,
                                                                               Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.train_result_pic_layout.addWidget(train_result_pic_title)
        self.setup_main_window.ui.load_pages.train_result_pic_frame.setStyleSheet(
            "background:{}".format(self.setup_main_window.themes["app_color"]["text_description"]))
        self.setup_main_window.ui.load_pages.train_result_frame.show()

        self.update_latest_train_result_pic(data_type=self.training_data_type, train_result_pic_path=train_result_pic_path)

        # 如果划分了测试集，就进行测试
        if self.is_split_test_set is True and self.split_out_rate != 0:
            self.begin_test_model(test_set_dir=self.test_data_dir,
                                  data_type=self.training_data_type,
                                  model_path=best_model_path)

        self.process_best_model_info(data_type=self.training_data_type,
                                     highest_acc = highest_acc,
                                     highest_val_acc=highest_val_acc,
                                     best_model_path=best_model_path)

    def incremental_training_finished(self):
        train_result_pic_path = self.incremental_thread.train_result_pic_path
        highest_acc = self.incremental_thread.highest_acc
        highest_val_acc = self.incremental_thread.highest_val_acc
        best_model_path = self.incremental_thread.best_model_path

        train_result_pic = QLabel()
        train_result_pic.setPixmap(QPixmap(train_result_pic_path))
        train_result_pic.setScaledContents(True)
        train_result_pic.setMaximumSize(450, 450)
        train_result_pic.setAlignment(Qt.AlignCenter)
        train_result_pic_title = QLabel("训练结果(Accuracy and Loss)")
        train_result_pic_title.setAlignment(Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.train_result_pic_layout.addWidget(train_result_pic, Qt.AlignCenter,
                                                                               Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.train_result_pic_layout.addWidget(train_result_pic_title)
        self.setup_main_window.ui.load_pages.train_result_pic_frame.setStyleSheet(
            "background:{}".format(self.setup_main_window.themes["app_color"]["text_description"]))
        self.setup_main_window.ui.load_pages.train_result_frame.show()

        self.update_latest_train_result_pic(data_type=self.training_data_type, train_result_pic_path=train_result_pic_path)

        # 如果划分了测试集，就进行测试
        if self.is_split_test_set is True and self.split_out_rate != 0:
            self.begin_test_model(test_set_dir=self.test_data_dir,
                                  data_type=self.training_data_type,
                                  model_path=best_model_path)

        self.process_best_model_info(data_type=self.training_data_type,
                                     highest_acc=highest_acc,
                                     highest_val_acc=highest_val_acc,
                                     best_model_path=best_model_path)

    # 更新最新的训练图（通过覆盖）、更新home页面中的展示的最新训练结果图
    def update_latest_train_result_pic(self, data_type, train_result_pic_path):
        save_dir = "images"
        save_sub_dir = os.path.join(save_dir, "metrics_images")
        pic_name = ""
        if data_type == "AFM":
            pic_name = "metric_afm.png"
        elif data_type == "SEM":
            pic_name = "metric_sem.png"
        elif data_type == "SAXS":
            pic_name = "metric_saxs.png"
        elif data_type == "WAXD":
            pic_name = "metric_waxd.png"
        else:
            return
        pic_path = os.path.join(save_sub_dir, pic_name)
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        if not os.path.isdir(save_sub_dir):
            os.mkdir(save_sub_dir)
        shutil.copy(train_result_pic_path, pic_path)
        self.refresh_home_metric_pictures()

    def refresh_home_metric_pictures(self):
        for i in range(0, self.setup_main_window.ui.load_pages.home_metric_layout.count()):
            self.setup_main_window.ui.load_pages.home_metric_layout.itemAt(i).widget().deleteLater()
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
        self.setup_main_window.ui.load_pages.home_metric_layout.addWidget(home_tab)

    def process_best_model_info(self, data_type, highest_acc, highest_val_acc, best_model_path):
        best_model_path = best_model_path.replace("\\", "/")
        if data_type == "AFM":
            if judge_is_best_model(data_type, highest_val_acc, highest_acc):
                self.best_model_info["afm_model"]["best_accuracy"] = highest_acc
                self.best_model_info["afm_model"]["best_val_accuracy"] = highest_val_acc
                self.best_model_info["afm_model"]["best_model_path"] = best_model_path
                write_json_file("best_model.json", self.best_model_info)
            else:
                return
        elif data_type == "SEM":
            if judge_is_best_model(data_type, highest_val_acc, highest_acc):
                self.best_model_info["sem_model"]["best_accuracy"] = highest_acc
                self.best_model_info["sem_model"]["best_val_accuracy"] = highest_val_acc
                self.best_model_info["sem_model"]["best_model_path"] = best_model_path
                write_json_file("best_model.json", self.best_model_info)
            else:
                return
        elif data_type == "SAXS":
            if judge_is_best_model(data_type, highest_val_acc, highest_acc):
                self.best_model_info["saxs_model"]["best_accuracy"] = highest_acc
                self.best_model_info["saxs_model"]["best_val_accuracy"] = highest_val_acc
                self.best_model_info["saxs_model"]["best_model_path"] = best_model_path
                write_json_file("best_model.json", self.best_model_info)
            else:
                return
        elif data_type == "WAXD":
            if judge_is_best_model(data_type, highest_val_acc, highest_acc):
                self.best_model_info["waxd_model"]["best_accuracy"] = highest_acc
                self.best_model_info["waxd_model"]["best_val_accuracy"] = highest_val_acc
                self.best_model_info["waxd_model"]["best_model_path"] = best_model_path
                write_json_file("best_model.json", self.best_model_info)
            else:
                return
        else:
            return
        # 绘制最佳模型的直方图
        draw_best_model_hist(best_model_json_path="best_model.json", pic_save_dir="images")
        self.refresh_home_best_model(data_type=data_type, best_model_path=best_model_path)

    def refresh_home_best_model(self, data_type, best_model_path):
        self.setup_main_window.best_model_pic.setPixmap(QPixmap("images/best_model_hist.png"))
        if data_type == "AFM":
            self.setup_main_window.best_afm_path.setText(best_model_path)
        elif data_type == "SEM":
            self.setup_main_window.best_sem_path.setText(best_model_path)
        elif data_type == "SAXS":
            self.setup_main_window.best_saxs_path.setText(best_model_path)
        elif data_type == "WAXD":
            self.setup_main_window.best_waxd_path.setText(best_model_path)
        else:
            return

    def split_train_to_test(self):
        data_set_split_out(self.training_data_dir, self.test_data_dir, self.split_out_rate)
        data_set_dir = self.get_data_set_dir(self.training_data_dir)
        self.home_page_functions.change_table_content(data_set_dir)

    def get_data_set_dir(self, src_dir):
        if src_dir[-1] == "\\" or src_dir[-1] == "/":
            src_dir = src_dir[:-1]
        data_set_dir = os.path.dirname(os.path.dirname(src_dir))
        return data_set_dir

    def begin_normal_training(self):
        self.setup_main_window.train_text_edit.setText("")

        self.sm = Stream()
        self.sm.newText.connect(self.onUpdateText)
        sys.stdout = self.sm
        # sys.stderr = self.sm

        if self.is_split_test_set is True:
            self.split_train_to_test()

        self.train_thread.training_data_type = self.training_data_type
        self.train_thread.training_data_dir = self.training_data_dir
        self.train_thread.model_save_dir = self.model_save_dir
        self.train_thread.epochs = self.epochs
        self.train_thread.batchsize = self.batchsize
        self.train_thread.validation_set_rate = self.validation_set_rate
        self.train_thread.learning_rate = self.learning_rate
        self.train_thread.lr_decay_steps = self.lr_decay_steps
        self.train_thread.lr_decay_rate = self.lr_decay_rate
        self.train_thread.dropout_rate = self.dropout_rate

        # click_off: 控制TensorFlow中fit的运行与否
        self.train_thread.callback.click_off = False
        self.train_thread.is_on = True
        self.train_thread.start()

        self.is_stop_training = False

        self.setup_main_window.back_btn_in_train_info_page.hide()
        self.setup_main_window.retraining_btn.hide()
        self.setup_main_window.stop_training_btn.show()
        # 等待进程运行完毕
        # loop = QEventLoop()
        # loop.exec_()

    def begin_incremental_training(self):
        self.setup_main_window.train_text_edit.setText("")

        self.sm = Stream()
        self.sm.newText.connect(self.onUpdateText)
        sys.stdout = self.sm

        if self.is_split_test_set is True:
            self.split_train_to_test()

        self.incremental_thread.training_data_type = self.training_data_type
        self.incremental_thread.training_data_dir = self.training_data_dir
        self.incremental_thread.model_save_dir = self.model_save_dir
        self.incremental_thread.epochs = self.epochs
        self.incremental_thread.batchsize = self.batchsize
        self.incremental_thread.validation_set_rate = self.validation_set_rate
        self.incremental_thread.learning_rate = self.learning_rate
        self.incremental_thread.lr_decay_steps = self.lr_decay_steps
        self.incremental_thread.lr_decay_rate = self.lr_decay_rate
        self.incremental_thread.pretrained_model = self.pretrained_model

        # click_off: 控制TensorFlow中fit的运行与否
        self.incremental_thread.callback.click_off = False
        self.incremental_thread.is_on = True
        self.incremental_thread.start()

        self.is_stop_training = False

        self.setup_main_window.back_btn_in_train_info_page.hide()
        self.setup_main_window.retraining_btn.hide()
        self.setup_main_window.stop_training_btn.show()

    def stop_normal_training(self):
        print('中止训练')
        self.is_stop_training = True
        self.train_thread.is_on = False
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.train_thread.handle, str(self.train_thread.currentThread()))
        self.train_thread.callback.click_off = True
        sys.stdout = sys.__stdout__

    def stop_incremental_training(self):
        print('中止训练')
        self.is_stop_training = True
        self.incremental_thread.is_on = False
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.incremental_thread.handle, str(self.incremental_thread.currentThread()))
        self.incremental_thread.callback.click_off = True
        sys.stdout = sys.__stdout__

    def onUpdateText(self, text):
        """将控制台输出到TextEdit中的策略."""
        cursor = self.setup_main_window.train_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        text = text.replace('\b', '')
        cursor.insertText(text)
        self.setup_main_window.train_text_edit.setTextCursor(cursor)
        self.setup_main_window.train_text_edit.ensureCursorVisible()

    def begin_test_model(self, test_set_dir, data_type, model_path):
        self.sm = Stream()
        self.sm.newText.connect(self.onUpdateText)
        sys.stdout = self.sm

        self.test_model_thread.test_set_dir = test_set_dir
        self.test_model_thread.model_path = os.path.normpath(model_path)
        self.test_model_thread.data_type = data_type

        self.test_model_thread.is_on = True
        self.test_model_thread.start()

    def test_model_finish_process(self):
        heatmap_save_path = self.test_model_thread.heatmap_save_path
        test_accuracy = self.test_model_thread.test_accuracy
        self.show_test_result(test_set_dir=self.test_data_dir,
                              heatmap_save_path=heatmap_save_path,
                              test_accuracy=test_accuracy)
        QMessageBox.about(self.setup_main_window, '提示', '训练完成!')
        sys.stdout = sys.__stdout__

    def show_test_result(self, test_set_dir, heatmap_save_path, test_accuracy):
        # 获得刚训练的模型路径
        # heatmap_save_path, test_accuracy = test_model(test_data_dir=test_set_dir, model_path=model_path, data_type=data_type)

        test_info_box_test_set = QHBoxLayout()
        test_set_data_nums_label_l = QLabel("测试集谱图数量: ")
        test_set_data_nums_label_l.setStyleSheet("font:12px")
        test_set_data_nums_label_r = QLabel()
        test_set_data_nums_label_l.setStyleSheet("font:12px")
        test_set_data_nums_label_r.setStyleSheet("color:white")
        test_info_box_test_set.addWidget(test_set_data_nums_label_l)
        test_info_box_test_set.addWidget(test_set_data_nums_label_r)
        test_info_box_test_set.addStretch(1)
        self.setup_main_window.ui.load_pages.test_set_info_layout.addLayout(test_info_box_test_set)

        label_list = os.listdir(test_set_dir)
        total_nums = 0
        for label in label_list:
            label_dir = os.path.join(test_set_dir, label)
            img_list = os.listdir(label_dir)
            img_nums = len(img_list)
            total_nums = total_nums + img_nums

            test_info_box_label_dir = QHBoxLayout()
            data_nums_label_l = QLabel("  {}年谱图数量: ".format(label))
            data_nums_label_l.setStyleSheet("font:12px")
            data_nums_label_r = QLabel(str(img_nums) + " 张")
            data_nums_label_r.setStyleSheet("font:12px")
            data_nums_label_r.setStyleSheet("color:white")
            test_info_box_label_dir.addWidget(data_nums_label_l)
            test_info_box_label_dir.addWidget(data_nums_label_r)
            test_info_box_label_dir.addStretch(1)
            self.setup_main_window.ui.load_pages.test_set_info_layout.addLayout(test_info_box_label_dir)
        test_set_data_nums_label_r.setText(str(total_nums) + " 张")

        test_info_box_accuracy = QHBoxLayout()
        accuracy_label_l = QLabel("准确率: ")
        accuracy_label_l.setStyleSheet("font:12px")
        accuracy_label_r = QLabel(str(test_accuracy))
        accuracy_label_l.setStyleSheet("font:12px")
        accuracy_label_r.setStyleSheet("color:white")
        test_info_box_accuracy.addWidget(accuracy_label_l)
        test_info_box_accuracy.addWidget(accuracy_label_r)
        test_info_box_accuracy.addStretch(1)
        self.setup_main_window.ui.load_pages.test_set_info_layout.addLayout(test_info_box_accuracy)

        test_result_pic = QLabel("heatmap")
        test_result_pic.setPixmap(QPixmap(heatmap_save_path))
        test_result_pic.setScaledContents(True)
        test_result_pic.setMaximumSize(375, 300)
        test_result_pic_title = QLabel("混淆矩阵(Confusion Matrix)")
        test_result_pic_title.setAlignment(Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.test_set_info_pic_layout.addWidget(test_result_pic, Qt.AlignCenter,
                                                                                Qt.AlignCenter)
        self.setup_main_window.ui.load_pages.test_set_info_pic_layout.addWidget(test_result_pic_title)

        self.setup_main_window.ui.load_pages.test_set_info_frame.setStyleSheet(
            "background:{}".format(self.setup_main_window.themes["app_color"]["text_description"]))
        self.setup_main_window.ui.load_pages.test_set_info_pic_frame.setStyleSheet(
            "background:{}".format(self.setup_main_window.themes["app_color"]["text_description"]))
        self.setup_main_window.ui.load_pages.test_result_frame.show()

    def stop_training_btn_event(self):
        stop_flag = QMessageBox.question(self.setup_main_window, '提示', '确定中止吗，中止后需重新训练!',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if stop_flag == QMessageBox.Yes:
            if self.is_incremental_train is True:
                self.stop_incremental_training()
            else:
                self.stop_normal_training()
            self.setup_main_window.back_btn_in_train_info_page.show()
            self.setup_main_window.retraining_btn.show()
            self.setup_main_window.stop_training_btn.hide()
        else:
            return

    def back_to_net_setting(self):
        back_flag = QMessageBox.question(self.setup_main_window, '提示', '确定返回吗!', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if back_flag == QMessageBox.Yes:
            MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_train_net_setting)
        else:
            return

    def back_to_main_in_page_train_info(self):
        back_flag = QMessageBox.question(self.setup_main_window, '提示', '确定返回吗,返回后会失去此次训练信息!',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if back_flag == QMessageBox.Yes:
            # 将stdout设置回默认值.
            if self.is_incremental_train is True:
                self.stop_incremental_training()
            else:
                self.stop_normal_training()
            self.setup_main_window.train_text_edit.setText("")
            MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_home)
            self.setup_main_window.ui.left_menu.select_only_one("btn_home")
            self.clear_test_and_train_result()
        else:
            return

    def clear_test_and_train_result(self):
        for i in range(0, self.setup_main_window.ui.load_pages.test_set_info_layout.count()):
            self.setup_main_window.ui.load_pages.test_set_info_layout.itemAt(i).layout().deleteLater()
        for i in range(0, self.setup_main_window.ui.load_pages.test_set_info_pic_layout.count()):
            self.setup_main_window.ui.load_pages.test_set_info_pic_layout.itemAt(i).widget().deleteLater()
        for i in range(0, self.setup_main_window.ui.load_pages.train_result_pic_layout.count()):
            self.setup_main_window.ui.load_pages.train_result_pic_layout.itemAt(i).widget().deleteLater()
        self.setup_main_window.ui.load_pages.test_result_frame.hide()
        self.setup_main_window.ui.load_pages.train_result_frame.hide()
