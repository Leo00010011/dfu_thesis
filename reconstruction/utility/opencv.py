def initialize_opencv():
    opencv_installed = True
    try:
        import cv2
        # from cv2 import cv2
    except ImportError:
        pass
        print("OpenCV is not detected. Using Identity as an initial")
        opencv_installed = False
    if opencv_installed:
        print("OpenCV is detected. Using ORB + 5pt algorithm")
    return opencv_installed
