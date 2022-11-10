# import pyrealsense2 as rs
from pyrealsense2 import pyrealsense2 as rs


def temporal_filter(depth_frame):
    """
    Our implementation of Temporal Filter (https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md#temporal-filter) does basic temporal smoothing and hole-filling. It is meaningless when applied to a single frame, so let's capture several consecutive frames:
    """

    temporal = rs.temporal_filter()
    temp_filtered = temporal.process(depth_frame)
    return temp_filtered
