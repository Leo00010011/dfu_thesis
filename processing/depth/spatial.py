# import pyrealsense2 as rs
from pyrealsense2 import pyrealsense2 as rs


def spatial_filter(depth_frame):
    """
    Spatial Filter (https://github.com/IntelRealSense/librealsense/blob/master/doc/post-processing-filters.md#spatial-edge-preserving-filter) is a fast implementation of Domain-Transform Edge Preserving Smoothing (http://inf.ufrgs.br/~eslgastal/DomainTransform/)
    """

    spatial = rs.spatial_filter()
    filtered_depth = spatial.process(depth_frame)
    return filtered_depth
