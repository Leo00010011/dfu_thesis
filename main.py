from report.pipeline import pipeline as report_pipeline
from reconstruction.pipeline import pipeline as reconstruction_pipeline
from measurement.pipeline import pipeline as measurement_pipeline
from segmentation.predictor import predict as segmentation_pipeline
from images.masking import save_crop, update_reconstruction_masks
from processing.pipeline import pipeline as processing_pipeline
from images.utils.names_generator import numeric_names
from output.pipeline import clear_output_pipeline
from input.realsense_reader import RSReader
from tracking import pipeline as tracker
from data.pipeline import data_pipeline
import presentation.windows as windows
import numpy as np
import time
import open3d as o3d
import os
# ignore TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)


if __name__ == "__main__":
    # clear output of previous execution
    # clear_output_pipeline()

    # read data pipeline
    patient = data_pipeline()

    # # initialize the camera reader
    # reader = RSReader()
    # # start recording with camera
    # reader.start_camera()
    # # save in json file the intrinsic matrix of the camera
    # reader.save_intrinsic()

    # # save the resolution of the camera
    # camera_resolution = (reader.rs.get_metadata().height,
    #                      reader.rs.get_metadata().width)

    # names = numeric_names()

    # bound_box = None

    # # # read frames from camera
    # for (color, depth) in reader.get_frames():
    #     # preprocess each frame
    #     color, depth = processing_pipeline(color, depth)
    #     color_cp = np.copy(color)

    #     # update bounding box of tracker
    #     if bound_box is not None:
    #         coords = tracker.update(color_cp)
    #         windows.draw_rectangle(color_cp, coords)
    #         # save images
    #         save_crop(color, depth, coords, next(names))

    #     # show window with frame
    #     windows.show_window('DFU Camera', color_cp)

    #     # wait for interaction
    #     key = windows.waitKey()
    #     # if interaction is q or ESC then stop recording
    #     if key == ord('q') or key == 27:
    #         reader.stop_camera()
    #         break
    #     # if interaction is s then select DFU region
    #     elif key == ord("s"):
    #         bound_box = windows.select_region("DFU Camera", color_cp)
    #         # init tracker
    #         tracker.init(color_cp, bound_box)

    # # close window
    # windows.destroyAll()
    # time.sleep(2)

    # # if never select DFU region, then close program
    # if bound_box is None:
    #     exit(0)

    # # start segmentation pipeline
    # segmentation_pipeline()

    # # update masks for reconstruction
    # update_reconstruction_masks(camera_resolution)

    depth_scale = reconstruction_pipeline({})

    perimeter, surface, volume = measurement_pipeline(depth_scale)
    report_pipeline(patient, perimeter, surface, volume)
