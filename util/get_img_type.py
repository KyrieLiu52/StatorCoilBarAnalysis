import cv2
import numpy as np

def get_img_type(img_path):
    src = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    # src = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = src
    cv2.cvtColor(src, cv2.COLOR_BGR2HSV, img)
    hue_sum = 0.0
    hue_mean = 0.0
    for i in range(len(img)):
        for j in range(len(img[0])):
            hue_sum = hue_sum + img[i][j][0]
    hue_mean = hue_sum / (len(img)*len(img[0]))
    # 新范围
    if hue_mean < 16 and hue_mean > 10:
        return "AFM"
    elif hue_mean < 2 or hue_mean > 175:
        return "SEM"
    elif hue_mean < 119 and hue_mean > 112:
        return "SAXS"
    elif hue_mean < 9 and hue_mean > 3:
        return "WAXD"