import tensorflow as tf


# 从一个训练集文件夹中读取数据，再按照比例划分为train和val
def data_load_from_one_dir(data_dir, img_height=224, img_width=224, batch_size=32, val_rate=0.2):

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        validation_split=val_rate,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        validation_split=val_rate,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = train_ds.class_names
    print(class_names)
    return train_ds, val_ds, class_names


# 从两个已经划分为train和val的文件夹中，读取数据
def data_load_from_train_and_val(data_dir, val_data_dir, img_height=224, img_width=224, batch_size=32):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        label_mode='categorical',
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        val_data_dir,
        label_mode='categorical',
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = train_ds.class_names
    print(class_names)
    return train_ds, val_ds, class_names


# 读取测试集
def data_load_from_test(test_data_dir, img_height=224, img_width=224, batch_size=32):
    test_ds = tf.keras.preprocessing.image_dataset_from_directory(
        test_data_dir,
        label_mode='categorical',
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)
    class_names = test_ds.class_names
    print(class_names)
    return test_ds, class_names
