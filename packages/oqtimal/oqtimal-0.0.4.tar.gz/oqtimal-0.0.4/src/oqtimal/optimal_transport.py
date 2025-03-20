
from oqtimal.algorithms import sinkhorn_knopp

def optimal_transport(key, x, y, algorithm="simplex", cost="euclidean", **kwargs):
    return sinkhorn_knopp(key, x, y, **kwargs)
