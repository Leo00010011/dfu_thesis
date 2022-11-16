from processing.color.contrast.clahe import CLAHE
import cv2
import numpy as np
from processing.color.contrast.agcwd import image_agcwd


def process_bright(rgb_img):
    img_negative = 255 - rgb_img
    agcwd = image_agcwd(img_negative, a=0.25, truncated_cdf=False)
    reversed = 255 - agcwd
    return reversed


def process_dimmed(rgb_img):
    agcwd = image_agcwd(rgb_img, a=0.75, truncated_cdf=True)
    return agcwd


def pipeline(rgb_img):
    rgb_img = CLAHE(rgb_img)
    YCrCb = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2YCrCb)
    Y = YCrCb[:, :, 0]
    # Determine whether image is bright or dimmed
    threshold = 0.3
    exp_in = 112  # Expected global average intensity
    M, N = rgb_img.shape[:2]
    mean_in = np.sum(Y/(M*N))
    t = (mean_in - exp_in) / exp_in
    if t < -threshold:  # Dimmed Image
        result = process_dimmed(Y)
        YCrCb[:, :, 0] = result
        return cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2RGB)
    elif t > threshold:
        result = process_bright(Y)
        YCrCb[:, :, 0] = result
        return cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2RGB)
    return rgb_img
