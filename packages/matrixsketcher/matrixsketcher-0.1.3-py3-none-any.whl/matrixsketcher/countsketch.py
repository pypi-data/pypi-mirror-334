# matrixsketcher/countsketch.py


import numpy as np
from numpy.random import default_rng
from scipy.sparse import isspmatrix, coo_matrix


def countsketch(X, sketch_size, random_state=None, sparse_output=True):
    """
    CountSketch feature hashing.
    ...
    """
    rng = default_rng(random_state)
    n, p = X.shape

    hashes = rng.integers(0, sketch_size, p)
    signs = rng.choice([-1, 1], p)

    if sparse_output:
        S = coo_matrix((signs, (hashes, np.arange(p))), shape=(sketch_size, p)).tocsr()
    else:
        S = np.zeros((sketch_size, p))
        for j in range(p):
            S[hashes[j], j] = signs[j]

    return X.dot(S.T) if isspmatrix(X) else X @ S.T
