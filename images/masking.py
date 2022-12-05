import cv2
import numpy as np
import json
from glob import glob

from images.utils.files import open_image


def pad_mask_to_fill_rectangle(mask, coords, size):
    a, b = size
    [x, y, w, h] = coords
    image_pad = np.zeros((a, b, mask.shape[-1]))
    image_pad[y:y+h, x:x+w] = mask
    return image_pad.astype(mask.dtype)


def crop_rectangular(image, coords):
    [x, y, w, h] = coords
    return image[y:y+h, x:x+w]


def apply_mask(image, mask):
    print(image.shape, mask.shape)
    return (image*mask).astype(image.dtype)


def save_crop(color, depth, coords, name):
    color_cropped = crop_rectangular(color, coords)
    cv2.imwrite(f'output/segmentation/{name}.jpg',
                cv2.cvtColor(color_cropped, cv2.COLOR_RGB2BGR))

    with open(f'output/segmentation/{name}.json', 'w') as json_file:
        json_content = json.dumps(coords)
        json_file.write(json_content)

    cv2.imwrite(f'output/reconstruction/color/{name}.jpg',
                cv2.cvtColor(color, cv2.COLOR_RGB2BGR))
    cv2.imwrite(f'output/reconstruction/depth/{name}.png', depth)


def update_reconstruction_masks(size):
    json_paths = sorted(glob('output/segmentation/*.json'))
    masks_paths = sorted(glob('output/masks/*.jpg'))
    color_paths = sorted(glob('output/reconstruction/color/*.jpg'))

    for json_path, mask_path, color_path in zip(json_paths, masks_paths, color_paths):
        with open(json_path, 'r') as json_file:
            cords = json.loads(json_file.read())
            mask = np.array(open_image(mask_path, False))
            color = np.array(open_image(color_path, False))
            mask[mask > 0] = 1
            mask_updated = pad_mask_to_fill_rectangle(mask, cords, size)
            color_masked = apply_mask(color, mask_updated)
            cv2.imwrite(f'output/reconstruction/color_masked/{color_path.split("/")[-1]}',
                        cv2.cvtColor(color_masked, cv2.COLOR_RGB2BGR))
