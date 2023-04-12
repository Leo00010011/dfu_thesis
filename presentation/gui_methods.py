import numpy as np
from images.masking import save_crop
from images.utils.names_generator import numeric_names
from input.realsense_reader import RSReader, RSPlayback
from typing import Union

def get_segmented_and_preprocessed_images_from_playback(reader : RSPlayback,preprocesor,tracker,windows) -> bool:
    names = numeric_names()
    bound_box = None
    for (color, depth) in reader.get_frames():
        # preprocess each frame
        color, depth = preprocesor(color, depth)
        color_cp = np.copy(color)

        # update bounding box of tracker
        if bound_box is not None:
            coords = tracker.update(color_cp)
            windows.draw_rectangle(color_cp, coords)
            # save images
            save_crop(color, depth, coords, next(names))

        # show window with frame
        windows.show_window('DFU Camera', color_cp)

        # wait for interaction
        key = windows.waitKey()
        # if interaction is q or ESC then stop recording
        if key == ord('q') or key == 27:
            reader.stop_camera()
            break
        # if interaction is s then select DFU region
        elif key == ord("s"):
            reader.playback.pause()
            bound_box = windows.select_region("DFU Camera", color_cp)
            # init tracker
            tracker.init(color_cp, bound_box)
            reader.playback.resume()
    
    return bound_box is None
        
    

def get_segmented_and_preprocessed_images_from_stream(reader :RSReader,preprocesor,tracker,windows) -> bool:
    names = numeric_names()

    bound_box = None
    for (color, depth) in reader.get_frames():
        # preprocess each frame
        color, depth = preprocesor(color, depth)
        color_cp = np.copy(color)

        # update bounding box of tracker
        if bound_box is not None:
            coords = tracker.update(color_cp)
            windows.draw_rectangle(color_cp, coords)
            # save images
            save_crop(color, depth, coords, next(names))

        # show window with frame
        windows.show_window('DFU Camera', color_cp)

        # wait for interaction
        key = windows.waitKey()
        # if interaction is q or ESC then stop recording
        if key == ord('q') or key == 27:
            reader.stop_camera()
            break
        # if interaction is s then select DFU region
        elif key == ord("s"):
            bound_box = windows.select_region("DFU Camera", color_cp)
            # init tracker
            tracker.init(color_cp, bound_box)

    return bound_box is None