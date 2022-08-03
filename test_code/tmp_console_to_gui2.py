import ctypes
import sys
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit
from PySide6.QtGui import QTextCursor
from test_code.tmp_train_saxs import train_saxs
import win32con

'''
控制台输出定向到Qtextedit中
'''


class Stream(QObject):
    """Redirects console output to text widget."""
    newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):  # real signature unknown; restored from __doc__
        """ flush(self) """
        pass


class GenMast(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.initUI()

        # Custom output stream.
        self.sm = Stream()
        self.sm.newText.connect(self.onUpdateText)
        sys.stdout = self.sm
        sys.stderr = self.sm

        self.my_thread = MyThread()

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def initUI(self):
        """Creates UI window on launch."""
        # Button for generating the master list.
        btnGenMast = QPushButton('Run', self)
        btnGenMast.move(450, 50)
        btnGenMast.resize(100, 200)
        btnGenMast.clicked.connect(self.genMastClicked)

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

    def printhello(self):
        self.my_thread.start()

    def genMastClicked(self):
        """Runs the main function."""
        print('Running...')
        self.printhello()
        # loop = QEventLoop()
        # QTimer.singleShot(2000, loop.quit)
        # loop.exec_()
        print('Done.')

class MyThread(QThread):  # 线程类
    # my_signal = Signal(str)  # 自定义信号对象。参数str就代表这个信号可以传一个字符串

    def __init__(self):
        super(MyThread, self).__init__()
        # self.count = 0
        self.is_on = True

    def run(self):  # 线程执行函数
        self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
            win32con.PROCESS_ALL_ACCESS, False, str(QThread.currentThread()))
        while self.is_on:
            # train code
            train_saxs("../data_split/saxs/train", epochs=30)
            self.is_on = False

if __name__ == '__main__':
    # Run the application.
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    gui = GenMast()
    sys.exit(app.exec_())