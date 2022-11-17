import cv2

DEFAULT_COLOR = (0, 255, 0)  # green


def show_window(name, img):
    show_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow(name, show_img)


def draw_rectangle(img, coords, color=DEFAULT_COLOR):
    [x, y, w, h] = coords
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)


def select_region(name, img):
    show_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return cv2.selectROI(name, show_img, fromCenter=False, showCrosshair=False)


def waitKey():
    return cv2.waitKey(1) & 0xFF


def destroyAll():
    cv2.destroyAllWindows()
