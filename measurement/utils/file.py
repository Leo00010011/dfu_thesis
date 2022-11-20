import open3d as o3d

PLY_PATH = 'output/reconstruction/scene/integrated.ply'


def open_point_cloud():
    return o3d.io.read_point_cloud(PLY_PATH)


def open_triangle_mesh():
    return o3d.io.read_triangle_mesh(PLY_PATH)
