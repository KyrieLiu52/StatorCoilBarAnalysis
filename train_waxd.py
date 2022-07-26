import numpy as np
import tensorflow as tf
from time import *
from data_load import data_load_from_one_dir
from save_dir_generator import get_result_save_dir
import os
import shutil
from save_result import save_loss_acc, save_train_history
from util.common_function import *


def model_load_waxd(IMG_SHAPE=(224, 224, 3), class_num=3, learning_rate=0.001, lr_decay_steps=20, lr_decay_rate=1, dropout_rate=0.2):
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                   include_top=False,
                                                   weights="imagenet")
    base_model.trainable = False
    model = tf.keras.models.Sequential([
        tf.keras.layers.experimental.preprocessing.Rescaling(1. / 127.5, offset=-1, input_shape=IMG_SHAPE),
        base_model,
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(class_num, activation='softmax'),
    ])
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=learning_rate,
        decay_steps=lr_decay_steps,
        decay_rate=lr_decay_rate
    )
    model.compile(optimizer=tf.optimizers.Adam(learning_rate=lr_schedule),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=['binary_crossentropy', 'accuracy'])
    return model


# default is best from experiment
def train_waxd(my_callback, data_dir="data/waxd/train", model_save_dir="models", epochs=30, batch_size=32,
              validation_set_rate=0.2, learning_rate=0.001, lr_decay_steps=20, lr_decay_rate=1, dropout_rate=0.2):
    print()
    print("Training Info".center(150, "*"))
    begin_time = time()

    result_total_folder = "./results"
    result_train_folder = os.path.join(result_total_folder, "train")
    result_runs_folder = get_result_save_dir()  # 保存每次训练结果的子目录
    result_img_type_dir = os.path.join(result_train_folder, "waxd")
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

    train_ds, val_ds, class_names = data_load_from_one_dir(data_dir=data_dir, batch_size=batch_size, val_rate = validation_set_rate)
    model = model_load_waxd(class_num=len(class_names), learning_rate=learning_rate, lr_decay_steps=lr_decay_steps, lr_decay_rate=lr_decay_rate, dropout_rate=dropout_rate)
    model.summary()

    best_model_name = "best_mobilenet_WAXD" + "_in_" + str(epochs) + "_epochs.h5"  # 保存最好的model文件名的格式
    last_model_name = "last_mobilenet_WAXD" + "_in_" + str(epochs) + "_epochs.h5"  # 保存最后一个epoch的model文件名的格式

    best_model_path = os.path.join(result_model_dir, best_model_name)
    last_model_path = os.path.join(result_model_dir, last_model_name)

    # 保存所欲epochs中最好的模型
    # verbose = 0 : 不在控制台输出检查点的信息

    checkpoint = tf.keras.callbacks.ModelCheckpoint(best_model_path, monitor="val_accuracy",
                                                    verbose=0, save_best_only=True, mode='max')
    callbacks_list = [checkpoint, my_callback]

    print("Training image type is WAXD")

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
    if judge_is_copy_model_to_model_dir("WAXD", highest_val_acc, highest_acc, best_model_path_in_model_dir):
        shutil.copy(best_model_path, model_dir)  # 把在checkpoint中找到的最佳模型，复制到models目录下（之前保存在每次运行的目录下）

    # 生成一个保存的目录save_dir ,传入绘制图像的函数中
    save_sub_dir = os.path.join("waxd", result_runs_folder)
    train_result_pic_path = save_loss_acc(history, save_dir="train", save_generator_dir=save_sub_dir)
    save_train_history(history, save_dir="train", save_generator_dir=save_sub_dir)

    print("*" * 150)
    print()

    # 返回训练结果折线图路径，最高的测试集准确率，最高的验证集准确率，最佳的模型路径
    return train_result_pic_path, highest_acc, highest_val_acc, best_model_path_in_model_dir


if __name__ == "__main__":
    train_waxd("data_split/waxd/train", epochs=10)
