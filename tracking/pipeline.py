from .tracker import get_tracker


def update(color_img):
    tracker = get_tracker()
    success, box = tracker.update(color_img)
    assert success
    return [int(v) for v in box]


def init(color_img, box):
    tracker = get_tracker()
    tracker.init(color_img, box)
