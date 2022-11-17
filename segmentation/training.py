import matplotlib.pyplot as plt
import segmentation_models as sm
import tensorflow as tf
from glob import glob
import skimage
import numpy as np
import pandas as pd
import cv2
import tqdm
import os
from scipy.ndimage.morphology import binary_fill_holes
from skimage.morphology import remove_small_objects
from skimage.io import imsave, imread
os.environ['SM_FRAMEWORK'] = 'tf.keras'


def gpu_setting(opts):
    print("Setting up GPUs 🔧")
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print("🔥", len(gpus), "Physical GPUs,",
                  len(logical_gpus), "Logical GPU")
        except RuntimeError as e:
            print(e)
    else:
        print("Unavailable GPUs 💩")
    print("===")


def load_data(opts):
    def get_id_from_file_path(p, separator="-"):
        return separator.join(p.split(os.path.sep)[-1].split(".")[0].split(separator)[1:])

    print("Loading data 🚧")
    paths = glob(opts["test_dir"] + "*" + opts['img_type'])
    if paths:
        id = list(map(get_id_from_file_path, paths))
        datas = pd.DataFrame({"ID": id, "PATH": paths})
        print(f"Data loaded, with: {len(paths)} datapoints 🎉")
        return datas
    else:
        print("No data found 🙈")
    print("===")


def get_image(opts, collection, preprocess_input,  index: int = 0):
    x = cv2.cvtColor(cv2.imread(collection["PATH"][index]), cv2.COLOR_BGR2RGB)

    if x.shape[0] > x.shape[1]:
        x_padded = cv2.copyMakeBorder(
            x, 0, 0, 0, (x.shape[0] - x.shape[1]), cv2.BORDER_CONSTANT, value=0)
    else:
        x_padded = cv2.copyMakeBorder(
            x, 0, (x.shape[1] - x.shape[0]), 0, 0, cv2.BORDER_CONSTANT, value=0)
    resize_target = int(int(x_padded.shape[0] / 32) * 32) + 32
    if resize_target < 96:
        resize_target = 96
    x_padded_unpretrain = np.copy(x_padded)
    if opts['use_pretrained_flag'] == 1:
        x_padded = preprocess_input(x_padded)
    return cv2.resize(x_padded, (resize_target, resize_target)), x.shape, x_padded.shape


def TTA(test_image):
    augmented_images = np.zeros(
        (8, test_image.shape[0], test_image.shape[1], test_image.shape[2]))
    augmented_images[0, :, :, :] = test_image
    augmented_images[1, :, :, :] = cv2.rotate(
        test_image, cv2.ROTATE_90_CLOCKWISE)
    augmented_images[2, :, :, :] = cv2.rotate(
        test_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    augmented_images[3, :, :, :] = cv2.rotate(test_image, cv2.ROTATE_180)
    augmented_images[4, :, :, :] = cv2.flip(test_image, 1)
    augmented_images[5, :, :, :] = cv2.flip(augmented_images[1, :, :, :], 1)
    augmented_images[6, :, :, :] = cv2.flip(augmented_images[3, :, :, :], 1)
    augmented_images[7, :, :, :] = cv2.flip(augmented_images[2, :, :, :], 1)
    return augmented_images


def TTA_reverse(predictions):
    reverse = np.zeros(
        (predictions.shape[0], predictions.shape[1], predictions.shape[2]))

    reverse[0, :, :] = predictions[0, :, :]
    reverse[1, :, :] = cv2.rotate(
        predictions[1, :, :], cv2.ROTATE_90_COUNTERCLOCKWISE)
    reverse[2, :, :] = cv2.rotate(
        predictions[2, :, :], cv2.ROTATE_90_CLOCKWISE)
    reverse[3, :, :] = cv2.rotate(predictions[3, :, :], cv2.ROTATE_180)
    reverse[4, :, :] = cv2.flip(predictions[4, :, :], 1)
    reverse[5, :, :] = cv2.flip(predictions[5, :, :], 1)
    reverse[5, :, :] = cv2.rotate(
        reverse[5, :, :], cv2.ROTATE_90_COUNTERCLOCKWISE)
    reverse[6, :, :] = cv2.flip(predictions[6, :, :], 1)
    reverse[6, :, :] = cv2.rotate(reverse[6, :, :], cv2.ROTATE_180)
    reverse[7, :, :] = cv2.flip(predictions[7, :, :], 1)
    reverse[7, :, :] = cv2.rotate(reverse[7, :, :], cv2.ROTATE_90_CLOCKWISE)
    return reverse
