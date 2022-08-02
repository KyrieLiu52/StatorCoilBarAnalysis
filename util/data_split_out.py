import os
import random
import shutil

'''
    从某个数据集中，划分出一部分数据：
    规则：
        1）如果target中没有数据，则从src中划分出split_scale
        2）如果target中有数据，则将target移动到src中，再重新进行划分
'''
def data_set_split_out(src_data_folder, target_data_folder, split_scale = 0.2):
    print()
    print("Split Data Set Info".center(150, "*"))
    print("从{0}中,划分出{2}%的数据,到{1}".format(src_data_folder,target_data_folder,split_scale*100))

    # 创建目录
    if not os.path.isdir(target_data_folder):
        os.mkdir(target_data_folder)
    label_names = os.listdir(src_data_folder)
    print("共{}类,分别为:{}".format(len(label_names), label_names))

    for label_name in label_names:
        src_label_name_path = os.path.join(src_data_folder, label_name)
        target_label_name_path = os.path.join(target_data_folder, label_name)
        if not os.path.isdir(target_label_name_path):
            # 如果不存在该label的target path，则新建
            os.mkdir(target_label_name_path)
        else:
            # 如果存在，则将其目录下的所有图片都移动到src下面的对应label目录中
            target_label_origin_imgs = os.listdir(target_label_name_path)
            for img_name in target_label_origin_imgs:
                target_img_path = os.path.join(target_label_name_path, img_name)
                tmp_src_img_path = os.path.join(src_label_name_path, img_name)
                if os.path.isfile(tmp_src_img_path):
                    shutil.copy(target_img_path, src_label_name_path)
                    os.remove(target_img_path)
                else:
                    shutil.move(target_img_path, src_label_name_path)

    # 划出数据
    for label_name in label_names:
        current_label_name_path = os.path.join(src_data_folder, label_name)
        # 获取当前label目录下的所有数据信息
        current_data = os.listdir(current_label_name_path)
        current_data_length = len(current_data)
        current_data_index_list = list(range(current_data_length))
        # 将current_data_index_list随机打乱
        random.shuffle(current_data_index_list)

        split_stop_flag = current_data_length * split_scale
        count = 0
        split_out_num = 0
        target_label_name_path = os.path.join(target_data_folder, label_name)

        for i in current_data_index_list:
            src_img_path = os.path.join(current_label_name_path, current_data[i])
            count = count + 1
            if count <= split_stop_flag:
                shutil.move(src_img_path, target_label_name_path)
                split_out_num = split_out_num + 1
            else:
                break
        print("从{}类中，划出了{}%的数据，一共{}张".format(label_name,split_scale*100,split_out_num))
    print("*" * 150)
    print()

if __name__ == '__main__':
    data_set_split_out("./data_split_out_folder/train", "./data_split_out_folder/test")