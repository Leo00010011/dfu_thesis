import cv2

tracker = cv2.TrackerMIL_create()


def get_tracker():
    return tracker
