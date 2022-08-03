
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import make_interp_spline

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

def save_result_pic(confidence, save_path):
    # 为labels添,15，为confidence添加0，因为插值至少需要4个点
    labels = [0, 10, 13]
    label_1 = labels[0]
    label_2 = labels[1]
    label_3 = labels[2]

    _labels = labels
    _confidence = confidence

    pre_add_num = 5
    for i in range(pre_add_num):
        _labels = np.insert(_labels, 0, label_1-i-1)
        _confidence = np.insert(_confidence, 0, 0)

    pre_added_num = pre_add_num + 1
    count = 1
    inter_nums_12 = label_2 - label_1 # 两个之间的间隔：如0和5之间有5个间隔
    confidence_interval_12 = (confidence[1]-confidence[0])/inter_nums_12
    for i in range(label_1+1, label_2):
        _labels = np.insert(_labels, pre_added_num + count - 1, i)
        tmp_confidence = confidence[0] + confidence_interval_12 * count
        _confidence = np.insert(_confidence, pre_added_num + count - 1, tmp_confidence)
        count = count + 1

    pre_added_num = pre_added_num + label_2 - label_1
    count = 1
    inter_nums_23 = label_3 - label_2  # 两个之间的间隔：如0和5之间有5个间隔
    confidence_interval_23 = (confidence[2] - confidence[1]) / inter_nums_23
    for i in range(label_2 + 1, label_3):
        _labels = np.insert(_labels, pre_added_num + count - 1, i)
        tmp_confidence = confidence[1] + confidence_interval_23 * count
        _confidence = np.insert(_confidence, pre_added_num + count - 1, tmp_confidence)
        count = count + 1

    # pre_added_num = pre_added_num + label_3 - label_2
    # index = pre_added_num + 1 - 1
    after_add_num = 5
    for i in range(after_add_num):
        _labels = np.append(_labels, label_3 + i + 1)
        _confidence = np.append(_confidence, 0)

    print(_labels)
    print(_confidence)

    x = np.array(_labels)
    y = np.array(_confidence)

    x_smooth = np.linspace(x.min(), x.max(), 300)  # 300 represents number of points to make between x.min and x.max
    y_smooth = make_interp_spline(x, y)(x_smooth)

    plt.figure(figsize=(7, 5))
    plt.plot(x_smooth, y_smooth, linewidth=2, markersize=12, label="Confidence")

    plt.xlabel("谱图年份")
    plt.ylabel("置信度")

    plt.axis([-0.5, 14.5, -0.05, 1.05])  # plt.axis([xmin,xmax,ymin,ymax])
    plt.legend(loc="upper right")

    plt.show()

if __name__ == '__main__':
    save_result_pic([0,0.9,0.1],"")