import os

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 设置中文字体和负号正常显示
from util.common_function import load_json_file

def draw_best_model_hist(best_model_json_path, pic_save_dir):
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False

    best_model_info = load_json_file(best_model_json_path)
    afm_model_info = best_model_info["afm_model"]
    sem_model_info = best_model_info["sem_model"]
    saxs_model_info = best_model_info["saxs_model"]
    waxd_model_info = best_model_info["waxd_model"]

    plt.figure(figsize=(8, 5))
    data_type_list = ['AFM', 'SEM', 'SAXS', 'WAXD']  # 横坐标刻度显示值
    accuracy_list = [afm_model_info["best_accuracy"],
                     sem_model_info["best_accuracy"],
                     saxs_model_info["best_accuracy"],
                     waxd_model_info["best_accuracy"]]  # 纵坐标值1
    val_accuracy_list = [afm_model_info["best_val_accuracy"],
                         sem_model_info["best_val_accuracy"],
                         saxs_model_info["best_val_accuracy"],
                         waxd_model_info["best_val_accuracy"]]  # 纵坐标值2
    x = range(len(accuracy_list))
    accuracy_list = np.around(accuracy_list, decimals=4)
    val_accuracy_list = np.around(val_accuracy_list, decimals=4)

    rects1 = plt.bar(x=x, height=accuracy_list, width=0.4, alpha=0.8, label="Accuracy")
    rects2 = plt.bar(x=[i + 0.4 for i in x], height=val_accuracy_list, width=0.4, label="Val Accuracy")
    plt.ylim(0, 1.09)  # y轴取值范围
    plt.ylabel("准确率")

    plt.xticks([index + 0.2 for index in x], data_type_list)
    plt.xlabel("谱图类型")
    plt.title("最佳模型准确率")
    plt.legend(loc='lower right')  # 设置题注
    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.01, str(height), ha="center", va="bottom")
    for rect in rects2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.01, str(height), ha="center", va="bottom")
    plt.gcf().subplots_adjust(left=0.08)
    plt.gcf().subplots_adjust(right=0.95)
    plt.gcf().subplots_adjust(top=0.92)
    # plt.show()
    pic_save_path = os.path.join(pic_save_dir, "best_model_hist.png")
    plt.savefig(pic_save_path, format='png', transparent=True)

if __name__ == '__main__':
    draw_best_model_hist("../best_model.json", "../images")
