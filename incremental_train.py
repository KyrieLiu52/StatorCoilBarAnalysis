import shutil
from time import time

import numpy as np
import tensorflow as tf
from data_load import data_load_from_one_dir
import os

from save_dir_generator import get_result_save_dir
from save_result import *
from util.common_function import *


def model_load_pre(pretrained_model_path, learning_rate=0.001, lr_decay_steps=20, lr_decay_rate=1):
    model = tf.keras.models.load_model(pretrained_model_path)
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=learning_rate,
        decay_steps=lr_decay_steps,
        decay_rate=lr_decay_rate
    )
    model.compile(optimizer=tf.optimizers.Adam(learning_rate = lr_schedule),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['binary_crossentropy', 'accuracy'])
    return model

def incremental_train(my_callback, data_dir, pretrained_model_path, data_type, model_save_dir="models", epochs=30, batch_size=32,
                      validation_set_rate=0.2, learning_rate=0.001, lr_decay_steps=20, lr_decay_rate=1):
    print()
    print("Training Info".center(150, "*"))
    begin_time = time()

    result_total_folder = "./results"
    result_train_folder = os.path.join(result_total_folder, "incremental_train")
    result_runs_folder = get_result_save_dir()  # 保存每次训练结果的子目录
    result_img_type_dir = os.path.join(result_train_folder, data_type)
    result_generate_dir = os.path.join(result_img_type_dir, result_runs_folder)  # 保存结果的完整目录
    result_model_dir = os.path.join(result_generate_dir, "models")  # 保存结果中模型的完整目录

    if not os.path.isdir(result_total_folder):
        os.mkdir(result_total_folder)
    if not os.path.isdir(result_train_folder):
        os.mkdir(result_train_folder)
    if not os.path.isdir(result_img_type_dir):
        os.mkdir(result_img_type_dir)
    if not os.path.isdir(result_generate_dir):
        os.mkdir(result_generate_dir)
    if not os.path.isdir(result_model_dir):
        os.mkdir(result_model_dir)

    model_dir = model_save_dir  # 保存在models文件夹的模型的目录

    train_ds, val_ds, class_names = data_load_from_one_dir(data_dir=data_dir, batch_size=batch_size, val_rate=validation_set_rate)

    model = model_load_pre(pretrained_model_path=pretrained_model_path, learning_rate=learning_rate, lr_decay_steps=lr_decay_steps, lr_decay_rate=lr_decay_rate)
    model.summary()
    increment_at = 2
    for layers in model.layers[:increment_at]:
        layers.trainable = False

    best_model_name = "best_increment_model_{}_in_{}_epochs.h5".format(data_type, epochs)  # 保存最好的model文件名的格式
    last_model_name = "last_increment_model_{}_in_{}_epochs.h5".format(data_type, epochs)
    best_model_path = os.path.join(result_model_dir, best_model_name)
    last_model_path = os.path.join(result_model_dir, last_model_name)

    checkpoint = tf.keras.callbacks.ModelCheckpoint(best_model_path, monitor="val_accuracy",
                                                    verbose=0, save_best_only=True, mode='max')
    callbacks_list = [checkpoint, my_callback]

    print("Training image type is {}".format(data_type))

    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks_list)

    # 表示被中止训练
    if my_callback.click_off is True:
        return "", 0, 0, ""

    end_time = time()
    run_time = end_time - begin_time
    print("训练完成!")
    print('训练时间为: ', run_time, "s")

    highest_val_acc = np.max(history.history['val_accuracy'])
    last_val_acc = history.history['val_accuracy'][-1]
    print("所有epochs中在验证集上最高准确率为{:.4f},该epoch的模型保存在{}".format(highest_val_acc, best_model_path))
    print("最后一个epoch在验证集上的准确率为{:.4f},该epoch的模型保存在{}".format(last_val_acc, last_model_path))
    highest_val_acc_index = np.argmax(history.history['val_accuracy'])
    highest_acc = history.history['accuracy'][highest_val_acc_index]

    model.save(last_model_path)
    best_model_path_in_model_dir = os.path.join(model_dir, best_model_name)
    if judge_is_copy_model_to_model_dir(data_type, highest_val_acc, highest_acc, best_model_path_in_model_dir):
        shutil.copy(best_model_path, model_dir)  # 把在checkpoint中找到的最佳模型，复制到models目录下（之前保存在每次运行的目录下）

    # 生成一个保存的目录save_dir ,传入绘制图像的函数中
    save_sub_dir = os.path.join(data_type, result_runs_folder)
    train_result_pic_path = save_loss_acc(history, save_dir="incremental_train", save_generator_dir=save_sub_dir)
    save_train_history(history, save_dir="incremental_train", save_generator_dir=save_sub_dir)

    print("*" * 150)
    print()

    # 返回训练结果折线图路径，最高的测试集准确率，最高的验证集准确率，最佳的模型路径
    return train_result_pic_path, highest_acc, highest_val_acc, best_model_path_in_model_dir


if __name__ == '__main__':
    incremental_train()