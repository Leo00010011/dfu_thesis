import numpy as np
import scipy as sc
import open3d as o3d
from scipy.spatial import ConvexHull
from sklearn.metrics.pairwise import euclidean_distances

from measurement.utils.heron import heron
from measurement.utils.top_ulcer import get_top
from sklearn.metrics.pairwise import euclidean_distances
from measurement.utils.point2plane import pP_distance as p2p
from measurement.utils.file import open_point_cloud, open_triangle_mesh

DEPTH_UNIT = 0.001


def perimeter(ulcer_pcd):
    ulcer2d = np.asarray(ulcer_pcd.points)[:, :2]
    ch = ConvexHull(ulcer2d)
    p = 0
    for edge in ch.simplices:
        p += euclidean_distances([ulcer2d[edge[0]]], [ulcer2d[edge[1]]])[0][0]
    return p / DEPTH_UNIT


def area(ulcer_mesh):
    triangles = np.asarray(ulcer_mesh.triangles)
    points = np.asarray(ulcer_mesh.vertices)
    area = 0
    for t in triangles:
        pts = points[t]
        area += heron(pts)
    return area / (DEPTH_UNIT ** 2)


def volume(ulcer_pcd):
    points_3d = get_top(ulcer_pcd)
    # luego hago la triangulacion de Delaunay en 3D
    delaunay = sc.spatial.Delaunay(np.concatenate(
        (points_3d.points, np.asarray(ulcer_pts.points))))
    # se calcula el volumen de cada piramide
    volume = 0
    for pyramid in delaunay.simplices:
        pts = delaunay.points[pyramid]
        AB = heron(pts[1:])
        h = pP_distance(pts[0], pts[1], pts[2], pts[3])
        volume += (AB * h) / 3
    return volume / (DEPTH_UNIT ** 3)


def measurement_pipeline(depth_scale_unit):
    mesh = open_triangle_mesh()
    pcd = open_point_cloud()

    return perimeter(pcd), area(mesh), volume(pcd)
