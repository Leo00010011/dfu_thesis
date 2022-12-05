from math import sqrt

import numpy as np
import open3d as o3d
import scipy as sc
from scipy.spatial import ConvexHull


def get_plane(x, y, z):
    xy = y - x
    xz = z - x
    n = np.cross(xy, xz)
    d = np.dot(x, n)
    return np.concatenate((n, [-d]))


def pP_distance(p0, x, y, z):
    plane = get_plane(x, y, z)
    num = abs(np.dot(np.concatenate((p0, [1])), plane))
    den = sqrt(np.sum(plane[:3] ** 2))
    return num / den


def get_top(ulcer_pts):
    # obtengo los puntos del borde de la ulcera
    #points_boundary = np.asarray(pcd.select_by_index(ulcer_pts.compute_convex_hull()[1]).points)
    ulcer2d = np.asarray(ulcer_pts.points)[:, :2]
    ch = ConvexHull(ulcer2d)
    points_boundary = np.asarray(pcd.points)[ch.vertices]
    # inicializo un interpolador
    interpolate = sc.interpolate.CloughTocher2DInterpolator(
        points_boundary[:, :2], points_boundary[:, -1])
    #interpolate = sc.interpolate.LinearNDInterpolator(points_boundary[:,:2], points_boundary[:,-1])
    # calculo los maximos y los minimos de los puntos del borde para generar la tapa
    mins = np.min(points_boundary[:, :2], axis=0)
    maxs = np.max(points_boundary[:, :2], axis=0)
    x = np.linspace(mins[0], maxs[0], 100)
    y = np.linspace(mins[1], maxs[1], 100)
    x, y = np.meshgrid(x, y)
    points = np.dstack((x, y))
    # genero los puntos de la tapa usando la interpolacion
    points_3d = []
    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            points_3d.append([points[i][j][0], points[i][j]
                              [1], interpolate(points[i][j])[0]])
    points_3d = np.array(points_3d)
    points_3d = points_3d[~np.isnan(points_3d[:, -1])]
    top = o3d.geometry.PointCloud()
    top.points = o3d.utility.Vector3dVector(points_3d)
    return top
