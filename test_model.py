import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from data_load import data_load_from_test
from save_result import show_heatmaps
from save_dir_generator import get_result_save_dir
import os


plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


def test_model(test_data_dir, model_path, data_type="default"):
    print()
    print("Test Model Info".center(150, "*"))
    print("正在对测试集数据进行测试......")
    test_ds, class_names = data_load_from_test(test_data_dir)
    postfix_list = ['years']
    class_names = ['{} {}'.format(a,b) for a in class_names for b in postfix_list]
    model = tf.keras.models.load_model(model_path)

    # 测试模型
    loss, binary_crossentropy, accuracy = model.evaluate(test_ds)
    # 输出结果
    print('在测试集上的准确率为: ', accuracy)

    test_real_labels = []   # 真实的标签向量
    test_pre_labels = []    # 预测的标签向量
    for test_batch_images, test_batch_labels in test_ds:
        test_batch_labels = test_batch_labels.numpy()   # one-hot类型的所有测试集数据的label
        test_batch_pres = model.predict(test_batch_images)  # 所有测试集数据预测结果的置信度

        test_batch_labels_max = np.argmax(test_batch_labels, axis=1)    # 最大值的索引为该数据的label
        test_batch_pres_max = np.argmax(test_batch_pres, axis=1)    # 最大值的索引为该预测的label

        # 将推理对应的标签取出
        for i in test_batch_labels_max:
            test_real_labels.append(i)
        for i in test_batch_pres_max:
            test_pre_labels.append(i)

    class_names_length = len(class_names)
    heat_maps = np.zeros((class_names_length, class_names_length))
    for test_real_label, test_pre_label in zip(test_real_labels, test_pre_labels):
        heat_maps[test_real_label][test_pre_label] = heat_maps[test_real_label][test_pre_label] + 1

    print("混淆矩阵如下:")
    print(heat_maps)
    heat_maps_sum = np.sum(heat_maps, axis=1).reshape(-1, 1)
    heat_maps_float = heat_maps / heat_maps_sum
    print("归一化混淆矩阵如下:")
    print(heat_maps_float)

    result_total_folder = "./results"
    result_test_folder = os.path.join(result_total_folder, "test")
    result_runs_folder = get_result_save_dir()  # 保存每次训练结果的子目录
    result_img_type_dir = os.path.join(result_test_folder, data_type)
    result_generate_dir = os.path.join(result_img_type_dir, result_runs_folder)

    if not os.path.isdir(result_total_folder):
        os.mkdir(result_total_folder)
    if not os.path.isdir(result_test_folder):
        os.mkdir(result_test_folder)
    if not os.path.isdir(result_img_type_dir):
        os.mkdir(result_img_type_dir)
    if not os.path.isdir(result_generate_dir):
        os.mkdir(result_generate_dir)
    save_sub_dir = os.path.join(data_type, result_runs_folder)

    heatmap_save_path = show_heatmaps(title="Confusion Matrix",
                                      x_labels=class_names,
                                      y_labels=class_names,
                                      harvest=heat_maps_float,
                                      save_dir=save_sub_dir)

    print("*" * 150)
    print()
    # 返回混淆矩阵路径，测试集准确率
    return heatmap_save_path, accuracy

if __name__ == '__main__':
    test_model("./data_split/afm/test",
               "models/best_increment_model_AFM_in_10_epochs.h5")
