from input.realsense_reader import RSReader
import cv2
from processing.pipeline import pipeline as processing_pipeline
from tracking import pipeline as tracker

reader = RSReader()
reader.start_camera()

initBB = None

rectangle_color = (0, 255, 0)  # green

for (color, depth) in reader.get_frames():
    color, depth = processing_pipeline(color, depth)
    (H, W) = color.shape[:2]
    if initBB is not None:
        [x, y, w, h] = tracker.update(color)
        cv2.rectangle(color, (x, y), (x + w, y + h), rectangle_color, 2)

    color_show = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)
    cv2.imshow("RGB", color_show)
    key = cv2.waitKey(1) & 0xFF
    if key & 0xFF == ord('q') or key == 27:
        reader.stop_camera()
        break
    elif key == ord("s"):
        initBB = cv2.selectROI("RGB", color, fromCenter=False,
                               showCrosshair=True)
        tracker.init(color, initBB)
    elif key == 32:
        print("A")
cv2.destroyAllWindows()
