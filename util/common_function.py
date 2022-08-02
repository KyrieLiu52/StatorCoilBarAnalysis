import os
import json


def load_json_file(json_path):
    items = {}
    app_path = os.path.abspath(os.getcwd())
    json_path = os.path.normpath(os.path.join(app_path, json_path))
    if not os.path.isfile(json_path):
        print(
            f"WARNING: \"{json_path}\" not found! check in the folder {app_path}")
    with open(json_path, "r", encoding='utf-8') as reader:
        tmp = json.loads(reader.read())
        items = tmp
    return items


def write_json_file(json_path, json_info):
    app_path = os.path.abspath(os.getcwd())
    json_path = os.path.normpath(os.path.join(app_path, json_path))
    if not os.path.isfile(json_path):
        print(f"WARNING: \"{json_path}\" not found! check in the folder {app_path}")

    with open(json_path, "w", encoding='utf-8') as writer:
        json.dump(json_info, writer)


def load_acc(data_type):
    best_model_info = load_json_file("best_model.json")
    highest_val_acc = 0
    highest_acc = 0
    if data_type == "AFM":
        highest_val_acc = best_model_info["afm_model"]["best_val_accuracy"]
        highest_acc = best_model_info["afm_model"]["best_accuracy"]
    elif data_type == "SEM":
        highest_val_acc = best_model_info["sem_model"]["best_val_accuracy"]
        highest_acc = best_model_info["sem_model"]["best_accuracy"]
    elif data_type == "SAXS":
        highest_val_acc = best_model_info["saxs_model"]["best_val_accuracy"]
        highest_acc = best_model_info["saxs_model"]["best_accuracy"]
    elif data_type == "WAXD":
        highest_val_acc = best_model_info["waxd_model"]["best_val_accuracy"]
        highest_acc = best_model_info["waxd_model"]["best_accuracy"]
    return highest_val_acc, highest_acc


def judge_is_copy_model_to_model_dir(data_type, highest_val_acc, highest_acc, best_model_path_in_model_dir):
    if not os.path.isfile(best_model_path_in_model_dir):
        return True
    if judge_is_best_model(data_type, highest_val_acc, highest_acc) is True:
        return True
    else:
        return False


def judge_is_best_model(data_type, highest_val_acc, highest_acc):
    json_highest_val_acc, json_highest_acc = load_acc(data_type)
    if json_highest_val_acc <= highest_val_acc and json_highest_acc < highest_acc:
        return True
    if json_highest_val_acc < highest_val_acc and json_highest_acc > highest_acc:
        if highest_val_acc > highest_acc:
            return False
        else:
            return True
    return False
