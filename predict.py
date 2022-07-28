import math
import os
import shutil

import scipy.stats
import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib

from save_dir_generator import get_result_save_dir

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

def save_result_pic(labels, confidences, save_path):
    max_index = 0
    max_confidence = confidences[0]
    max_confidence_2 = confidences[0]
    for i in range(1, len(confidences)):
        if confidences[i] > max_confidence:
            max_confidence_2 = max_confidence
            max_index = i
            max_confidence = confidences[i]
    max_confidence = max_confidence * (1 - max_confidence_2)
    # 范围为0-15，刻度为1/20
    sep_N = 15 * 20
    gen_labels = []
    gen_confidence = []

    for i in range(sep_N):
        gen_labels.append(i*15 / sep_N)
    for i in range(sep_N):
        gen_confidence.append(0)
    gen_max_index = 0
    for i in range(len(gen_labels)):
        if gen_labels[i] == labels[max_index]:
            gen_max_index = i
            break
    a = confidences[max_index] * 0.1
    b = gen_labels[gen_max_index]
    pi = 3.1415926
    c = pow(1 / (a * math.sqrt(2 * pi)), 2)
    for i in range(len(gen_labels)):
        gen_confidence[i] = a * math.exp(-pow(gen_labels[i] - b, 2)/(2*c))
    gen_confidence = np.multiply(gen_confidence, 10)

    plt.figure(figsize=(7, 5)) # 不声明一个新的画布，就会将当前的绘画绘制在上次的画布中
    plt.plot(gen_labels, gen_confidence, linewidth=2, markersize=12, label="Confidence")
    plt.axis([-0.5, 15, -0.05, 1.05])
    plt.xlabel('谱图年份', fontsize=14)
    plt.ylabel('置信度', fontsize=14)
    plt.legend()
    plt.grid(color='black', alpha=0.2)

    plt.gcf().subplots_adjust(left=0.1)
    plt.gcf().subplots_adjust(right=0.95)
    plt.gcf().subplots_adjust(top=0.95)

    # plt.show()
    plt.savefig(save_path, format="png", transparent=True)


def visualize_feature_map(img_batch, save_path):
    feature_map = np.squeeze(img_batch, axis=0)
    print(feature_map.shape)

    feature_map_combination = []
    plt.figure(figsize=(7, 5))

    num_pic = feature_map.shape[2]
    row = 4
    col = num_pic // row
    for i in range(0, num_pic):
        feature_map_split = feature_map[:, :, i]
        feature_map_combination.append(feature_map_split)
        plt.subplot(row, col, i + 1)
        plt.imshow(feature_map_split, cmap="gray")
        plt.axis('off')
        plt.title('feature_map_{}'.format(i), fontdict={'size': 6})

    plt.gcf().subplots_adjust(left=0.02)
    plt.gcf().subplots_adjust(bottom=0.02)
    plt.gcf().subplots_adjust(right=0.98)
    plt.gcf().subplots_adjust(top=0.96)
    plt.show()
    plt.savefig(save_path, format="png", transparent=True)
    # 各个特征图按1：1 叠加
    # feature_map_sum = sum(ele for ele in feature_map_combination)
    # plt.imshow(feature_map_sum)


def predict_image(img_path, model_path, img_type, save_folder):
    class_names = ["0", "10", "13"]
    result_img_type_dir = os.path.join(save_folder, img_type)
    predict_result_save_dir = os.path.join(result_img_type_dir, get_result_save_dir())
    if not os.path.isdir(result_img_type_dir):
        os.mkdir(result_img_type_dir)
    if not os.path.isdir(predict_result_save_dir):
        os.mkdir(predict_result_save_dir)

    img_name = os.path.basename(img_path)
    result_path = os.path.join(predict_result_save_dir, "predict_result_pic.png")   # 预测结果图的路径，用于保存结果和返回路径给前端
    feature1_path = os.path.join(predict_result_save_dir, "mid_feature1_pic.png")   # 中间特征_1 的路径
    feature2_path = os.path.join(predict_result_save_dir, "mid_feature2_pic.png")   # 中间特征_2 的路径
    src_img_path = os.path.join(predict_result_save_dir, img_name)   # 将原图复制一份，保存在测试结果目录下

    model = tf.keras.models.load_model(model_path)

    img_init = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)  # 打开图片
    # img_init = cv2.imread(img_path)
    img_init = cv2.resize(img_init, (224, 224))
    img = np.asarray(img_init)

    model_slice_1 = tf.keras.models.Model(inputs=model.get_layer("mobilenetv2_1.00_224").input,
                                          outputs=model.get_layer("mobilenetv2_1.00_224").get_layer("Conv1").output,
                                          name="model_slice")
    mid_model_1 = tf.keras.Sequential([
        model.get_layer("rescaling"),
        model_slice_1
    ])
    model_slice_feature_1 = mid_model_1.predict(img.reshape(1, 224, 224, 3))

    model_slice_2 = tf.keras.models.Model(inputs=model.get_layer("mobilenetv2_1.00_224").input,
                                          outputs=model.get_layer("mobilenetv2_1.00_224").get_layer(
                                              "block_1_project_BN").output,
                                          name="model_slice")
    mid_model_2 = tf.keras.Sequential([
        model.get_layer("rescaling"),
        model_slice_2
    ])
    model_slice_feature_2 = mid_model_2.predict(img.reshape(1, 224, 224, 3))

    visualize_feature_map(model_slice_feature_1, save_path=feature1_path)
    visualize_feature_map(model_slice_feature_2, save_path=feature2_path)

    outputs = model.predict(img.reshape(1, 224, 224, 3))
    predict_index = np.argmax(outputs)
    predict_label = class_names[predict_index]

    predict_result = predict_label + "年"
    confidence = outputs[0][predict_index]
    save_result_pic(labels=[0, 10, 13], confidences=outputs[0], save_path=result_path)

    shutil.copy(img_path, src_img_path)

    # 返回预测结果，置信度，结果图的路径，中间特征层1的图片，中间特征层2的图片， 被检测的原图
    return predict_result, confidence, result_path, feature1_path, feature2_path, src_img_path


if __name__ == '__main__':
    predict_image("./test_code/PPT_SAXS.png",
                  "models/saxs.h5", "SAXS", "inference_result_tmp")
    # save_result_pic([0,10,13],[0.9,0.0,0.1],"")
