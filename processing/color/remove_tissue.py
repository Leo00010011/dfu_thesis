import numpy as np
# import cv2
from cv2 import cv2
from scipy.ndimage.morphology import binary_fill_holes


def remove_tissue(img):
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])

    imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(imgHSV, low_green, high_green)
    mask = 255-mask
    mask = binary_fill_holes(mask > 0)
    # mask must be calculated
    assert(mask is not None)

    mask = mask.astype(np.uint8)
    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN,  cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    res = cv2.bitwise_and(img, img, mask=mask)
    res[(mask == 0)] = [255, 255, 255]
    return res
