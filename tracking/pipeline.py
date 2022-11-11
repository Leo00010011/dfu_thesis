# import cv2
from cv2 import cv2


def pipeline(color_img):
    tracker = cv2.TrackerCSRT_create()
