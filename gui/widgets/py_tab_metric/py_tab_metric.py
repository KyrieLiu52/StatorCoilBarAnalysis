from qt_core import *


class PyTabMetric(QTabWidget):
    def __init__(self):
        super().__init__()
        self.title = ['表面AFM谱图', '表面SEM谱图', '2D-SAXS谱图', '2D-WAXD谱图']
        self.image_list = ['images/metrics_images/metric_afm.png', 'images/metrics_images/metric_sem.png', 'images/metrics_images/metric_saxs.png', 'images/metrics_images/metric_waxd.png']

        # SETUP UI
        self.setup_ui()

    # 页面总体布局
    def setup_ui(self):
        for i in range(4):
            self.add_tab(i)

    # 添加tab
    def add_tab(self, i):
        tab = QWidget()
        tab.setContentsMargins(0, 0, 0, 0)
        tab.setStyleSheet(
            "background-color: #2c313c;"
        )
        self.addTab(tab, f'{self.title[i]}')
        # 设置每个tab的内容
        layout = QHBoxLayout(tab)
        layout.setObjectName(u"layout")
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        img_frame = QFrame()
        img_frame.setContentsMargins(0,0,0,0)
        img_frame.setStyleSheet("background:#4f5b6e")
        img_layout = QVBoxLayout(img_frame)
        img_layout.setContentsMargins(0,0,0,0)
        img_layout.setSpacing(0)
        img = QLabel()
        img.setScaledContents(True)
        img.setPixmap(QPixmap(self.image_list[i]))
        img_layout.addWidget(img)
        layout.addWidget(img_frame)
