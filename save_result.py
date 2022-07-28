import matplotlib.pyplot as plt
import os
import pickle
import numpy as np


def save_loss_acc(history, save_dir="default", save_generator_dir="default_type"):
    # 从history中提取模型训练集和验证集准确率信息和误差信息
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # 按照上下结构将图画输出
    plt.figure(figsize=(9, 9))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right', fontsize=12)
    plt.ylabel('Accuracy', fontsize=14)
    plt.ylim([min(plt.ylim()), 1])
    plt.title('Training and Validation Accuracy', fontsize=16)

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right', fontsize=12)
    plt.ylabel('Cross Entropy', fontsize=14)
    plt.title('Training and Validation Loss', fontsize=16)
    plt.xlabel('epoch', fontsize=14)

    save_dir = os.path.join("./results", save_dir)
    save_generator_dir = os.path.join(save_dir, save_generator_dir)
    save_path = os.path.join(save_generator_dir, "loss_and_acc.png")
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    if not os.path.isdir(save_generator_dir):
        os.mkdir(save_generator_dir)
    plt.gcf().subplots_adjust(bottom=0.07)
    plt.gcf().subplots_adjust(top=0.95)
    plt.gcf().subplots_adjust(left=0.1)
    plt.gcf().subplots_adjust(right=0.95)
    # plt.show()
    plt.savefig(save_path, dpi=100, format="png")
    return save_path


def save_train_history(history, save_dir="default", save_generator_dir="default_type"):
    save_dir = os.path.join("./results", save_dir)
    save_generator_dir = os.path.join(save_dir, save_generator_dir)
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    if not os.path.isdir(save_generator_dir):
        os.mkdir(save_generator_dir)

    hist_save_path = os.path.join(save_generator_dir, "train_history.pickle")
    with open(hist_save_path, 'wb') as file:
        pickle.dump(history.history, file)

    highest_acc = np.max(history.history['val_accuracy'])
    ha_save_path = os.path.join(save_generator_dir, "highest_acc_{:.6f}.txt".format(highest_acc))
    with open(ha_save_path, 'wb') as file:
        pickle.dump("the highest accuracy is {0}".format(highest_acc), file, 0) #第三个参数0 表示ASCII编码


def load_train_history(file_path):
    with open(file_path, 'rb') as f:
        h = pickle.load(f)
    return h

def show_heatmaps(title, x_labels, y_labels, harvest, save_dir="default"):
    fig, ax = plt.subplots()
    im = ax.imshow(harvest, cmap=plt.cm.Blues)

    ax.set_xticks(np.arange(len(y_labels)))
    ax.set_yticks(np.arange(len(x_labels)))
    ax.set_xticklabels(y_labels)
    ax.set_yticklabels(x_labels)

    # 因为x轴的标签太长了，所以旋转45
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # 每个map的具体数值
    for i in range(len(x_labels)):
        for j in range(len(y_labels)):
            text = ax.text(j, i, round(harvest[i, j], 2),
                           ha="center", va="center", color="black")
    ax.set_xlabel("Predict label", fontsize=14)
    ax.set_ylabel("Actual label", fontsize=14)
    ax.set_title(title, fontsize=16)
    fig.tight_layout()
    plt.colorbar(im)

    save_dir = os.path.join("./results/test", save_dir)
    save_path = os.path.join(save_dir, "heatmap.png")

    plt.gcf().subplots_adjust(left=0.05)

    # plt.show()
    plt.savefig(save_path, dpi=100)
    return save_path

class MyHistory():
    def __init__(self):
        self.history = {}

if __name__ == '__main__':
    my_history = MyHistory()
    my_history.history = load_train_history("results/train/afm/result_20210828_132505/train_history.pickle")
    save_loss_acc(my_history)
    print(1)
    # class_names = ['0','10','13']
    # postfix_list = ['years']
    # class_names = ['{} {}'.format(a, b) for a in class_names for b in postfix_list]
    # heat_maps = np.zeros((3, 3))
    # heat_maps_sum = np.sum(heat_maps, axis=1).reshape(-1, 1)
    # heat_maps_float = heat_maps / heat_maps_sum
    #
    # heatmap_save_path = show_heatmaps(title="Confusion Matrix",
    #                                   x_labels=class_names,
    #                                   y_labels=class_names,
    #                                   harvest=heat_maps_float)