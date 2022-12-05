import open3d as o3d

PLY_PATH = 'output/reconstruction/scene/integrated.ply'


def open_point_cloud():
    mesh = open_triangle_mesh()
    pcd = o3d.geometry.PointCloud()
    pcd.points = mesh.vertices
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(100)
    return pcd


def open_triangle_mesh():
    mesh = o3d.io.read_triangle_mesh(PLY_PATH)
    mesh.compute_vertex_normals()
    return mesh

