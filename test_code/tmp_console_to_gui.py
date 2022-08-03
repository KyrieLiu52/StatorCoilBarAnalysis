import ctypes
# import win32con
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThread
from PySide6.QtCore import QObject, QEventLoop, QTimer
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
from PySide6.QtGui import QTextCursor

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.Signal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):  # real signature unknown; restored from __doc__
        """ flush(self) """
        pass


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.Exit.triggered.connect(self.close)
        # self.pushButton_Detection.clicked.connect()

    def initUI(self):
        """Creates UI window on launch."""
        # Button for generating the master list.
        btnGenMast = QPushButton('Run', self)
        btnGenMast.move(450, 50)
        btnGenMast.resize(100, 200)
        btnGenMast.clicked.connect(Training_Dialog().run_training())

        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(200)
        self.process.move(30, 50)

        # Set window size and title, then show the window.
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('Generate Master')
        self.show()


class Training_Dialog(QDialog):
    def __init__(self):
        super(Training_Dialog, self).__init__()
        self.es = EmittingStream()
        self.es.textWritten.connect(self.normalOutputWritten)
        sys.stdout = self.es
        sys.stder = self.es
        self.my_thread = MyThread()  # 实例化线程对象

    def stop_training(self):
        self.my_thread.is_on = False
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.my_thread.handle, 0)
        print('终止训练', self.my_thread.handle, ret)

    def run_training(self):
        self.my_thread.start()  # 启动线程

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


class MyThread(QThread):  # 线程类
    # my_signal = Signal(str)  # 自定义信号对象。参数str就代表这个信号可以传一个字符串

    def __init__(self):
        super(MyThread, self).__init__()
        # self.count = 0
        self.is_on = True

    def run(self):  # 线程执行函数
        # self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
        #     win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
        while self.is_on:
            # train code
            self.is_on = False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = MainUI()
    gui.show()

    sys.exit(app.exec_())