import tensorflow as tf

class My_Callback(tf.keras.callbacks.Callback):
    def __init__(self):
        super(My_Callback, self).__init__()
        # self.count = 0
        self.click_off = False

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch = epoch
        print('\n')

    def on_batch_end(self, batch, logs={}):
        if self.click_off is True:
            self.model.stop_training = True