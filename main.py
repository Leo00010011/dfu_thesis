from report.pipeline import pipeline as report_pipeline
from reconstruction.pipeline import pipeline as reconstruction_pipeline
from measurement.pipeline import pipeline as measurement_pipeline
from segmentation.predictor import predict as segmentation_pipeline
from images.masking import save_crop, update_reconstruction_masks
from processing.pipeline import pipeline as processing_pipeline
from images.utils.names_generator import numeric_names
from output.pipeline import clear_output_pipeline
from input.realsense_reader import RSReader, RSPlayback
from tracking import pipeline as tracker
from data.pipeline import data_pipeline
import presentation.windows as windows
from presentation.gui_methods import get_segmented_and_preprocessed_images_from_playback, get_segmented_and_preprocessed_images_from_stream
import numpy as np
import time
import open3d as o3d
import json

import os
import datetime
# ignore TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)


if __name__ == "__main__":
    # clear output of previous execution
    clear_output_pipeline()
    # read data pipeline
    patient = data_pipeline()

    start_time = time.time()
    # initialize the camera reader
    reader = RSReader()
    # start recording with camera
    reader.start_camera()
    # save in json file the intrinsic matrix of the camera
    reader.save_intrinsic()

    ##ARCHIVOS GUARDADOS HASTA AQUI
    # output/reconstruction/intrinsic.json

    # # # # save the resolution of the camera
    camera_resolution = reader.get_resolution()

    # read frames
    has_images = get_segmented_and_preprocessed_images_from_stream(reader,processing_pipeline,tracker,windows)

    # close window
    windows.destroyAll()
    time.sleep(2)

    # if never select DFU region, then close program
    if has_images:
        exit(0)

    ##ARCHIVOS GUARDADOS HASTA AQUI
    ## output/segmentation/  .jpg   ~ lo que está dentro del rectángulo
    ## output/segmentation/  .json  ~ coordenadas del rectángulo
    ## output/reconstruction/color/ .jpg ~ la imagen completa
    ## output/reconstruction/depth/ .jpg ~ la profundidad

    # start segmentation pipeline
    segmentation_pipeline()

    ## ARCHIVOS GUARDADOS HASTA AQUI
    ## Se cogen las imagenes de output/segmentation
    ## Los pesos se sacan de metadata/weights/linknet
    ## Las segmentaciones se salvan en output/masks/
    

    # # update masks for reconstruction
    update_reconstruction_masks(camera_resolution)

    # ARCHIVOS GUARDADOS HASTA AQUI
    # Se cargan los output/segmentation/*.json
    # Se cargan los output/masks/*.json
    # Se cargan los mask output/reconstruction/color/*.jpg
    # output/reconstruction/color_masked/ ~ Aplicar la mascara a las imagenes a color

    depth_scale = reconstruction_pipeline({})

    with open('output/reconstruction/intrinsic.json') as intr_file:
        intr = json.load(intr_file)
    depth_scale = intr["depth_scale"]

    perimeter, surface, volume = measurement_pipeline(depth_scale)
    end_time = time.time() - start_time

    report_pipeline(patient, perimeter, surface, volume)
