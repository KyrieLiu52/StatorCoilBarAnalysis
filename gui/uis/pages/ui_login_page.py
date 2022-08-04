# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_pageMtXTGg.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(625, 424)
        self.login_frame = QFrame(Form)
        self.login_frame.setObjectName(u"login_frame")
        self.login_frame.setGeometry(QRect(10, 10, 600, 400))
        self.login_frame.setMinimumSize(QSize(600, 400))
        self.login_frame.setMaximumSize(QSize(600, 400))
        self.login_frame.setFrameShape(QFrame.StyledPanel)
        self.login_frame.setFrameShadow(QFrame.Raised)
        self.login_content_layout = QVBoxLayout(self.login_frame)
        self.login_content_layout.setObjectName(u"login_content_layout")
        self.login_title_frame = QFrame(self.login_frame)
        self.login_title_frame.setObjectName(u"login_title_frame")
        self.login_title_frame.setFrameShape(QFrame.StyledPanel)
        self.login_title_frame.setFrameShadow(QFrame.Raised)
        self.login_title_layout = QVBoxLayout(self.login_title_frame)
        self.login_title_layout.setObjectName(u"login_title_layout")

        self.login_content_layout.addWidget(self.login_title_frame)

        self.login_text_frame = QFrame(self.login_frame)
        self.login_text_frame.setObjectName(u"login_text_frame")
        self.login_text_frame.setFrameShape(QFrame.StyledPanel)
        self.login_text_frame.setFrameShadow(QFrame.Raised)
        self.login_label_and_edit_layout = QHBoxLayout(self.login_text_frame)
        self.login_label_and_edit_layout.setObjectName(u"login_label_and_edit_layout")
        self.login_label_frame = QFrame(self.login_text_frame)
        self.login_label_frame.setObjectName(u"login_label_frame")
        self.login_label_frame.setFrameShape(QFrame.StyledPanel)
        self.login_label_frame.setFrameShadow(QFrame.Raised)
        self.login_label_layout = QVBoxLayout(self.login_label_frame)
        self.login_label_layout.setObjectName(u"login_label_layout")
        self.label_username_frame = QFrame(self.login_label_frame)
        self.label_username_frame.setObjectName(u"label_username_frame")
        self.label_username_frame.setMinimumSize(QSize(100, 40))
        self.label_username_frame.setFrameShape(QFrame.StyledPanel)
        self.label_username_frame.setFrameShadow(QFrame.Raised)
        self.label_username_layout = QVBoxLayout(self.label_username_frame)
        self.label_username_layout.setObjectName(u"label_username_layout")
        self.label_username_layout.setContentsMargins(-1, -1, -1, 20)

        self.login_label_layout.addWidget(self.label_username_frame)

        self.label_pwd_frame = QFrame(self.login_label_frame)
        self.label_pwd_frame.setObjectName(u"label_pwd_frame")
        self.label_pwd_frame.setMinimumSize(QSize(100, 40))
        self.label_pwd_frame.setFrameShape(QFrame.StyledPanel)
        self.label_pwd_frame.setFrameShadow(QFrame.Raised)
        self.label_pwd_layout = QVBoxLayout(self.label_pwd_frame)
        self.label_pwd_layout.setObjectName(u"label_pwd_layout")
        self.label_pwd_layout.setContentsMargins(-1, 20, -1, -1)

        self.login_label_layout.addWidget(self.label_pwd_frame)


        self.login_label_and_edit_layout.addWidget(self.login_label_frame)

        self.login_text_input_frame = QFrame(self.login_text_frame)
        self.login_text_input_frame.setObjectName(u"login_text_input_frame")
        self.login_text_input_frame.setFrameShape(QFrame.StyledPanel)
        self.login_text_input_frame.setFrameShadow(QFrame.Raised)
        self.login_edit_layout = QVBoxLayout(self.login_text_input_frame)
        self.login_edit_layout.setObjectName(u"login_edit_layout")
        self.input_username_frame = QFrame(self.login_text_input_frame)
        self.input_username_frame.setObjectName(u"input_username_frame")
        self.input_username_frame.setMinimumSize(QSize(0, 40))
        self.input_username_frame.setFrameShape(QFrame.StyledPanel)
        self.input_username_frame.setFrameShadow(QFrame.Raised)
        self.input_username_layout = QVBoxLayout(self.input_username_frame)
        self.input_username_layout.setObjectName(u"input_username_layout")
        self.input_username_layout.setContentsMargins(-1, -1, -1, 20)

        self.login_edit_layout.addWidget(self.input_username_frame)

        self.input_pwd_frame = QFrame(self.login_text_input_frame)
        self.input_pwd_frame.setObjectName(u"input_pwd_frame")
        self.input_pwd_frame.setMinimumSize(QSize(0, 40))
        self.input_pwd_frame.setFrameShape(QFrame.StyledPanel)
        self.input_pwd_frame.setFrameShadow(QFrame.Raised)
        self.input_pwd_layout = QVBoxLayout(self.input_pwd_frame)
        self.input_pwd_layout.setObjectName(u"input_pwd_layout")
        self.input_pwd_layout.setContentsMargins(-1, 20, -1, -1)

        self.login_edit_layout.addWidget(self.input_pwd_frame)


        self.login_label_and_edit_layout.addWidget(self.login_text_input_frame)


        self.login_content_layout.addWidget(self.login_text_frame)

        self.login_btn_frame = QFrame(self.login_frame)
        self.login_btn_frame.setObjectName(u"login_btn_frame")
        self.login_btn_frame.setFrameShape(QFrame.StyledPanel)
        self.login_btn_frame.setFrameShadow(QFrame.Raised)
        self.login_btn_layout = QHBoxLayout(self.login_btn_frame)
        self.login_btn_layout.setObjectName(u"login_btn_layout")

        self.login_content_layout.addWidget(self.login_btn_frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

