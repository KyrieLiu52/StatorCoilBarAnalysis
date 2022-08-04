# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'right_columnQbKVWS.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qt_core import *


class Ui_RightColumn(object):
    def setupUi(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName(u"RightColumn")
        RightColumn.resize(289, 652)
        self.main_pages_layout = QVBoxLayout(RightColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.menus = QStackedWidget(RightColumn)
        self.menus.setObjectName(u"menus")
        self.menu_1 = QWidget()
        self.menu_1.setObjectName(u"menu_1")
        self.verticalLayout_2 = QVBoxLayout(self.menu_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.user_info_frame = QFrame(self.menu_1)
        self.user_info_frame.setObjectName(u"user_info_frame")
        self.user_info_frame.setFrameShape(QFrame.NoFrame)
        self.user_info_frame.setFrameShadow(QFrame.Raised)
        self.user_info_grid = QGridLayout(self.user_info_frame)
        self.user_info_grid.setSpacing(0)
        self.user_info_grid.setObjectName(u"user_info_grid")
        self.user_info_grid.setContentsMargins(10, 0, 10, 0)

        self.verticalLayout_2.addWidget(self.user_info_frame)

        self.space_frame = QFrame(self.menu_1)
        self.space_frame.setObjectName(u"space_frame")
        self.space_frame.setFrameShape(QFrame.NoFrame)
        self.space_frame.setFrameShadow(QFrame.Raised)
        self.space_layout = QVBoxLayout(self.space_frame)
        self.space_layout.setSpacing(0)
        self.space_layout.setObjectName(u"space_layout")
        self.space_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.space_frame)

        self.menus.addWidget(self.menu_1)

        self.main_pages_layout.addWidget(self.menus)


        self.retranslateUi(RightColumn)

        self.menus.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RightColumn)
    # setupUi

    def retranslateUi(self, RightColumn):
        RightColumn.setWindowTitle(QCoreApplication.translate("RightColumn", u"Form", None))
    # retranslateUi

