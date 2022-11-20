import numpy as np
import open3d as o3d
from sklearn.metrics.pairwise import euclidean_distances
from measurement.utils.heron import heron


def perimeter(ulcer_pcd):
    """
    Se calcula el perimetro como la suma de las distancia Euclideana de los puntos de la frontera de la ulcera.
    Para ello se calculan los puntos que pertenecen a la envoltura convexa de la nube de puntos y se calcula la distancia entre ellos.
    Fuente: Wound 3D Geometrical Feature Estimation Using Poisson Reconstruction
    """
    convex_hull = ulcer_pcd.select_by_index(
        ulcer_pcd.compute_convex_hull()[1]).points
    points_boundary = np.asarray(convex_hull)

    distances = euclidean_distances(points_boundary, points_boundary)
    p = distances[0][-1]
    for i in range(0, distances.shape[0] - 1):
        p += distances[i][i+1]

    return p


def surface(ulcer_pcd, ulcer_mesh):
    triangles = np.asarray(ulcer_mesh.triangles)
    points = np.asarray(ulcer_pcd.points)
    s = 0
    for t in triangles:
        pts = points[t]
        s += heron(pts)
    return s
