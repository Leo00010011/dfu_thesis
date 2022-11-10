# import cv2
import numpy as np


def image_agcwd(img, a=0.25, truncated_cdf=False):
    hist, _ = np.histogram(img.flatten(), 256, [0, 256])
    prob_normalized = hist / hist.sum()

    unique_intensity = np.unique(img)
    prob_min = prob_normalized.min()
    prob_max = prob_normalized.max()

    pn_temp = (prob_normalized - prob_min) / (prob_max - prob_min)
    pn_temp[pn_temp > 0] = prob_max * (pn_temp[pn_temp > 0]**a)
    pn_temp[pn_temp < 0] = prob_max * (-((-pn_temp[pn_temp < 0])**a))
    prob_normalized_wd = pn_temp / pn_temp.sum()  # normalize to [0,1]
    cdf_prob_normalized_wd = prob_normalized_wd.cumsum()

    if truncated_cdf:
        inverse_cdf = np.maximum(0.5, 1 - cdf_prob_normalized_wd)
    else:
        inverse_cdf = 1 - cdf_prob_normalized_wd

    img_new = img.copy()
    for i in unique_intensity:
        img_new[img == i] = np.round(255 * (i / 255)**inverse_cdf[i])

    return img_new
