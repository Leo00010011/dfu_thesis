import numpy as np
import time

from images.masking import save_crop, update_reconstruction_masks
from images.utils.names_generator import numeric_names
from input.realsense_reader import RSReader
import presentation.windows as windows
from processing.pipeline import pipeline as processing_pipeline
from tracking import pipeline as tracker
from reconstruction.pipeline import pipeline as reconstruction_pipeline
from segmentation.predictor import predict as segmentation_pipeline


reader = RSReader()
reader.start_camera()
reader.save_intrinsic()

camera_resolution = (reader.rs.get_metadata().height,
                     reader.rs.get_metadata().width)
print(camera_resolution)

names = numeric_names()

bound_box = None

for (color, depth) in reader.get_frames():
    color, depth = processing_pipeline(color, depth)
    color_cp = np.copy(color)

    if bound_box is not None:
        coords = tracker.update(color_cp)
        windows.draw_rectangle(color_cp, coords)
        save_crop(color, depth, coords, next(names))

    windows.show_window('CameraStream', color_cp)

    key = windows.waitKey()
    if key == ord('q') or key == 27:
        reader.stop_camera()
        break
    elif key == ord("s"):
        bound_box = windows.select_region("CameraStream", color_cp)
        tracker.init(color_cp, bound_box)

windows.destroyAll()
time.sleep(2)

# segmentation_pipeline()
# update_reconstruction_masks(camera_resolution)

reconstruction_pipeline()
