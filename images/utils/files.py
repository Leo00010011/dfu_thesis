import cv2
import numpy as np


def open_image(filename: str, gray=False):
    img = cv2.cvtColor(cv2.imread(filename),
                       cv2.COLOR_BGR2GRAY if gray else cv2.COLOR_BGR2RGB)
    return img


def get_image(filename: str, preprocess_input=None):
    x = open_image(filename)
    if x.shape[0] > x.shape[1]:
        x_padded = cv2.copyMakeBorder(
            x, 0, 0, 0, (x.shape[0] - x.shape[1]), cv2.BORDER_CONSTANT, value=0)
    else:
        x_padded = cv2.copyMakeBorder(
            x, 0, (x.shape[1] - x.shape[0]), 0, 0, cv2.BORDER_CONSTANT, value=0)
    resize_target = int(int(x_padded.shape[0] / 32) * 32) + 32
    if resize_target < 96:
        resize_target = 96
    if not preprocess_input is None:
        x_padded = preprocess_input(x_padded)
    return cv2.resize(x_padded, (resize_target, resize_target)), x.shape, x_padded.shape
