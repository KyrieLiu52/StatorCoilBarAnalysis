# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pagesIXHvLk.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(888, 570)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(0, 0, 0, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_history_2 = QWidget()
        self.page_history_2.setObjectName(u"page_history_2")
        self.page_history_2_layout = QVBoxLayout(self.page_history_2)
        self.page_history_2_layout.setSpacing(0)
        self.page_history_2_layout.setObjectName(u"page_history_2_layout")
        self.page_history_2_layout.setContentsMargins(0, 0, 0, 0)
        self.history_frame_2 = QFrame(self.page_history_2)
        self.history_frame_2.setObjectName(u"history_frame_2")
        self.history_frame_2.setFrameShape(QFrame.NoFrame)
        self.history_frame_2.setFrameShadow(QFrame.Raised)
        self.history_detail_layout = QVBoxLayout(self.history_frame_2)
        self.history_detail_layout.setSpacing(0)
        self.history_detail_layout.setObjectName(u"history_detail_layout")
        self.history_detail_layout.setContentsMargins(0, 0, 0, 0)

        self.page_history_2_layout.addWidget(self.history_frame_2)

        self.pages.addWidget(self.page_history_2)
        self.page_inference = QWidget()
        self.page_inference.setObjectName(u"page_inference")
        self.page_inference_layout = QVBoxLayout(self.page_inference)
        self.page_inference_layout.setObjectName(u"page_inference_layout")
        self.inference_frame = QFrame(self.page_inference)
        self.inference_frame.setObjectName(u"inference_frame")
        self.inference_frame.setFrameShape(QFrame.NoFrame)
        self.inference_frame.setFrameShadow(QFrame.Raised)
        self.inference_layout = QHBoxLayout(self.inference_frame)
        self.inference_layout.setObjectName(u"inference_layout")
        self.inference_layout.setContentsMargins(0, 0, 0, 0)

        self.page_inference_layout.addWidget(self.inference_frame, 0, Qt.AlignHCenter)

        self.model_path_frame = QFrame(self.page_inference)
        self.model_path_frame.setObjectName(u"model_path_frame")
        self.model_path_frame.setFrameShape(QFrame.NoFrame)
        self.model_path_frame.setFrameShadow(QFrame.Raised)
        self.model_path_layout = QGridLayout(self.model_path_frame)
        self.model_path_layout.setObjectName(u"model_path_layout")
        self.model_path_layout.setContentsMargins(0, 0, 0, 0)

        self.page_inference_layout.addWidget(self.model_path_frame)

        self.pages.addWidget(self.page_inference)
        self.page_inference_2 = QWidget()
        self.page_inference_2.setObjectName(u"page_inference_2")
        self.page_inference_2_layout = QVBoxLayout(self.page_inference_2)
        self.page_inference_2_layout.setObjectName(u"page_inference_2_layout")
        self.inference_frame_2 = QFrame(self.page_inference_2)
        self.inference_frame_2.setObjectName(u"inference_frame_2")
        self.inference_frame_2.setStyleSheet(u"")
        self.inference_frame_2.setFrameShape(QFrame.NoFrame)
        self.inference_frame_2.setFrameShadow(QFrame.Raised)
        self.inference_tab_layout = QHBoxLayout(self.inference_frame_2)
        self.inference_tab_layout.setSpacing(0)
        self.inference_tab_layout.setObjectName(u"inference_tab_layout")
        self.inference_tab_layout.setContentsMargins(0, 0, 0, 0)

        self.page_inference_2_layout.addWidget(self.inference_frame_2)

        self.pages.addWidget(self.page_inference_2)
        self.page_history = QWidget()
        self.page_history.setObjectName(u"page_history")
        self.page_history_layout = QVBoxLayout(self.page_history)
        self.page_history_layout.setObjectName(u"page_history_layout")
        self.frame_table = QFrame(self.page_history)
        self.frame_table.setObjectName(u"frame_table")
        self.frame_table.setMinimumSize(QSize(0, 40))
        self.frame_table.setFrameShape(QFrame.NoFrame)
        self.frame_table.setFrameShadow(QFrame.Raised)
        self.table_layout = QVBoxLayout(self.frame_table)
        self.table_layout.setSpacing(0)
        self.table_layout.setObjectName(u"table_layout")
        self.table_layout.setContentsMargins(0, 0, 0, 0)

        self.page_history_layout.addWidget(self.frame_table)

        self.frame_turn_page_btn = QFrame(self.page_history)
        self.frame_turn_page_btn.setObjectName(u"frame_turn_page_btn")
        self.frame_turn_page_btn.setMinimumSize(QSize(350, 40))
        self.frame_turn_page_btn.setMaximumSize(QSize(16777215, 40))
        self.frame_turn_page_btn.setFrameShape(QFrame.NoFrame)
        self.frame_turn_page_btn.setFrameShadow(QFrame.Raised)
        self.frame_turn_page_btn.setLineWidth(1)
        self.turn_page_btn_layout = QHBoxLayout(self.frame_turn_page_btn)
        self.turn_page_btn_layout.setSpacing(6)
        self.turn_page_btn_layout.setObjectName(u"turn_page_btn_layout")
        self.turn_page_btn_layout.setContentsMargins(0, 0, 0, 0)

        self.page_history_layout.addWidget(self.frame_turn_page_btn, 0, Qt.AlignHCenter)

        self.pages.addWidget(self.page_history)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_home.sizePolicy().hasHeightForWidth())
        self.page_home.setSizePolicy(sizePolicy)
        self.page_home.setStyleSheet(u"")
        self.page_home_layout = QVBoxLayout(self.page_home)
        self.page_home_layout.setSpacing(0)
        self.page_home_layout.setObjectName(u"page_home_layout")
        self.page_home_layout.setContentsMargins(5, 5, 5, 5)
        self.page_home_row_1 = QFrame(self.page_home)
        self.page_home_row_1.setObjectName(u"page_home_row_1")
        sizePolicy.setHeightForWidth(self.page_home_row_1.sizePolicy().hasHeightForWidth())
        self.page_home_row_1.setSizePolicy(sizePolicy)
        self.page_home_row_1.setFrameShape(QFrame.NoFrame)
        self.page_home_row_1.setFrameShadow(QFrame.Raised)
        self.page_home_row_1_layout = QHBoxLayout(self.page_home_row_1)
        self.page_home_row_1_layout.setObjectName(u"page_home_row_1_layout")
        self.best_model_frame = QFrame(self.page_home_row_1)
        self.best_model_frame.setObjectName(u"best_model_frame")
        self.best_model_frame.setStyleSheet(u"")
        self.best_model_frame.setFrameShape(QFrame.NoFrame)
        self.best_model_frame.setFrameShadow(QFrame.Raised)
        self.best_model_layout = QHBoxLayout(self.best_model_frame)
        self.best_model_layout.setObjectName(u"best_model_layout")

        self.page_home_row_1_layout.addWidget(self.best_model_frame)

        self.main_func_frame = QFrame(self.page_home_row_1)
        self.main_func_frame.setObjectName(u"main_func_frame")
        self.main_func_frame.setStyleSheet(u"")
        self.main_func_frame.setFrameShape(QFrame.StyledPanel)
        self.main_func_frame.setFrameShadow(QFrame.Raised)
        self.main_func_layout = QGridLayout(self.main_func_frame)
        self.main_func_layout.setObjectName(u"main_func_layout")

        self.page_home_row_1_layout.addWidget(self.main_func_frame)


        self.page_home_layout.addWidget(self.page_home_row_1)

        self.page_home_row_2 = QFrame(self.page_home)
        self.page_home_row_2.setObjectName(u"page_home_row_2")
        sizePolicy.setHeightForWidth(self.page_home_row_2.sizePolicy().hasHeightForWidth())
        self.page_home_row_2.setSizePolicy(sizePolicy)
        self.page_home_row_2.setFrameShape(QFrame.NoFrame)
        self.page_home_row_2.setFrameShadow(QFrame.Raised)
        self.page_home_row_2_layout = QHBoxLayout(self.page_home_row_2)
        self.page_home_row_2_layout.setObjectName(u"page_home_row_2_layout")
        self.metric_frame = QFrame(self.page_home_row_2)
        self.metric_frame.setObjectName(u"metric_frame")
        self.metric_frame.setStyleSheet(u"")
        self.metric_frame.setFrameShape(QFrame.NoFrame)
        self.metric_frame.setFrameShadow(QFrame.Raised)
        self.home_metric_layout = QVBoxLayout(self.metric_frame)
        self.home_metric_layout.setSpacing(0)
        self.home_metric_layout.setObjectName(u"home_metric_layout")
        self.home_metric_layout.setContentsMargins(0, 0, 0, 0)

        self.page_home_row_2_layout.addWidget(self.metric_frame)

        self.dataset_info_frame = QFrame(self.page_home_row_2)
        self.dataset_info_frame.setObjectName(u"dataset_info_frame")
        self.dataset_info_frame.setStyleSheet(u"")
        self.dataset_info_frame.setFrameShape(QFrame.StyledPanel)
        self.dataset_info_frame.setFrameShadow(QFrame.Raised)
        self.dataset_info_layout = QVBoxLayout(self.dataset_info_frame)
        self.dataset_info_layout.setObjectName(u"dataset_info_layout")

        self.page_home_row_2_layout.addWidget(self.dataset_info_frame)

        self.page_home_row_2_layout.setStretch(0, 1)
        self.page_home_row_2_layout.setStretch(1, 2)

        self.page_home_layout.addWidget(self.page_home_row_2)

        self.page_home_layout.setStretch(0, 1)
        self.page_home_layout.setStretch(1, 2)
        self.pages.addWidget(self.page_home)
        self.page_add_images = QWidget()
        self.page_add_images.setObjectName(u"page_add_images")
        self.page_add_images.setStyleSheet(u"")
        self.page_add_images_layout = QVBoxLayout(self.page_add_images)
        self.page_add_images_layout.setSpacing(0)
        self.page_add_images_layout.setObjectName(u"page_add_images_layout")
        self.page_add_images_layout.setContentsMargins(0, 0, 0, 0)
        self.add_images_scroll_area = QScrollArea(self.page_add_images)
        self.add_images_scroll_area.setObjectName(u"add_images_scroll_area")
        self.add_images_scroll_area.setStyleSheet(u"background: transparent;")
        self.add_images_scroll_area.setFrameShape(QFrame.NoFrame)
        self.add_images_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.add_images_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.add_images_scroll_area.setWidgetResizable(True)
        self.add_images_scroll_area_contents = QWidget()
        self.add_images_scroll_area_contents.setObjectName(u"add_images_scroll_area_contents")
        self.add_images_scroll_area_contents.setGeometry(QRect(0, 0, 128, 57))
        self.add_images_scroll_area_contents.setStyleSheet(u"background: transparent;")
        self.add_images_scroll_layout = QVBoxLayout(self.add_images_scroll_area_contents)
        self.add_images_scroll_layout.setSpacing(0)
        self.add_images_scroll_layout.setObjectName(u"add_images_scroll_layout")
        self.add_images_title_frame = QFrame(self.add_images_scroll_area_contents)
        self.add_images_title_frame.setObjectName(u"add_images_title_frame")
        self.add_images_title_frame.setMaximumSize(QSize(16777215, 200))
        self.add_images_title_frame.setFrameShape(QFrame.StyledPanel)
        self.add_images_title_frame.setFrameShadow(QFrame.Raised)
        self.add_images_title_layout = QHBoxLayout(self.add_images_title_frame)
        self.add_images_title_layout.setSpacing(0)
        self.add_images_title_layout.setObjectName(u"add_images_title_layout")
        self.add_images_title_layout.setContentsMargins(0, 0, 0, 0)
        self.add_images_title_label = QLabel(self.add_images_title_frame)
        self.add_images_title_label.setObjectName(u"add_images_title_label")
        self.add_images_title_label.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")

        self.add_images_title_layout.addWidget(self.add_images_title_label, 0, Qt.AlignHCenter)


        self.add_images_scroll_layout.addWidget(self.add_images_title_frame)

        self.add_images_content_frame = QFrame(self.add_images_scroll_area_contents)
        self.add_images_content_frame.setObjectName(u"add_images_content_frame")
        self.add_images_content_frame.setMinimumSize(QSize(0, 0))
        self.add_images_content_frame.setMaximumSize(QSize(16777215, 16777215))
        self.add_images_content_frame.setFrameShape(QFrame.NoFrame)
        self.add_images_content_frame.setFrameShadow(QFrame.Raised)
        self.add_images_grid_layout = QGridLayout(self.add_images_content_frame)
        self.add_images_grid_layout.setSpacing(0)
        self.add_images_grid_layout.setObjectName(u"add_images_grid_layout")
        self.add_images_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.add_images_scroll_layout.addWidget(self.add_images_content_frame)

        self.add_images_btn_frame = QFrame(self.add_images_scroll_area_contents)
        self.add_images_btn_frame.setObjectName(u"add_images_btn_frame")
        self.add_images_btn_frame.setMinimumSize(QSize(0, 0))
        self.add_images_btn_frame.setMaximumSize(QSize(16777215, 200))
        self.add_images_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.add_images_btn_frame.setFrameShadow(QFrame.Raised)
        self.add_btn_layout = QHBoxLayout(self.add_images_btn_frame)
        self.add_btn_layout.setSpacing(0)
        self.add_btn_layout.setObjectName(u"add_btn_layout")
        self.add_btn_layout.setContentsMargins(0, 0, 0, 0)

        self.add_images_scroll_layout.addWidget(self.add_images_btn_frame)

        self.add_images_scroll_area.setWidget(self.add_images_scroll_area_contents)

        self.page_add_images_layout.addWidget(self.add_images_scroll_area)

        self.pages.addWidget(self.page_add_images)
        self.page_train_base_setting = QWidget()
        self.page_train_base_setting.setObjectName(u"page_train_base_setting")
        self.page_train_base_setting.setStyleSheet(u"")
        self.page_train_base_setting_layout = QVBoxLayout(self.page_train_base_setting)
        self.page_train_base_setting_layout.setObjectName(u"page_train_base_setting_layout")
        self.train_base_setting_title_frame = QFrame(self.page_train_base_setting)
        self.train_base_setting_title_frame.setObjectName(u"train_base_setting_title_frame")
        self.train_base_setting_title_frame.setMaximumSize(QSize(16777215, 200))
        self.train_base_setting_title_frame.setFrameShape(QFrame.StyledPanel)
        self.train_base_setting_title_frame.setFrameShadow(QFrame.Raised)
        self.train_base_setting_title_layout = QHBoxLayout(self.train_base_setting_title_frame)
        self.train_base_setting_title_layout.setObjectName(u"train_base_setting_title_layout")
        self.train_base_setting_title_label = QLabel(self.train_base_setting_title_frame)
        self.train_base_setting_title_label.setObjectName(u"train_base_setting_title_label")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        self.train_base_setting_title_label.setFont(font)
        self.train_base_setting_title_label.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")

        self.train_base_setting_title_layout.addWidget(self.train_base_setting_title_label, 0, Qt.AlignHCenter)


        self.page_train_base_setting_layout.addWidget(self.train_base_setting_title_frame)

        self.train_base_setting_content_frame = QFrame(self.page_train_base_setting)
        self.train_base_setting_content_frame.setObjectName(u"train_base_setting_content_frame")
        self.train_base_setting_content_frame.setMinimumSize(QSize(0, 320))
        self.train_base_setting_content_frame.setFrameShape(QFrame.StyledPanel)
        self.train_base_setting_content_frame.setFrameShadow(QFrame.Raised)
        self.train_base_setting_grid_out = QGridLayout(self.train_base_setting_content_frame)
        self.train_base_setting_grid_out.setObjectName(u"train_base_setting_grid_out")

        self.page_train_base_setting_layout.addWidget(self.train_base_setting_content_frame)

        self.train_base_setting_btn_frame = QFrame(self.page_train_base_setting)
        self.train_base_setting_btn_frame.setObjectName(u"train_base_setting_btn_frame")
        self.train_base_setting_btn_frame.setMaximumSize(QSize(16777215, 200))
        self.train_base_setting_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.train_base_setting_btn_frame.setFrameShadow(QFrame.Raised)
        self.train_base_setting_btn_layout = QHBoxLayout(self.train_base_setting_btn_frame)
        self.train_base_setting_btn_layout.setObjectName(u"train_base_setting_btn_layout")

        self.page_train_base_setting_layout.addWidget(self.train_base_setting_btn_frame)

        self.pages.addWidget(self.page_train_base_setting)
        self.page_train_net_setting = QWidget()
        self.page_train_net_setting.setObjectName(u"page_train_net_setting")
        self.page_train_net_setting_layout = QVBoxLayout(self.page_train_net_setting)
        self.page_train_net_setting_layout.setObjectName(u"page_train_net_setting_layout")
        self.train_net_setting_title_frame = QFrame(self.page_train_net_setting)
        self.train_net_setting_title_frame.setObjectName(u"train_net_setting_title_frame")
        self.train_net_setting_title_frame.setMaximumSize(QSize(16777215, 200))
        self.train_net_setting_title_frame.setFrameShape(QFrame.StyledPanel)
        self.train_net_setting_title_frame.setFrameShadow(QFrame.Raised)
        self.train_net_setting_title_layout = QHBoxLayout(self.train_net_setting_title_frame)
        self.train_net_setting_title_layout.setObjectName(u"train_net_setting_title_layout")
        self.train_net_setting_title_label = QLabel(self.train_net_setting_title_frame)
        self.train_net_setting_title_label.setObjectName(u"train_net_setting_title_label")
        self.train_net_setting_title_label.setFont(font)
        self.train_net_setting_title_label.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")

        self.train_net_setting_title_layout.addWidget(self.train_net_setting_title_label, 0, Qt.AlignHCenter)


        self.page_train_net_setting_layout.addWidget(self.train_net_setting_title_frame)

        self.train_net_setting_content_frame = QFrame(self.page_train_net_setting)
        self.train_net_setting_content_frame.setObjectName(u"train_net_setting_content_frame")
        self.train_net_setting_content_frame.setMinimumSize(QSize(0, 320))
        self.train_net_setting_content_frame.setFrameShape(QFrame.StyledPanel)
        self.train_net_setting_content_frame.setFrameShadow(QFrame.Raised)
        self.train_net_setting_grid_layout = QGridLayout(self.train_net_setting_content_frame)
        self.train_net_setting_grid_layout.setObjectName(u"train_net_setting_grid_layout")

        self.page_train_net_setting_layout.addWidget(self.train_net_setting_content_frame)

        self.train_net_setting_btn_frame = QFrame(self.page_train_net_setting)
        self.train_net_setting_btn_frame.setObjectName(u"train_net_setting_btn_frame")
        self.train_net_setting_btn_frame.setMaximumSize(QSize(16777215, 200))
        self.train_net_setting_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.train_net_setting_btn_frame.setFrameShadow(QFrame.Raised)
        self.train_net_setting_btn_layout = QHBoxLayout(self.train_net_setting_btn_frame)
        self.train_net_setting_btn_layout.setObjectName(u"train_net_setting_btn_layout")

        self.page_train_net_setting_layout.addWidget(self.train_net_setting_btn_frame)

        self.pages.addWidget(self.page_train_net_setting)
        self.page_train_info = QWidget()
        self.page_train_info.setObjectName(u"page_train_info")
        self.page_train_info_layout = QVBoxLayout(self.page_train_info)
        self.page_train_info_layout.setObjectName(u"page_train_info_layout")
        self.page_train_info_scroll_area = QScrollArea(self.page_train_info)
        self.page_train_info_scroll_area.setObjectName(u"page_train_info_scroll_area")
        self.page_train_info_scroll_area.setStyleSheet(u"background: transparent;")
        self.page_train_info_scroll_area.setFrameShape(QFrame.NoFrame)
        self.page_train_info_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page_train_info_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.page_train_info_scroll_area.setWidgetResizable(True)
        self.page_train_info_scroll_area_content = QWidget()
        self.page_train_info_scroll_area_content.setObjectName(u"page_train_info_scroll_area_content")
        self.page_train_info_scroll_area_content.setGeometry(QRect(0, 0, 870, 547))
        self.page_train_info_scroll_area_content.setStyleSheet(u"background: transparent;")
        self.page_train_info_scroll_layout = QVBoxLayout(self.page_train_info_scroll_area_content)
        self.page_train_info_scroll_layout.setObjectName(u"page_train_info_scroll_layout")
        self.train_info_title_frame = QFrame(self.page_train_info_scroll_area_content)
        self.train_info_title_frame.setObjectName(u"train_info_title_frame")
        self.train_info_title_frame.setMaximumSize(QSize(16777215, 200))
        self.train_info_title_frame.setFrameShape(QFrame.StyledPanel)
        self.train_info_title_frame.setFrameShadow(QFrame.Raised)
        self.train_info_title_layout = QHBoxLayout(self.train_info_title_frame)
        self.train_info_title_layout.setObjectName(u"train_info_title_layout")
        self.train_info_title_label = QLabel(self.train_info_title_frame)
        self.train_info_title_label.setObjectName(u"train_info_title_label")
        self.train_info_title_label.setFont(font)
        self.train_info_title_label.setStyleSheet(u"font: 700 20pt \"Microsoft YaHei UI\";")

        self.train_info_title_layout.addWidget(self.train_info_title_label, 0, Qt.AlignHCenter)


        self.page_train_info_scroll_layout.addWidget(self.train_info_title_frame)

        self.train_info_setting_show_frame = QFrame(self.page_train_info_scroll_area_content)
        self.train_info_setting_show_frame.setObjectName(u"train_info_setting_show_frame")
        self.train_info_setting_show_frame.setFrameShape(QFrame.StyledPanel)
        self.train_info_setting_show_frame.setFrameShadow(QFrame.Raised)
        self.train_info_setting_show_layout = QVBoxLayout(self.train_info_setting_show_frame)
        self.train_info_setting_show_layout.setObjectName(u"train_info_setting_show_layout")
        self.train_info_setting_show_layout.setContentsMargins(200, -1, 200, -1)
        self.train_info_setting_show_title_label = QLabel(self.train_info_setting_show_frame)
        self.train_info_setting_show_title_label.setObjectName(u"train_info_setting_show_title_label")
        self.train_info_setting_show_title_label.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.train_info_setting_show_layout.addWidget(self.train_info_setting_show_title_label)

        self.train_info_setting_show_info_frame = QFrame(self.train_info_setting_show_frame)
        self.train_info_setting_show_info_frame.setObjectName(u"train_info_setting_show_info_frame")
        self.train_info_setting_show_info_frame.setFrameShape(QFrame.StyledPanel)
        self.train_info_setting_show_info_frame.setFrameShadow(QFrame.Raised)
        self.train_select_info_grid_layout = QGridLayout(self.train_info_setting_show_info_frame)
        self.train_select_info_grid_layout.setObjectName(u"train_select_info_grid_layout")
        self.train_select_info_grid_layout.setContentsMargins(50, -1, -1, -1)

        self.train_info_setting_show_layout.addWidget(self.train_info_setting_show_info_frame)


        self.page_train_info_scroll_layout.addWidget(self.train_info_setting_show_frame)

        self.train_info_content_frame = QFrame(self.page_train_info_scroll_area_content)
        self.train_info_content_frame.setObjectName(u"train_info_content_frame")
        self.train_info_content_frame.setFrameShape(QFrame.StyledPanel)
        self.train_info_content_frame.setFrameShadow(QFrame.Raised)
        self.train_info_content_layout = QVBoxLayout(self.train_info_content_frame)
        self.train_info_content_layout.setObjectName(u"train_info_content_layout")
        self.train_info_content_layout.setContentsMargins(200, -1, 200, -1)
        self.train_info_content_title_label = QLabel(self.train_info_content_frame)
        self.train_info_content_title_label.setObjectName(u"train_info_content_title_label")
        self.train_info_content_title_label.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.train_info_content_layout.addWidget(self.train_info_content_title_label)

        self.train_info_text_edit = QTextEdit(self.train_info_content_frame)
        self.train_info_text_edit.setObjectName(u"train_info_text_edit")
        self.train_info_text_edit.setReadOnly(True)

        self.train_info_content_layout.addWidget(self.train_info_text_edit)


        self.page_train_info_scroll_layout.addWidget(self.train_info_content_frame)

        self.train_and_test_result_frame = QFrame(self.page_train_info_scroll_area_content)
        self.train_and_test_result_frame.setObjectName(u"train_and_test_result_frame")
        self.train_and_test_result_frame.setMinimumSize(QSize(0, 0))
        self.train_and_test_result_frame.setFrameShape(QFrame.NoFrame)
        self.train_and_test_result_frame.setFrameShadow(QFrame.Raised)
        self.train_and_test_result_layout = QHBoxLayout(self.train_and_test_result_frame)
        self.train_and_test_result_layout.setObjectName(u"train_and_test_result_layout")
        self.train_and_test_result_layout.setContentsMargins(200, -1, 200, -1)
        self.test_result_frame = QFrame(self.train_and_test_result_frame)
        self.test_result_frame.setObjectName(u"test_result_frame")
        self.test_result_frame.setStyleSheet(u"")
        self.test_result_frame.setFrameShape(QFrame.NoFrame)
        self.test_result_frame.setFrameShadow(QFrame.Raised)
        self.test_result_layout = QVBoxLayout(self.test_result_frame)
        self.test_result_layout.setObjectName(u"test_result_layout")
        self.train_info_test_result_title_label = QLabel(self.test_result_frame)
        self.train_info_test_result_title_label.setObjectName(u"train_info_test_result_title_label")
        self.train_info_test_result_title_label.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.test_result_layout.addWidget(self.train_info_test_result_title_label)

        self.test_set_info_frame = QFrame(self.test_result_frame)
        self.test_set_info_frame.setObjectName(u"test_set_info_frame")
        self.test_set_info_frame.setMinimumSize(QSize(0, 150))
        self.test_set_info_frame.setStyleSheet(u"")
        self.test_set_info_frame.setFrameShape(QFrame.NoFrame)
        self.test_set_info_frame.setFrameShadow(QFrame.Raised)
        self.test_set_info_layout = QVBoxLayout(self.test_set_info_frame)
        self.test_set_info_layout.setObjectName(u"test_set_info_layout")

        self.test_result_layout.addWidget(self.test_set_info_frame)

        self.test_set_info_pic_frame = QFrame(self.test_result_frame)
        self.test_set_info_pic_frame.setObjectName(u"test_set_info_pic_frame")
        self.test_set_info_pic_frame.setStyleSheet(u"")
        self.test_set_info_pic_frame.setFrameShape(QFrame.NoFrame)
        self.test_set_info_pic_frame.setFrameShadow(QFrame.Raised)
        self.test_set_info_pic_layout = QVBoxLayout(self.test_set_info_pic_frame)
        self.test_set_info_pic_layout.setObjectName(u"test_set_info_pic_layout")
        self.test_set_info_pic_layout.setContentsMargins(9, 9, 9, -1)

        self.test_result_layout.addWidget(self.test_set_info_pic_frame)

        self.test_result_layout.setStretch(0, 1)
        self.test_result_layout.setStretch(1, 2)
        self.test_result_layout.setStretch(2, 4)

        self.train_and_test_result_layout.addWidget(self.test_result_frame, 0, Qt.AlignTop)

        self.train_result_frame = QFrame(self.train_and_test_result_frame)
        self.train_result_frame.setObjectName(u"train_result_frame")
        self.train_result_frame.setStyleSheet(u"")
        self.train_result_frame.setFrameShape(QFrame.NoFrame)
        self.train_result_frame.setFrameShadow(QFrame.Raised)
        self.train_result_layout = QVBoxLayout(self.train_result_frame)
        self.train_result_layout.setObjectName(u"train_result_layout")
        self.train_result_title_label = QLabel(self.train_result_frame)
        self.train_result_title_label.setObjectName(u"train_result_title_label")
        self.train_result_title_label.setStyleSheet(u"font: 700 12pt \"Microsoft YaHei UI\";")

        self.train_result_layout.addWidget(self.train_result_title_label)

        self.train_result_pic_frame = QFrame(self.train_result_frame)
        self.train_result_pic_frame.setObjectName(u"train_result_pic_frame")
        self.train_result_pic_frame.setStyleSheet(u"")
        self.train_result_pic_frame.setFrameShape(QFrame.NoFrame)
        self.train_result_pic_frame.setFrameShadow(QFrame.Raised)
        self.train_result_pic_layout = QVBoxLayout(self.train_result_pic_frame)
        self.train_result_pic_layout.setObjectName(u"train_result_pic_layout")
        self.train_result_pic_layout.setContentsMargins(9, 9, 9, -1)

        self.train_result_layout.addWidget(self.train_result_pic_frame)

        self.train_result_layout.setStretch(0, 1)
        self.train_result_layout.setStretch(1, 5)

        self.train_and_test_result_layout.addWidget(self.train_result_frame, 0, Qt.AlignTop)

        self.train_and_test_result_layout.setStretch(0, 4)
        self.train_and_test_result_layout.setStretch(1, 5)

        self.page_train_info_scroll_layout.addWidget(self.train_and_test_result_frame)

        self.train_info_btn_frame = QFrame(self.page_train_info_scroll_area_content)
        self.train_info_btn_frame.setObjectName(u"train_info_btn_frame")
        self.train_info_btn_frame.setMinimumSize(QSize(0, 0))
        self.train_info_btn_frame.setMaximumSize(QSize(16777215, 200))
        self.train_info_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.train_info_btn_frame.setFrameShadow(QFrame.Raised)
        self.train_info_btn_layout = QHBoxLayout(self.train_info_btn_frame)
        self.train_info_btn_layout.setObjectName(u"train_info_btn_layout")

        self.page_train_info_scroll_layout.addWidget(self.train_info_btn_frame)

        self.page_train_info_scroll_area.setWidget(self.page_train_info_scroll_area_content)

        self.page_train_info_layout.addWidget(self.page_train_info_scroll_area)

        self.pages.addWidget(self.page_train_info)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.add_images_title_label.setText(QCoreApplication.translate("MainPages", u"\u65b0\u589e\u8c31\u56fe", None))
        self.train_base_setting_title_label.setText(QCoreApplication.translate("MainPages", u"\u57fa\u672c\u8bbe\u7f6e", None))
        self.train_net_setting_title_label.setText(QCoreApplication.translate("MainPages", u"\u8bad\u7ec3\u53c2\u6570\u8bbe\u7f6e", None))
        self.train_info_title_label.setText(QCoreApplication.translate("MainPages", u"\u8bad\u7ec3\u4fe1\u606f", None))
        self.train_info_setting_show_title_label.setText(QCoreApplication.translate("MainPages", u"\u57fa\u672c\u4fe1\u606f", None))
        self.train_info_content_title_label.setText(QCoreApplication.translate("MainPages", u"\u8bad\u7ec3\u8fc7\u7a0b\uff1a", None))
        self.train_info_test_result_title_label.setText(QCoreApplication.translate("MainPages", u"\u6d4b\u8bd5\u7ed3\u679c", None))
        self.train_result_title_label.setText(QCoreApplication.translate("MainPages", u"\u8bad\u7ec3\u7ed3\u679c", None))
    # retranslateUi

