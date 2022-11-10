# import pyrealsense2 as rs
from pyrealsense2 import pyrealsense2 as rs


def hole_filling_filter(depth_frame):
    """
    Hole Filling (https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md#holes-filling-filter) filter offers additional layer of depth exterpolation:
    """
    hole_filling = rs.hole_filling_filter()
    filled_depth = hole_filling.process(depth_frame)
    return filled_depth
