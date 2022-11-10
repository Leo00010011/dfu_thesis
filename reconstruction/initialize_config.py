from file import check_folder_structure, extract_rgbd_frames
import os
import sys
sys.path.append("../utility")


def set_default_value(config, key, value):
    if key not in config:
        config[key] = value


def initialize_config(config):

    # set default parameters if not specified
    set_default_value(config, "depth_map_type", "redwood")
    set_default_value(config, "n_frames_per_fragment", 100)
    set_default_value(config, "n_keyframes_per_n_frame", 5)
    set_default_value(config, "min_depth", 0.3)
    set_default_value(config, "max_depth", 3.0)
    set_default_value(config, "voxel_size", 0.05)
    set_default_value(config, "max_depth_diff", 0.07)
    set_default_value(config, "depth_scale", 1000)
    set_default_value(config, "preference_loop_closure_odometry", 0.1)
    set_default_value(config, "preference_loop_closure_registration", 5.0)
    set_default_value(config, "tsdf_cubic_size", 3.0)
    set_default_value(config, "icp_method", "color")
    set_default_value(config, "global_registration", "ransac")
    set_default_value(config, "python_multi_threading", True)

    # `slac` and `slac_integrate` related parameters.
    # `voxel_size` and `min_depth` paramters from previous section,
    # are also used in `slac` and `slac_integrate`.
    set_default_value(config, "max_iterations", 5)
    set_default_value(config, "sdf_trunc", 0.04)
    set_default_value(config, "block_count", 40000)
    set_default_value(config, "distance_threshold", 0.07)
    set_default_value(config, "fitness_threshold", 0.3)
    set_default_value(config, "regularizer_weight", 1)
    set_default_value(config, "method", "slac")
    set_default_value(config, "device", "CPU:0")
    set_default_value(config, "save_output_as", "pointcloud")
    set_default_value(config, "folder_slac", "slac/")
    set_default_value(config, "template_optimized_posegraph_slac",
                      "optimized_posegraph_slac.json")

    # path related parameters.
    set_default_value(config, "folder_fragment", "fragments/")
    set_default_value(config, "subfolder_slac",
                      "slac/%0.3f/" % config["voxel_size"])
    set_default_value(config, "template_fragment_posegraph",
                      "fragments/fragment_%03d.json")
    set_default_value(config, "template_fragment_posegraph_optimized",
                      "fragments/fragment_optimized_%03d.json")
    set_default_value(config, "template_fragment_pointcloud",
                      "fragments/fragment_%03d.ply")
    set_default_value(config, "folder_scene", "scene/")
    set_default_value(config, "template_global_posegraph",
                      "scene/global_registration.json")
    set_default_value(config, "template_global_posegraph_optimized",
                      "scene/global_registration_optimized.json")
    set_default_value(config, "template_refined_posegraph",
                      "scene/refined_registration.json")
    set_default_value(config, "template_refined_posegraph_optimized",
                      "scene/refined_registration_optimized.json")
    set_default_value(config, "template_global_mesh", "scene/integrated.ply")
    set_default_value(config, "template_global_traj", "scene/trajectory.log")

    if config["path_dataset"].endswith(".bag"):
        assert os.path.isfile(config["path_dataset"]), (
            f"File {config['path_dataset']} not found.")
        print("Extracting frames from RGBD video file")
        config["path_dataset"], config["path_intrinsic"], config[
            "depth_scale"] = extract_rgbd_frames(config["path_dataset"])
