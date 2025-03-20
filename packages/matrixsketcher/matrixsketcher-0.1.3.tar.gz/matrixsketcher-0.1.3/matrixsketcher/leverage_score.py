# matrixsketcher/leverage_score.py


import numpy as np
from numpy.random import default_rng
from scipy.linalg import svd
from scipy.sparse import isspmatrix
from scipy.sparse.linalg import svds
from ._utils import _validate_rank


def leverage_score_sampling(X, sample_size, rank=None, random_state=None, 
                            scale=True, sampling="leverage", axis=0):
    """
    Perform leverage score sampling on either rows or columns.

    Parameters:
    - X (array or sparse matrix): Input data matrix (n x p)
    - sample_size (int): Number of rows or columns to sample (depends on axis)
    - rank (int, optional): Rank for SVD (only used if sampling="leverage", defaults to min(n, p) - 1)
    - random_state (int, optional): Seed for reproducibility
    - scale (bool, optional): Whether to scale selected rows/columns by sqrt(1/prob)
    - sampling (str): "leverage", "uniform", or "weighted" (weighted/uniform only for rows)
    - axis (int): 0 for row sampling (default), 1 for column sampling

    Returns:
    - Sampled subset of X with selected rows or columns.
    """

    rng = default_rng(random_state)
    n, p = X.shape

    if axis not in {0, 1}:
        raise ValueError("axis must be 0 (rows) or 1 (columns)")
    
    if axis == 1 and sampling in {"uniform", "weighted"}:
        raise ValueError("Uniform and weighted sampling are only supported for rows.")

    dim = n if axis == 0 else p  # Number of rows if axis=0, columns if axis=1
    if sample_size > dim:
        raise ValueError(f"sample_size {sample_size} exceeds dimension size {dim}")

    if sampling not in {"uniform", "leverage", "weighted"}:
        raise ValueError('sampling must be "leverage", "uniform", or "weighted"')

    if sampling == "leverage":
        # Ensure rank is at most min(n, p) - 1
        max_rank = min(n, p) - 1
        rank = _validate_rank(rank, max_rank, "leverage_score_sampling") if rank is not None else max_rank

        # Compute SVD
        if axis == 0:  # Row sampling (use U)
            U, s, _ = svds(X, k=rank) if isspmatrix(X) else svds(X, k=rank)
            U = U[:, np.argsort(s)[::-1]]  # Sort by singular values
            leverage_scores = np.sum(U**2, axis=1)
        else:  # Column sampling (use V)
            _, s, Vt = svds(X, k=rank) if isspmatrix(X) else svds(X, k=rank)
            V = Vt[np.argsort(s)[::-1], :].T  # Sort and transpose
            leverage_scores = np.sum(V**2, axis=1)

        leverage_probs = leverage_scores / np.sum(leverage_scores)
        selected_indices = rng.choice(dim, size=sample_size, replace=False, p=leverage_probs)

    elif sampling == "weighted":  # Only applies to row sampling
        row_norms = np.array(X.power(2).sum(axis=1)).ravel() if isspmatrix(X) else np.sum(X**2, axis=1)
        weighted_probs = row_norms / np.sum(row_norms)
        selected_indices = rng.choice(n, size=sample_size, replace=False, p=weighted_probs)

    else:  # Uniform sampling (only for rows)
        selected_indices = rng.choice(n, size=sample_size, replace=False)

    # Scale selected rows/columns if requested
    if scale:
        scaled_rows_or_cols = []
        for idx in selected_indices:
            vec = X[idx].toarray().ravel() if isspmatrix(X) else X[idx] if axis == 0 else X[:, idx]
            prob = (
                leverage_probs[idx] if sampling == "leverage"
                else weighted_probs[idx] if sampling == "weighted"
                else 1
            )
            scaled_rows_or_cols.append(vec / np.sqrt(prob))

        return np.vstack(scaled_rows_or_cols) if axis == 0 else np.column_stack(scaled_rows_or_cols)

    return X[selected_indices, :] if axis == 0 else X[:, selected_indices]
