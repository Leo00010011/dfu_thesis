import os
import cv2
import glob
import numpy as np
import segmentation_models as sm
from images.utils.files import get_image
from segmentation.config import OPTS, PATH
from scipy.ndimage.morphology import binary_fill_holes
from skimage.morphology import remove_small_objects
from images.utils.data_augmentation import TTA, TTA_reverse

sm.set_framework('tf.keras')
sm.framework()


def predict_model(filename: str, model, pretrained: str):
    img, os, ops = get_image(
        filename, preprocess_input=sm.get_preprocessing(OPTS[pretrained]))
    img_aug = TTA(img)
    img_p = model.predict(img_aug, verbose=0, batch_size=4)
    img_p_total = np.mean(TTA_reverse(np.squeeze(img_p), axis=0))
    img_p = cv2.resize(img_p_total, ops[:2][::-1])[0:os[0], 0:os[1]]
    return img_p


def predict():
    linknets = []
    unets = []

    for i in range(5):
        linknets.append(sm.Linknet(
            OPTS['pretrained_model_1'], classes=1, activation='sigmoid', encoder_weights='imagenet'))
        unets.append(sm.Unet(OPTS['pretrained_model_2'], classes=1, activation='sigmoid',
                             encoder_weights='imagenet', decoder_block_type='transpose'))
        linknets[-1].load_weights(OPTS["models_save_path_1"] +
                                  f"linknet_{i+1}.h5")
        unets[-1].load_weights(OPTS["models_save_path_2"] + f"unet_{i+1}.h5")

    images = glob.glob(PATH + "*" + OPTS["img_type"])
    for img_path in images:
        ln = predict_model(img_path, linknets[0], "pretrained_model_1")
        for linknet in linknets[1:]:
            ln += predict_model(img_path, linknet, "pretrained_model_1")

        un = predict_model(img_path, unets[0], "pretrained_model_2")
        for unet in unets[1:]:
            un += predict_model(img_path, unet, "pretrained_model_2")

        average = np.array((ln.astype(float) + un.astype(float))/2)
        average = np.uint(average > .5)
        average = binary_fill_holes(average > 0).astype(float)
        average = remove_small_objects(
            average > .5, min_size=100, connectivity=2)

        cv2.imwrite(OPTS['results_save_path'] +
                    img_path.split("/")[-1], average)
