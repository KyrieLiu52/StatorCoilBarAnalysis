import tensorflow as tf
from time import *
import os
import numpy as np


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
            print(f"\nStopping at Epoch {self.epoch}, Batch {batch}")
            self.model.stop_training = True


def data_load_from_one_dir(data_dir, img_height=224, img_width=224, batch_size=32):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = train_ds.class_names
    print(class_names)
    return train_ds, val_ds, class_names


def model_load_saxs(IMG_SHAPE=(224, 224, 3), class_num=3):
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights="imagenet")
    base_model.trainable = False
    model = tf.keras.models.Sequential([
        tf.keras.layers.experimental.preprocessing.Rescaling(1. / 127.5, offset=-1, input_shape=IMG_SHAPE),
        base_model,
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(class_num, activation='softmax'),
    ])

    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=20,
        decay_rate=1
    )
    model.compile(optimizer=tf.optimizers.Adam(learning_rate=lr_schedule),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['binary_crossentropy', 'accuracy'])
    return model


# default is best from experiment
def train_saxs(my_callback, data_dir="data_split/saxs/train", batch_size=32, epochs=30):
    begin_time = time()

    model = model_load_saxs()
    train_ds, val_ds, class_names = data_load_from_one_dir(data_dir=data_dir, batch_size=batch_size)
    # model.summary()

    checkpoint = tf.keras.callbacks.ModelCheckpoint("models/best.h5", monitor="val_accuracy",
                                                    verbose=0, save_best_only=True, mode='max')
    callbacks_list = [checkpoint, my_callback]

    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks_list)

    end_time = time()
    run_time = end_time - begin_time
    print("训练完成!")
    print('训练时间为: ', run_time, "s")

    highest_acc = np.max(history.history['val_accuracy'])
    last_acc = history.history['val_accuracy'][-1]
    print("所有epochs中最高准确率为{:.4f},该epoch模型保存在...".format(highest_acc))
    print("最后一个epoch的准确率为{:.4f},该epoch模型保存在...".format(last_acc))


if __name__ == "__main__":
    my_callback = My_Callback()
    my_callback.click_off=True
    train_saxs(my_callback=my_callback, data_dir="../data_split/saxs/train", epochs=30)
