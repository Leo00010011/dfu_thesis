# import pyrealsense2 as rs
from pyrealsense2 import pyrealsense2 as rs


def decimation_filter(depth_frame):
    """
    When using Depth-from-Stereo solution, z-accuracy is related to original spacial resolution.

If you are satisfied with lower spatial resolution, the Decimation Filter (https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md#decimation-filter) will reduce spatial resolution preserving z-accuracy and performing some rudamentary hole-filling.
    """

    decimation = rs.decimation_filter()
    decimated_depth = decimation.process(depth_frame)
    return decimated_depth
