from os import remove
from glob import glob

def clear_output_pipeline():
    # clear segmentation
    remove_files(glob("output/segmentation/*.*"))
    # clear masks
    remove_files(glob("output/masks/*.*"))
    # clear reconstruction
    remove_files(glob("output/reconstruction/*.*"))
    remove_files(glob("output/reconstruction/color/*.*"))
    remove_files(glob("output/reconstruction/color_masked/*.*"))
    remove_files(glob("output/reconstruction/depth/*.*"))
    remove_files(glob("output/reconstruction/fragments/*.*"))
    remove_files(glob("output/reconstruction/scene/*.*"))

def remove_files(files):
    for path in files:
        remove(path)