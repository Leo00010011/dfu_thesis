import numpy as np
import open3d as o3d
from scipy.spatial import ConvexHull
from sklearn.metrics.pairwise import euclidean_distances

from measurement.utils.heron import heron


def perimeter(ulcer_pcd):
    """
    Se calcula el perimetro como la suma de las distancia Euclideana de los puntos de la frontera de la ulcera.
    Para ello se calculan los puntos que pertenecen a la envoltura convexa de la nube de puntos y se calcula la distancia entre ellos.
    Fuente: Wound 3D Geometrical Feature Estimation Using Poisson Reconstruction
    """
    ulcer_2d = np.asarray(ulcer_pcd.points)[:, :2]
    convex_hull = ConvexHull(ulcer_2d)
    p = 0
    for edge in convex_hull.simplices:
        p += euclidean_distances([ulcer_2d[edge[0]]],
                                 [ulcer_2d[edge[1]]])[0][0]
    return p


def surface(ulcer_mesh):
    triangles = np.asarray(ulcer_mesh.triangles)
    points = np.asarray(ulcer_mesh.vertices)
    s = 0
    for t in triangles:
        pts = points[t]
        s += heron(pts)
    return s


def volume(ulcer_pcd):
    return 0


def pipeline(depth_unit_value):
    DEPTH_UNIT = 1/depth_unit_value

    mesh = o3d.io.read_triangle_mesh(
        './output/reconstruction/scene/integrated.ply')
    mesh.compute_vertex_normals()

    pcd = o3d.geometry.PointCloud()
    pcd.points = mesh.vertices
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=30))
    pcd.orient_normals_consistent_tangent_plane(100)

    p = perimeter(pcd)/DEPTH_UNIT
    print('p', p)
    s = surface(mesh)/DEPTH_UNIT**2
    print('s', s)
    v = volume(pcd)
    return p, s, v
