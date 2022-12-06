from math import sqrt

import numpy as np


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

