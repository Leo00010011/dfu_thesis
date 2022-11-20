from sklearn.metrics.pairwise import euclidean_distances
from math import sqrt


def heron(p):
    S = euclidean_distances(p, p)
    SP = (S[0][1] + S[0][2] + S[1][2])/2
    return sqrt(SP * (SP - S[0][1]) * (SP - S[0][2]) * (SP - S[1][2]))
