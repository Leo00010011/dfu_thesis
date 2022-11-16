# import pyrealsense2 as rs
from pyrealsense2 import pyrealsense2 as rs
from processing.depth.decimation import decimation_filter
from processing.depth.spatial import spatial_filter
from processing.depth.temporal import temporal_filter
from processing.depth.hole_filling import hole_filling_filter


def pipeline(depth_frame):
    return depth_frame
    """
    These filters work best when applied sequentially one after another. At longer range, it also helps using `disparity_transform` to switch from depth representation to disparity form:
    """
    depth_to_disparity = rs.disparity_transform(True)
    disparity_to_depth = rs.disparity_transform(False)

    depth_frame = decimation_filter(depth_frame)
    depth_frame = depth_to_disparity.process(depth_frame)
    depth_frame = spatial_filter(depth_frame)
    depth_frame = temporal_filter(depth_frame)
    depth_frame = disparity_to_depth.process(depth_frame)
    depth_frame = hole_filling_filter(depth_frame)

    return depth_frame
