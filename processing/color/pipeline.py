from processing.color.focus import focus
from processing.color.remove_tissue import remove_tissue
from processing.color.contrast.pipeline import pipeline as contrast_pipeline


def pipeline(rgb_img, with_tissue=False):
    rgb_img = focus(rgb_img)
    rgb_img = contrast_pipeline(rgb_img)  # enhance contrast
    return rgb_img if with_tissue else remove_tissue(rgb_img)
