import ctypes

import win32con
from PySide6.QtCore import QObject, Signal, QThread

from incremental_train import incremental_train
from test_model import test_model
from train_afm import train_afm
from train_saxs import train_saxs
from train_sem import train_sem
from train_waxd import train_waxd

'''
功能：
    将控制台中的输出，重定向到GUI的控件 W 中
使用方法：
    1.在GUI中，定义一个如何更新 W 中内容的函数 onUpdateText
    2.在GUI中，将onUpdateText函数 绑定到 输出流Stream 中的newText中
    3.将sys的stdout设置为自定义的输出流 Stream
    4.在GUI中调用 特定的线程，执行功能函数，将功能函数写在 线程的run中
    5.在关闭GUI的时候，将sys的stdout重置为 sys.__stdout__
'''


# 自定义的输出流，将输出重定向到某个地方
class Stream(QObject):
    """Redirects console output to text widget."""
    newText = Signal(str)

    def write(self, text):
        # 发出内容
        self.newText.emit(str(text))

    def flush(self):  # real signature unknown; restored from __doc__
        """ flush(self) """
        pass


class TrainThread(QThread):  # 线程类
    # my_signal = Signal(str)  # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    def __init__(self):
        super(TrainThread, self).__init__()
        # self.count = 0
        self.is_on = True
        self.callback = None

        self.training_data_type = ""
        self.training_data_dir = ""
        self.model_save_dir = ""
        self.epochs = 10
        self.batchsize = 32
        self.validation_set_rate = 0.2
        self.learning_rate = 0.001
        self.lr_decay_steps = 20
        self.lr_decay_rate = 1
        self.dropout_rate = 0.2

        self.train_result_pic_path=""
        self.highest_acc=0
        self.highest_val_acc=0
        self.best_model_path=""

    def run(self):  # 线程执行函数
        self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
            win32con.PROCESS_ALL_ACCESS, False, str(QThread.currentThread()))
        while self.is_on:
             # train code
            if self.training_data_type == "AFM":
                train_result_pic_path, highest_acc, highest_val_acc, best_model_path=train_afm(my_callback=self.callback,
                          data_dir=self.training_data_dir, model_save_dir=self.model_save_dir, epochs=self.epochs,
                          batch_size=self.batchsize, validation_set_rate=self.validation_set_rate,
                          learning_rate=self.learning_rate, lr_decay_steps=self.lr_decay_steps,
                          lr_decay_rate=self.lr_decay_rate, dropout_rate=self.dropout_rate)
                self.train_result_pic_path = train_result_pic_path
                self.highest_acc = highest_acc
                self.highest_val_acc = highest_val_acc
                self.best_model_path = best_model_path
            elif self.training_data_type == "SEM":
                train_result_pic_path, highest_acc, highest_val_acc, best_model_path = train_sem(my_callback=self.callback,
                    data_dir=self.training_data_dir, model_save_dir=self.model_save_dir, epochs=self.epochs,
                    batch_size=self.batchsize, validation_set_rate=self.validation_set_rate,
                    learning_rate=self.learning_rate, lr_decay_steps=self.lr_decay_steps,
                    lr_decay_rate=self.lr_decay_rate, dropout_rate=self.dropout_rate)
                self.train_result_pic_path = train_result_pic_path
                self.highest_acc = highest_acc
                self.highest_val_acc = highest_val_acc
                self.best_model_path = best_model_path
            elif self.training_data_type == "SAXS":
                train_result_pic_path, highest_acc, highest_val_acc, best_model_path = train_saxs(my_callback=self.callback,
                    data_dir=self.training_data_dir, model_save_dir=self.model_save_dir, epochs=self.epochs,
                    batch_size=self.batchsize, validation_set_rate=self.validation_set_rate,
                    learning_rate=self.learning_rate, lr_decay_steps=self.lr_decay_steps,
                    lr_decay_rate=self.lr_decay_rate, dropout_rate=self.dropout_rate)
                self.train_result_pic_path = train_result_pic_path
                self.highest_acc = highest_acc
                self.highest_val_acc = highest_val_acc
                self.best_model_path = best_model_path
            elif self.training_data_type == "WAXD":
                train_result_pic_path, highest_acc, highest_val_acc, best_model_path = train_waxd(my_callback=self.callback,
                    data_dir=self.training_data_dir, model_save_dir=self.model_save_dir, epochs=self.epochs,
                    batch_size=self.batchsize, validation_set_rate=self.validation_set_rate,
                    learning_rate=self.learning_rate, lr_decay_steps=self.lr_decay_steps,
                    lr_decay_rate=self.lr_decay_rate, dropout_rate=self.dropout_rate)
                self.train_result_pic_path = train_result_pic_path
                self.highest_acc = highest_acc
                self.highest_val_acc = highest_val_acc
                self.best_model_path = best_model_path
            else:
                pass
            self.is_on = False


class IncrementalTrainThread(QThread):
    def __init__(self):
        super(IncrementalTrainThread, self).__init__()
        # 线程参数
        self.is_on = True
        self.callback = None
        # 训练参数
        self.training_data_type = ""
        self.training_data_dir = ""
        self.model_save_dir = ""
        self.epochs = 10
        self.batchsize = 32
        self.validation_set_rate = 0.2
        self.learning_rate = 0.001
        self.lr_decay_steps = 20
        self.lr_decay_rate = 1
        self.pretrained_model = ""
        # 训练返回值
        self.train_result_pic_path = ""
        self.highest_acc = 0
        self.highest_val_acc = 0
        self.best_model_path = ""

    def run(self):  # 线程执行函数
        self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
            win32con.PROCESS_ALL_ACCESS, False, str(QThread.currentThread()))
        while self.is_on:
             # incremental train code
            train_result_pic_path, highest_acc, highest_val_acc, best_model_path = incremental_train(my_callback=self.callback,
                              data_dir=self.training_data_dir, pretrained_model_path=self.pretrained_model,
                              data_type=self.training_data_type, model_save_dir=self.model_save_dir,
                              epochs=self.epochs, batch_size=self.batchsize, validation_set_rate=self.validation_set_rate,
                              learning_rate=self.learning_rate, lr_decay_steps=self.lr_decay_steps, lr_decay_rate=self.lr_decay_rate)
            self.train_result_pic_path = train_result_pic_path
            self.highest_acc = highest_acc
            self.highest_val_acc = highest_val_acc
            self.best_model_path = best_model_path
            self.is_on = False


# 测试模型的线程
class TestModelThread(QThread):
    def __init__(self):
        super(TestModelThread, self).__init__()
        self.is_on = True
        # 测试参数
        self.test_set_dir = ""
        self.model_path = ""
        self.data_type = ""
        # 测试返回值
        self.heatmap_save_path = ""
        self.test_accuracy = 0.0
    def run(self):
        self.handle = ctypes.windll.kernel32.OpenThread(  # @UndefinedVariable
            win32con.PROCESS_ALL_ACCESS, False, str(QThread.currentThread()))
        while self.is_on:
            heatmap_save_path, test_accuracy = test_model(test_data_dir=self.test_set_dir,
                                                          model_path=self.model_path,
                                                          data_type=self.data_type)
            self.heatmap_save_path = heatmap_save_path
            self.test_accuracy = test_accuracy
            self.is_on = False