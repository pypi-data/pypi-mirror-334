# matrixsketcher/cur_decomposition.py


import numpy as np
from numpy.random import default_rng
from scipy.linalg import pinv, svd
from scipy.sparse import isspmatrix
from scipy.sparse.linalg import svds
from ._utils import _validate_rank


def cur_decomposition(X, d_rows, d_cols, rank=None, random_state=None, sampling="uniform",
                      regularization=0.0):
    """
    CUR decomposition with leverage-based column selection and configurable row selection.
    
    Parameters:
    - X (array or sparse matrix): Input data matrix (n x k)
    - d_rows (int): Number of rows to select
    - d_cols (int): Number of columns to select
    - rank (int, optional): Rank for leverage score computation (default: min(n, p) - 1)
    - random_state (int, optional): Seed for reproducibility
    - sampling (str): "uniform" (random row selection) or "leverage" (leverage score row selection)
    - regularization (float): Small positive value for numerical stability (default: 0.0)

    Returns:
    - C (array): Selected columns
    - R (array): Selected rows
    - W (array): Intersection matrix
    """
    rng = default_rng(random_state)
    n, p = X.shape

    if d_rows > n or d_cols > p:
        raise ValueError("Sample size cannot exceed matrix dimensions.")

    # Default rank = min(n, p) - 1 for svds() stability
    rank = min(rank or min(n, p) - 1, min(n, p) - 1)

    if sampling not in {"uniform", "leverage"}:
        raise ValueError("sampling must be 'uniform' or 'leverage'")

    # Column selection (always leverage-based)
    if isspmatrix(X):
        _, s, Vt = svds(X, k=rank)
    else:
        _, s, Vt = svd(X, full_matrices=False)
    Vt = Vt[np.argsort(s)[::-1], :]
    col_probs = np.sum(Vt[:rank].T**2, axis=1)
    col_probs /= np.sum(col_probs)
    col_indices = rng.choice(p, d_cols, replace=False, p=col_probs)

    # Row selection (can be leverage-based or uniform)
    if sampling == "leverage":
        if isspmatrix(X):
            U, s, _ = svds(X, k=rank)
        else:
            U, s, _ = svd(X, full_matrices=False)
        U = U[:, np.argsort(s)[::-1]]
        row_probs = np.sum(U**2, axis=1)
        row_probs /= np.sum(row_probs)
        row_indices = rng.choice(n, d_rows, replace=False, p=row_probs)
    else:  # Uniform row selection
        row_indices = rng.choice(n, d_rows, replace=False)

    # Build C, R, W
    if isspmatrix(X):
        C = X[:, col_indices].tocsc()
        R = X[row_indices, :].tocsr()
        W = X[row_indices, :][:, col_indices].toarray()
    else:
        C = X[:, col_indices]
        R = X[row_indices, :]
        W = X[np.ix_(row_indices, col_indices)]

    if regularization > 0:
        W += regularization * np.eye(W.shape[0])

    return C, W, R
