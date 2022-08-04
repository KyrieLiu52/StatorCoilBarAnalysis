from qt_core import *


class PyHistoryDetailPage(QWidget):
    def __init__(self, data):
        super(PyHistoryDetailPage, self).__init__()
        self.data = data
        # SETUP UI
        self.setup_ui()

    # 页面总体布局
    def setup_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            "background-color: #2c313c;"
        )
        # 设置每个self的内容
        layout = QHBoxLayout(self)
        layout.setObjectName(u"layout")
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # 左半部分
        left_frame = QFrame(self)
        left_frame.setFrameShape(QFrame.NoFrame)
        left_frame.setFrameShadow(QFrame.Raised)
        verticalLayout = QVBoxLayout(left_frame)
        verticalLayout.setSpacing(0)
        verticalLayout.setObjectName(u"verticalLayout")
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        left_top_frame = QFrame(left_frame)
        left_top_frame.setObjectName(u"left_top_frame")
        left_top_frame.setFrameShape(QFrame.NoFrame)
        left_top_frame.setFrameShadow(QFrame.Raised)
        gridLayout = QGridLayout(left_top_frame)
        gridLayout.setSpacing(0)
        gridLayout.setObjectName(u"gridLayout")
        gridLayout.setContentsMargins(30, 0, 0, 5)
        # 内容

        style = 'color: white; font: bold 14px;'

        # 左上角栅格内容
        # 标题(图片type)
        image_title = QLabel(left_top_frame)
        image_title.setObjectName(u"image_title")
        if self.data[2] == "AFM":
            image_title.setText("表面AFM谱图")
        elif self.data[2] == "SEM":
            image_title.setText("表面SEM谱图")
        elif self.data[2] == "SAXS":
            image_title.setText("2D-SAXS谱图")
        elif self.data[2] == "WAXD":
            image_title.setText("2D-WAXD谱图")
        image_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        image_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        image_title.setContentsMargins(0, 10, 10, 10)

        # 谱图类型
        image_type_title = QLabel(left_top_frame)
        image_type_title.setObjectName(u'image_type_title')
        image_type_title.setText('谱图类型：')
        # 设置样式
        image_type_title.setStyleSheet(style)
        image_type_title.setContentsMargins(5, 0, 5, 0)

        image_type = QLabel(left_top_frame)
        image_type.setObjectName(u'image_type')
        image_type.setText(image_title.text())

        # 检测时间
        image_time_title = QLabel(left_top_frame)
        image_time_title.setObjectName(u'image_time_title')
        image_time_title.setText('检测时间：')
        # 设置样式
        image_time_title.setStyleSheet(style)
        image_time_title.setContentsMargins(5, 0, 5, 0)

        image_time = QLabel(left_top_frame)
        image_time.setObjectName(u'image_time')
        image_time.setText(self.data[3])
        # 图片名称
        image_name_title = QLabel(left_top_frame)
        image_name_title.setObjectName(u'image_name_title')
        image_name_title.setText('图片名称：')
        # 设置样式
        image_name_title.setStyleSheet(style)
        image_name_title.setContentsMargins(5, 0, 5, 0)

        image_name = QLabel(left_top_frame)
        image_name.setObjectName(u'image_name')
        image_name.setText(self.data[5])
        # 图片地址
        image_path_title = QLabel(left_top_frame)
        image_path_title.setObjectName(u'image_path_title')
        image_path_title.setText('图片地址：')
        # 设置样式
        image_path_title.setStyleSheet(style)
        image_path_title.setContentsMargins(5, 0, 5, 0)

        image_path = QLabel(left_top_frame)
        image_path.setObjectName(u'image_path')
        image_path.setText(self.data[1])
        # 图片
        image = QLabel(left_top_frame)
        image.setObjectName(u'image')
        image.setPixmap(QPixmap(self.data[1]))
        image.setContentsMargins(0, 5, 5, 5)
        image.setMaximumSize(400, 300)
        image.setScaledContents(True)

        gridLayout.setColumnStretch(2, 1)
        gridLayout.addWidget(image_title, 0, 0, 1, 3)
        gridLayout.addWidget(image_type_title, 1, 1, 1, 1)
        gridLayout.addWidget(image_type, 1, 2, 1, 1)
        gridLayout.addWidget(image_time_title, 2, 1, 1, 1)
        gridLayout.addWidget(image_time, 2, 2, 1, 1)
        gridLayout.addWidget(image_name_title, 3, 1, 1, 1)
        gridLayout.addWidget(image_name, 3, 2, 1, 1)
        gridLayout.addWidget(image_path_title, 4, 1, 1, 1)
        gridLayout.addWidget(image_path, 4, 2, 1, 1)
        gridLayout.addWidget(image, 1, 0, 4, 1)
        verticalLayout.addWidget(left_top_frame)

        # 左上左下分割线
        line_1 = QFrame(left_frame)
        line_1.setObjectName(u"line_1")
        line_1.setStyleSheet(u"")
        line_1.setFrameShape(QFrame.HLine)
        line_1.setFrameShadow(QFrame.Sunken)
        verticalLayout.addWidget(line_1)

        # 左下角
        left_bottom_frame = QFrame(left_frame)
        left_bottom_frame.setObjectName(u"left_bottom_frame")
        left_bottom_frame.setFrameShape(QFrame.NoFrame)
        left_bottom_frame.setFrameShadow(QFrame.Raised)
        inference_left_bottom_layout = QGridLayout(left_bottom_frame)
        inference_left_bottom_layout.setSpacing(0)
        inference_left_bottom_layout.setObjectName(u"inference_left_bottom_layout")
        inference_left_bottom_layout.setContentsMargins(0, 10, 10, 10)

        # 设置内容
        # 设置label内容
        result_image = QLabel(left_bottom_frame)
        result_image.setObjectName(u"result_image")
        result_image.setPixmap(QPixmap(self.data[7]))
        # result.setMaximumSize(500, 400)
        result_image.setScaledContents(True)

        result_title = QLabel(left_bottom_frame)
        result_title.setObjectName(u"result_title")
        result_title.setText('预测结果：')
        result_title.setContentsMargins(0, 10, 0, 10)
        result_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        result = QLabel(left_bottom_frame)
        result.setObjectName(u"result")
        result.setText(self.data[4])
        result.setContentsMargins(0, 0, 0, 0)
        result.setStyleSheet(
            "color: red;"
            'font: bold 20px;'
        )

        result_confidence_title = QLabel(left_bottom_frame)
        result_confidence_title.setObjectName(u"result_confidence_title")
        result_confidence_title.setText('置信度：')
        result_confidence_title.setContentsMargins(0, 0, 0, 0)
        result_confidence_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        result_confidence = QLabel(left_bottom_frame)
        result_confidence.setObjectName(u"result_confidence")
        result_confidence.setText(self.data[6])
        result_confidence.setContentsMargins(0, 0, 0, 0)
        result_confidence.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )

        inference_left_bottom_layout.addWidget(result_image, 0, 0, 2, 1)
        inference_left_bottom_layout.addWidget(result_title, 0, 1, 1, 1)
        inference_left_bottom_layout.addWidget(result, 0, 2, 1, 1)
        inference_left_bottom_layout.addWidget(result_confidence_title, 1, 1, 1, 1)
        inference_left_bottom_layout.addWidget(result_confidence, 1, 2, 1, 1)
        inference_left_bottom_layout.setContentsMargins(0, 10, 10, 10)

        verticalLayout.addWidget(left_bottom_frame)

        verticalLayout.setStretch(0, 1)
        verticalLayout.setStretch(1, 1)
        verticalLayout.setStretch(2, 1)

        layout.addWidget(left_frame)

        # 左右分界线
        line_2 = QFrame(self)
        line_2.setObjectName(u"line_2")
        line_2.setFrameShape(QFrame.VLine)
        line_2.setFrameShadow(QFrame.Sunken)

        layout.addWidget(line_2)

        # 右半部分
        right_frame = QFrame(self)
        right_frame.setObjectName(u"right_frame")
        right_frame.setFrameShape(QFrame.NoFrame)
        right_frame.setFrameShadow(QFrame.Raised)
        inference_right_layout = QVBoxLayout(right_frame)
        inference_right_layout.setSpacing(0)
        inference_right_layout.setContentsMargins(10, 10, 10, 10)
        inference_right_layout.setObjectName(u"inference_right_frame")

        # feature_title = QLabel(right_frame)
        # feature_title.setObjectName(u"feature_title")

        feature_img_1_title = QLabel(right_frame)
        feature_img_1_title.setObjectName(u"feature_img_1_title")
        feature_img_1_title.setText('中间特征层：')
        feature_img_1_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        feature_img_1_title.setContentsMargins(10, 10, 10, 10)

        # 内容
        feature_img_1 = QLabel(right_frame)
        feature_img_1.setObjectName(u"feature_img_1")
        feature_img_1.setPixmap(QPixmap(self.data[8]))
        feature_img_1.setScaledContents(True)
        feature_img_1.setContentsMargins(10, 10, 10, 10)

        feature_img_2_title = QLabel(right_frame)
        feature_img_2_title.setObjectName(u"feature_img_2_title")
        feature_img_2_title.setText('推理特征图：')
        feature_img_2_title.setStyleSheet(
            "color: white;"
            'font: bold 20px;'
        )
        feature_img_2_title.setContentsMargins(10, 10, 10, 10)
        # 内容
        feature_img_2 = QLabel(right_frame)
        feature_img_2.setObjectName(u"feature_img_2")
        feature_img_2.setPixmap(QPixmap(self.data[9]))
        feature_img_2.setScaledContents(True)
        feature_img_2.setContentsMargins(10, 10, 10, 10)

        inference_right_layout.addWidget(feature_img_1_title)
        inference_right_layout.addWidget(feature_img_1)
        inference_right_layout.addWidget(feature_img_2_title)
        inference_right_layout.addWidget(feature_img_2)
        inference_right_layout.setStretch(0, 1)
        inference_right_layout.setStretch(1, 4)
        inference_right_layout.setStretch(2, 1)
        inference_right_layout.setStretch(3, 4)

        layout.addWidget(right_frame)

        layout.setStretch(0, 3)
        layout.setStretch(1, 1)
        layout.setStretch(2, 2)

    