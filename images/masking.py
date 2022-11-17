import cv2
import numpy as np

FIXED = 20


def mask_rectangle(image, coords):
    [x, y, w, h] = coords
    mask = np.zeros(image.shape)
    mask[max(y-FIXED, 0):y+h+FIXED, max(x-FIXED, 0):x+w+FIXED, ] = 1
    masked = mask*image
    return masked.astype(image.dtype)


def crop_rectangular(image, coords):
    [x, y, w, h] = coords
    return image[max(y-FIXED, 0):y+h+FIXED, max(x-FIXED, 0):x+w+FIXED]


def mask_and_crop(image, coords):
    return mask_rectangle(image, coords), crop_rectangular(image, coords)


def save_mask_and_crop(color, depth, coords, name):
    color_masked, color_cropped = mask_and_crop(color, coords)
    depth_masked = mask_rectangle(depth, coords)
    cv2.imwrite(f'output/segmentation/{name}.jpg',
                cv2.cvtColor(color_cropped, cv2.COLOR_RGB2BGR))
    cv2.imwrite(f'output/reconstruction/color/{name}.jpg',
                cv2.cvtColor(color_masked, cv2.COLOR_RGB2BGR))
    cv2.imwrite(f'output/reconstruction/depth/{name}.png', depth_masked)
