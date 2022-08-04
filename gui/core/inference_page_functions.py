import sqlite3
import time

from qt_core import *
import json
import os
import cv2
from gui.widgets.py_image_widget import PyImageWidget
from gui.widgets.py_tab import PyTab
from ..uis.windows.main_window.functions_main_window import *
from predict import *


class InferencePageFunctions:

    def __init__(self, setup_main_window):
        self.num_img = 0  # 打开的图片的数量
        self.max_num_img = 8  # 最多一次上传8张图片
        self.setup_main_window = setup_main_window
        self.img_path = []  # 图片地址
        self.img_type = []  # 图片类型
        self.img_name = []  # 图片名称
        self.model_path = self.get_path()  # 谱图和模型路径
        self.widget_list = []  # widget list 保存生成的image_widget控件，用于刷新时删除界面中的之前生成的控件
        self.predict_thread = PredictThread(img_path=self.img_path, img_type=self.img_type, model_path=self.model_path)
        self.predict_thread.signal.connect(self.deal_predict_result)
        self.result_list = []  # 最终结果存入数据库
        self.inference_page_tab = None
        # self.msg_thread = MsgThread()

    # 获取图片路径
    def get_img_path(self):
        img_path, _ = QFileDialog.getOpenFileName(
            self.setup_main_window.ui.central_widget,
            "选择你要上传的图片",  # 标题
            r"data",  # 起始目录
            "图片类型 (*.jpg *jpeg *.png *.jpe *.tif *.tiff *.bmp *.tbi *.jfif)"  # 选择类型过滤项，过滤内容在括号中
        )
        if img_path != '':
            if img_path in self.img_path:
                QMessageBox.warning(
                    self.setup_main_window,
                    '警告',
                    '不要重复选择同一张图片！')
            else:
                self.add_btn(img_path)

    # 获取图片名称
    def get_img_name(self, img_path):
        for path in img_path:
            self.img_name.append(path.split('/')[-1].split('.')[0])

    # 添加图片
    # 删除添加按钮后重新添加，使按钮每次都能排在最后
    def add_btn(self, img_path):
        image_widget = PyImageWidget(img_path)
        self.widget_list.append(image_widget)
        image_widget.combox.currentIndexChanged.connect(lambda: self.choose_image_type(image_widget))
        image_widget.change_btn.clicked.connect(lambda: self.change_btn_clicked(image_widget))
        image_widget.delete_btn.clicked.connect(lambda: self.delete_btn_clicked(image_widget))
        self.setup_main_window.ui.load_pages.inference_layout.addWidget(image_widget)
        self.setup_main_window.ui.load_pages.inference_layout.removeWidget(self.setup_main_window.choose_img_btn)
        self.num_img += 1
        self.img_path.append(img_path)  # 添加图片地址到列表
        tmp_img_type = self.get_img_type(img_path)
        self.img_type.append(tmp_img_type)
        if tmp_img_type == "AFM":
            image_widget.combox.setCurrentText("表面AFM谱图")
        elif tmp_img_type == "SEM":
            image_widget.combox.setCurrentText("表面SEM谱图")
        elif tmp_img_type == "SAXS":
            image_widget.combox.setCurrentText("2D-SAXS谱图")
        elif tmp_img_type == "WAXD":
            image_widget.combox.setCurrentText("2D-WAXD谱图")
        else:
            image_widget.combox.setCurrentText("表面AFM谱图")

        if self.num_img < self.max_num_img:  # 如果当前选择的图片数量小于最大选择数量，则重新添加按钮，否则移除
            self.setup_main_window.ui.load_pages.inference_layout.addWidget(self.setup_main_window.choose_img_btn)
        else:
            self.setup_main_window.ui.load_pages.inference_layout.addWidget(self.setup_main_window.choose_img_btn)
            self.setup_main_window.choose_img_btn.hide()  # removeWidget无法彻底删除控件，使用deleteLater可以彻底删除

    # 获取图片
    def change_btn_clicked(self, image_widget):
        path, _ = QFileDialog.getOpenFileName(
            self.setup_main_window.ui.central_widget,
            "选择你要上传的图片",  # 标题
            r"data",  # 起始目录
            "图片类型 (*.jpg *jpeg *.png *.jpe *.tif *.tiff *.bmp *.tbi *.jfif)"  # 选择类型过滤项，过滤内容在括号中
        )
        if path != '':
            # 新图片地址替换旧图片地址
            if path in self.img_path:
                QMessageBox.warning(
                    self.setup_main_window,
                    '警告',
                    '不要重复选择同一张图片！')
            else:
                image_widget_index = self.img_path.index(image_widget.image_path)
                self.img_path[image_widget_index] = path
                image_widget.image_path = path
                image_widget.image.setPixmap(QPixmap(path))
                tmp_img_type = self.get_img_type(path)
                self.img_type[image_widget_index] = tmp_img_type
                if tmp_img_type == "AFM":
                    image_widget.combox.setCurrentText("表面AFM谱图")
                elif tmp_img_type == "SEM":
                    image_widget.combox.setCurrentText("表面SEM谱图")
                elif tmp_img_type == "SAXS":
                    image_widget.combox.setCurrentText("2D-SAXS谱图")
                elif tmp_img_type == "WAXD":
                    image_widget.combox.setCurrentText("2D-WAXD谱图")
                else:
                    image_widget.combox.setCurrentText("表面AFM谱图")

    # 删除组件
    def delete_btn_clicked(self, image_widget):
        del self.img_type[self.img_path.index(image_widget.image_path)]
        self.img_path.remove(image_widget.image_path)  # 删除控件前，将被删除的图片地址从地址列表中移除
        image_widget.deleteLater()
        self.num_img -= 1

    def get_img_type(self, img_path):
        src = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # src = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = src
        cv2.cvtColor(src, cv2.COLOR_BGR2HSV, img)
        hue_sum = 0.0
        hue_mean = 0.0
        for i in range(len(img)):
            for j in range(len(img[0])):
                hue_sum = hue_sum + img[i][j][0]
        hue_mean = hue_sum / (len(img) * len(img[0]))
        # 新范围
        if hue_mean < 16 and hue_mean > 10:
            return "AFM"
        elif hue_mean < 2 or hue_mean > 175:
            return "SEM"
        elif hue_mean < 119 and hue_mean > 112:
            return "SAXS"
        elif hue_mean < 9 and hue_mean > 3:
            return "WAXD"

    # 更改图片类型
    def choose_image_type(self, image_widget):
        txt = image_widget.combox.currentText()
        if txt != '表面AFM谱图':
            if txt == '表面SEM谱图':
                self.img_type[self.img_path.index(image_widget.image_path)] = 'SEM'
            elif txt == '2D-SAXS谱图':
                self.img_type[self.img_path.index(image_widget.image_path)] = 'SAXS'
            elif txt == '2D-WAXD谱图':
                self.img_type[self.img_path.index(image_widget.image_path)] = 'WAXD'

    # 从json文件中获取谱图和模型路径
    def get_path(self):
        # ///////////////////////////////////////////////////////////////
        json_file = "model_path.json"
        app_path = os.path.abspath(os.getcwd())
        model_path = os.path.normpath(os.path.join(app_path, json_file))
        if not os.path.isfile(model_path):
            print(f"WARNING: \"model_path.json\" not found! check in the folder {model_path}")

        with open(model_path, "r", encoding='utf-8') as reader:
            paths = json.loads(reader.read())
        return paths

    # 选择谱图数据路径
    def choose_data_path(self, widget):
        path = QFileDialog.getExistingDirectory(
            self.setup_main_window.ui.central_widget,
            "选择路径",  # 标题
            r".",  # 起始目录
        )
        if path != '':
            print(widget)
            widget.setText(path)
            print(path)

    # 选择模型
    def choose_model(self, widget):
        path, _ = QFileDialog.getOpenFileName(
            self.setup_main_window.ui.central_widget,
            "选择模型",  # 标题
            r"models",  # 起始目录
            "模型类型 (*.h5)"  # 选择类型过滤项，过滤内容在括号中
        )
        if path != '':
            widget.setText(path)
            print(path)

    # 检查当前页面内容是否正常
    def check(self):
        if self.num_img == 0:
            QMessageBox.warning(
                self.setup_main_window,
                '警告',
                '没有选择图片！')
        # 获取路径，保存图片路径和模型路径
        else:
            # 获取谱图和模型路径
            self.model_path['inference_result_path'] = self.setup_main_window.inference_result_path.text()
            self.model_path['afm_model_path'] = self.setup_main_window.afm_model_path.text()
            self.model_path['sem_model_path'] = self.setup_main_window.sem_model_path.text()
            self.model_path['saxs_model_path'] = self.setup_main_window.saxs_model_path.text()
            self.model_path['waxd_model_path'] = self.setup_main_window.waxd_model_path.text()
            # 检查谱图路径是否存在，若无则创建
            infer_result_path = os.path.normpath(os.path.abspath(self.model_path['inference_result_path']))
            if not os.path.exists(infer_result_path):
                os.mkdir(infer_result_path)
            if not os.path.exists(os.path.join(infer_result_path, 'AFM')):
                os.mkdir(os.path.join(infer_result_path, 'AFM'))
            if not os.path.exists(os.path.join(infer_result_path, 'SEM')):
                os.mkdir(os.path.join(infer_result_path, 'SEM'))
            if not os.path.exists(os.path.join(infer_result_path, 'SAXS')):
                os.mkdir(os.path.join(infer_result_path, 'SAXS'))
            if not os.path.exists(os.path.join(infer_result_path, 'WAXD')):
                os.mkdir(os.path.join(infer_result_path, 'WAXD'))

            self.predict_thread.img_path = self.img_path
            self.predict_thread.img_type = self.img_type
            self.predict_thread.model_path = self.model_path
            self.predict_thread.is_on = True
            self.predict_thread.start()
            # # 获取图片地址
            # print(self.img_path)  # debug
            # print(self.img_type)
            # # 获取谱图和模型路径
            # self.model_path['inference_result_path'] = self.setup_main_window.inference_result_path.text()
            # self.model_path['afm_model_path'] = self.setup_main_window.afm_model_path.text()
            # self.model_path['sem_model_path'] = self.setup_main_window.sem_model_path.text()
            # self.model_path['saxs_model_path'] = self.setup_main_window.saxs_model_path.text()
            # self.model_path['waxd_model_path'] = self.setup_main_window.waxd_model_path.text()
            # print(self.model_path)  # debug
            #
            # self.get_img_name(self.img_path)
            #
            # # 检查谱图路径是否存在，若无则创建
            # infer_result_path = os.path.normpath(os.path.abspath(self.model_path['inference_result_path']))
            # if not os.path.exists(infer_result_path):
            #     os.mkdir(infer_result_path)
            # if not os.path.exists(os.path.join(infer_result_path, 'AFM')):
            #     os.mkdir(os.path.join(infer_result_path, 'AFM'))
            # if not os.path.exists(os.path.join(infer_result_path, 'SEM')):
            #     os.mkdir(os.path.join(infer_result_path, 'SEM'))
            # if not os.path.exists(os.path.join(infer_result_path, 'SAXS')):
            #     os.mkdir(os.path.join(infer_result_path, 'SAXS'))
            # if not os.path.exists(os.path.join(infer_result_path, 'WAXD')):
            #     os.mkdir(os.path.join(infer_result_path, 'WAXD'))
            #
            # self.setup_main_window.check_btn.setText("正在检测中...")
            # # self.setup_main_window.check_btn.setStyleSheet("background-color:#088A08;color:white;")
            #
            # # 获取预测的结果后生成tab
            # inference_page_tab = PyTab(self.get_data())
            # inference_page_tab.setStyleSheet(
            #     "QTabWidget {border-top-color: rgba(255, 255, 255, 0);}"
            #     "QTabWidget::pane{top:-1px;}"
            #     "QTabBar::tab {"
            #     "min-width:100px;"
            #     "color: #8a95aa;"
            #     "background-color: #1e2229;"
            #     "border: 2px solid #1b1e23;"
            #     "border-top-left-radius: 10px;"
            #     "border-top-right-radius: 10px;padding:5px;"
            #     "padding-right: 5px;"
            #     "}"
            #     "QTabBar::tab:!selected {margin-top: 5px;} "
            #     "QTabBar::tab:selected {color: #568af2;}; "
            # )
            # self.setup_main_window.ui.load_pages.inference_tab_layout.addWidget(inference_page_tab)
            #
            # self.setup_main_window.check_btn.setText("开始检测")
            # # self.setup_main_window.check_btn.setStyleSheet("background-color:#0B610B;color:#8a95aa;")
            #
            # ## process bar
            # QMessageBox.information(
            #     self.setup_main_window,
            #     '提示',
            #     '检测完成')
            # ##
            #
            # # 跳转到结果页面
            # MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_inference_2)

    # def get_data(self):
    #     result_list = []
    #     self.msg_box = QMessageBox()
    #     for i, item in enumerate(self.img_path):
    #         img_type = self.img_type[i]
    #         img_name = self.img_name[i]
    #         model_path = ""
    #         if img_type == "AFM":
    #             model_path = self.model_path["afm_model_path"]
    #         elif img_type == "SEM":
    #             model_path = self.model_path["sem_model_path"]
    #         elif img_type == "SAXS":
    #             model_path = self.model_path["saxs_model_path"]
    #         elif img_type == "WAXD":
    #             model_path = self.model_path["waxd_model_path"]
    #         print(model_path)
    #         predict_result, confidence, result_path, feature1_path, feature2_path, src_img_path = predict_image(img_path=item,
    #                                                                                               model_path=model_path,
    #                                                                                               img_type=img_type,
    #                                                                                               save_folder=
    #                                                                                               self.model_path[
    #                                                                                                   "inference_result_path"])
    #         predict_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
    #         self.inference_result_to_database(self.setup_main_window.history_page_functions, (src_img_path, img_type, predict_time, predict_result, img_name, confidence,
    #                                            result_path, feature1_path, feature2_path))
    #         result_list.append((src_img_path, img_type, predict_time, predict_result, img_name, confidence, result_path,
    #                             feature1_path, feature2_path))
    #     return result_list

    # 检测结果写入数据库history.db
    def inference_result_to_database(self, history_page_functions, data):
        try:
            sql = f"INSERT INTO HISTORY(img_path, img_type, infer_time, predict_result, img_name, confidence, result_path, feature1_path, feature2_path) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}', '{data[7]}', '{data[8]}');"
            history_page_functions.cursor.execute(sql)
            history_page_functions.conn.commit()
        except sqlite3.Error as e:
            print(e)

    # 刷新界面
    def refresh(self):
        self.num_img = 0
        self.img_path = []  # 清除图片地址
        self.img_type = []  # 清除图片类型
        for widget in self.widget_list:  # 删除控件
            widget.deleteLater()
        self.widget_list = []
        self.result_list = []
        if self.inference_page_tab is not None:
            self.inference_page_tab.deleteLater()
            self.inference_page_tab = None

            print('删除tab控件')
        # widget_count = self.setup_main_window.ui.load_pages.inference_tab_layout.count()
        # if widget_count != 0:
        #     for i in range(0, widget_count):
        #         self.setup_main_window.ui.load_pages.inference_tab_layout.itemAt(i).widget().deleteLater()

        # 重置谱图和模型路径
        model_path = self.get_path()
        self.setup_main_window.inference_result_path.setText(model_path['inference_result_path'])
        self.setup_main_window.afm_model_path.setText(model_path['afm_model_path'])
        self.setup_main_window.sem_model_path.setText(model_path['sem_model_path'])
        self.setup_main_window.saxs_model_path.setText(model_path['saxs_model_path'])
        self.setup_main_window.waxd_model_path.setText(model_path['waxd_model_path'])
        self.setup_main_window.choose_img_btn.show()

        print('Inference Page is clicked! ')

    def deal_predict_result(self, i, data):
        print(self.predict_thread.error_flag)
        if self.predict_thread.error_flag:
            self.predict_thread.is_on = False
            self.progress.close()
            # 完成任务后删除进度条
            self.progress.deleteLater()
            self.result_list = []
            QMessageBox.warning(
                self.setup_main_window,
                f'第{i}张图片出现错误',
                f"{self.predict_thread.error_info}"
            )
            self.predict_thread.error_flag = False
            return
        if data is None:
            # 进度条
            # 第一次进行初始化
            self.progress = QProgressDialog(self.setup_main_window)
            pb = QProgressBar(self.progress)
            pb.setFormat('%v/%m')
            self.progress.setBar(pb)
            self.progress.setWindowFlag(Qt.FramelessWindowHint)
            # process.setAttribute(Qt.WA_TranslucentBackground)
            self.progress.setFixedSize(500, 100)
            self.progress.setAutoReset(False)
            self.progress.setAutoClose(False)
            self.progress.setCancelButtonText(None)
            self.progress.setRange(0, self.num_img)
            # 设置锁定于当前窗口
            self.progress.setModal(True)
            self.progress.setLabelText(f'正在检测第{i}张图片...\n(请等待检测完成)')
            self.progress.setValue(i)
            self.progress.show()

        else:
            # 进度条
            self.progress.setLabelText(f'正在检测第{i}张图片...\n(请等待检测完成)')
            self.progress.setValue(i)
            # 将结果写入数据库
            self.inference_result_to_database(self.setup_main_window.history_page_functions, data)
            # 将结果存入result_list中，用于生成tab
            self.result_list.append(data)
            if self.progress.value() == self.num_img:
                QMessageBox.information(
                    self.setup_main_window,
                    '提示',
                    '检测完成！'
                )
                self.progress.close()
                # 完成任务后删除进度条
                self.progress.deleteLater()

                # 这里获取预测的结果后生成tab
                self.inference_page_tab = PyTab(self.result_list)
                self.inference_page_tab.setStyleSheet(
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
                self.setup_main_window.ui.load_pages.inference_tab_layout.addWidget(self.inference_page_tab)
                # 跳转到结果页面
                MainFunctions.set_page(self.setup_main_window, self.setup_main_window.ui.load_pages.page_inference_2)


class PredictThread(QThread):
    signal = Signal(int, tuple)

    def __init__(self, img_path, img_type, model_path):
        super().__init__()
        self.img_path = img_path
        self.img_type = img_type
        self.model_path = model_path
        self.error_flag = False
        self.error_info = None
        self.is_on = False

    def run(self):
        # 这里执行predict并通过信号返回结果 (int, (data))
        while self.is_on is True:
            self.signal.emit(1, None)
            for i, item in enumerate(self.img_path):
                img_type = self.img_type[i]
                # 获取图片名称
                img_name = item.split('/')[-1].split('.')[0]
                # 获取模型路径
                model_path = ""
                if img_type == "AFM":
                    model_path = self.model_path["afm_model_path"]
                elif img_type == "SEM":
                    model_path = self.model_path["sem_model_path"]
                elif img_type == "SAXS":
                    model_path = self.model_path["saxs_model_path"]
                elif img_type == "WAXD":
                    model_path = self.model_path["waxd_model_path"]
                predict_result, confidence, result_path, feature1_path, feature2_path, src_img_path = None,None,None,None,None,None
                try:
                    predict_result, confidence, result_path, feature1_path, feature2_path, src_img_path = predict_image(
                        img_path=item,
                        model_path=model_path,
                        img_type=img_type,
                        save_folder=
                        self.model_path[
                            "inference_result_path"])
                except Exception as e:
                    self.error_info = e
                    self.error_flag = True
                predict_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
                self.signal.emit(i + 1, (src_img_path, img_type, predict_time, predict_result, img_name, confidence,
                                         result_path, feature1_path, feature2_path))
            self.is_on = False

