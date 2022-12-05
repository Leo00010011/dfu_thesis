import cv2

# Tracker CSR-DCT
# tracker = cv2.TrackerCSRT_create()
tracker = cv2.TrackerMIL_create()


def get_tracker():
    return tracker
