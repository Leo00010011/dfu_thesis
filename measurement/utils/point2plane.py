def get_plane(x: np.array, y: np.array, z: np.array):
    xy = y - x
    xz = z - x
    n = np.cross(xy, xz)
    d = np.dot(x, n)
    return np.concatenate((n, [-d]))

def pP_distance(p0: np.array, x: np.array, y: np.array, z: np.array):
    plane = get_plane(x, y, z)
    num = abs(np.dot(np.concatenate((p0, [1])), plane))
    den = sqrt(np.sum(plane[:3] ** 2))
    return num / den