import numpy as np
import cv2

KERNEL = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])


def focus(img):
    img = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=np.std(img))
    return cv2.filter2D(img, -1, KERNEL)
