import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

# s = "a\na\r"
# print(s)
# s = s.replace("\n", " ")
# print(s)


#
# s = ["1","2","3"]
# print(s)
# if 2 in s:
#     s.remove("2")
# print(s)

# count = 0
# a = "1"
# try:
#     count = count+1
#     a = a + 1
# except:
#     print("error")
#     print(count)
# else:
#     print(count)

# for item,type in [1,2,3], [4,5,6]:
#     print(item,type)

# print("AFM" == "AFM")

# import matplotlib.pyplot as plt
# plt.imread("../data/afm/train/0/AFM_0_20210816_173255_0.tif")

# print("123")
# from util.common_function import load_json_file, write_json_file
#
# best_model_info = load_json_file("../best_model.json")
# highest_val_acc = 0.9325
# highest_acc = 0.9999
# best_model_path = "i am best2"
# print(best_model_info["sem_model"])
#
# if best_model_info["sem_model"]["best_val_accuracy"] < highest_val_acc or (
#         best_model_info["sem_model"]["best_val_accuracy"] == highest_val_acc and
#         best_model_info["sem_model"]["best_accuracy"] < highest_acc):
#     best_model_info["sem_model"]["best_accuracy"] = highest_acc
#     best_model_info["sem_model"]["best_val_accuracy"] = highest_val_acc
#     best_model_info["sem_model"]["best_model_path"] = best_model_path
#     write_json_file("../best_model.json", best_model_info)
#
# print(best_model_info["sem_model"])
#
# path = "./Project/FilterD\\\///river/\\\hello.txt"
# print(os.path.basename(path))

# import time
# print(1)
# time.sleep(5)
# print(2)
#
# import getpass
#
# imagenet_model_dir = "C:/Users/{}/.keras/models".format(getpass.getuser())
# imagenet_model_name = "mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5"
# imagenet_model_path = os.path.join(imagenet_model_dir , imagenet_model_name)
#
# print(os.listdir(imagenet_model_dir))
# print(os.path.exists(imagenet_model_path))

# print("Trainging info".center(100, "-"))
# print("-"*50)

# def get_img_type(img_path):
#     src = cv2.imread(img_path, cv2.IMREAD_COLOR)
#     img = src
#     cv2.cvtColor(src, cv2.COLOR_BGR2HSV, img)
#     hue_sum = 0.0
#     hue_mean = 0.0
#     for i in range(len(img)):
#         for j in range(len(img[0])):
#             hue_sum = hue_sum + img[i][j][0]
#     hue_mean = hue_sum / (len(img)*len(img[0]))
#     # 新范围
#     if hue_mean < 16 and hue_mean > 10:
#         return "AFM"
#     elif hue_mean < 2 or hue_mean > 175:
#         return "SEM"
#     elif hue_mean < 119 and hue_mean > 112:
#         return "SAXS"
#     elif hue_mean < 9 and hue_mean > 3:
#         return "WAXD"
#
#     print(hue_mean)
#     return hue_mean

    # 未截取边框的范围
    # if hue_mean < 10 and hue_mean > 6:
    #     return "AFM"
    # elif hue_mean < 2 or hue_mean > 175:
    #     return "SEM"
    # elif hue_mean < 70 and hue_mean > 60:
    #     return "SAXS"
    # elif hue_mean < 5 and hue_mean > 3:
    #     return "WAXD"

if __name__ == '__main__':
    # dir = "G:/Project_Code/spectrogram_aging/data_onedir_aug/sem"
    # img_list = []
    # for label in os.listdir(dir):
    #     label_dir = os.path.join(dir, label)
    #     for img_name in os.listdir(label_dir):
    #         tmp_img_path = os.path.join(label_dir, img_name)
    #         img_list.append(tmp_img_path)
    # hue_mean_list = []
    # for img_path in img_list:
    #     tmp_hue_mean = get_img_type(img_path)
    #     hue_mean_list.append(tmp_hue_mean)
    #
    # x = np.array(hue_mean_list)
    # y = np.ones((1,len(hue_mean_list)))
    # plt.scatter(x, y, c="green")
    # plt.show()

    # path = "G:/Project_Code/spectrogram_aging/data_onedir_aug/saxs/0/C1-1 - 3_contrast.png"
    # print(get_img_type(path))

    src_dir = "./data/test/111/test.txt"
    # if src_dir[-1] == "\\" or src_dir[-1] == "/" :
    #     src_dir = src_dir[:-1]
    # print(src_dir)
    filename = os.path.basename(src_dir)
    print(filename)
    # print(os.path.join(head,"test"))

