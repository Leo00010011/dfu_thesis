import cv2
import numpy as np
import json
from glob import glob

from images.utils.files import open_image


def mask_rectangle(image, coords, size):
    a, b = size
    [x, y, w, h] = coords
    image_pad = np.zeros((a, b, image.shape[-1]))
    image_pad[y:y+h, x:x+w] = image
    return image_pad.astype(image.dtype)


def crop_rectangular(image, coords):
    [x, y, w, h] = coords
    return image[y:y+h, x:x+w]


def save_crop(color, depth, coords, name):
    color_cropped = crop_rectangular(color, coords)
    depth_cropped = crop_rectangular(depth, coords)
    cv2.imwrite(f'output/segmentation/{name}.jpg',
                cv2.cvtColor(color_cropped, cv2.COLOR_RGB2BGR))

    with open(f'output/segmentation/{name}.json', 'w') as json_file:
        json_content = json.dumps(coords)
        json_file.write(json_content)

    cv2.imwrite(f'output/reconstruction/color/{name}.jpg',
                cv2.cvtColor(color_cropped, cv2.COLOR_RGB2BGR))
    cv2.imwrite(f'output/reconstruction/depth/{name}.png', depth_cropped)


def update_reconstruction_masks(size):
    json_paths = sorted(glob('output/segmentation/*.json'))
    masks_paths = sorted(glob('output/masks/*.jpg'))
    reconstruction_color_masks = sorted(
        glob('output/reconstruction/color/*.jpg'))
    reconstruction_depth_masks = sorted(
        glob('output/reconstruction/depth/*.png'))

    for json_path, mask_path, color_path, depth_path in zip(json_paths, masks_paths, reconstruction_color_masks, reconstruction_depth_masks):
        with open(json_path, 'r') as json_file:
            cords = json.loads(json_file.read())
            mask = np.array(open_image(mask_path, True))
            mask[mask > 0] = 255
            color = np.array(open_image(color_path))
            depth = np.array(open_image(depth_path))
            color_masked = mask_rectangle(cv2.bitwise_and(
                color, color, mask=mask), cords, size)
            depth_masked = mask_rectangle(cv2.bitwise_and(
                depth, depth, mask=mask), cords, size)
            cv2.imwrite(color_path,
                        cv2.cvtColor(color_masked, cv2.COLOR_RGB2BGR))
            cv2.imwrite(depth_path,
                        cv2.cvtColor(depth_masked, cv2.COLOR_RGB2BGR))
