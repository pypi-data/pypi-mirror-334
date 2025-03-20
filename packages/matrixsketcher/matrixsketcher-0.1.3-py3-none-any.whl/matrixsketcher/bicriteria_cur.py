# matrixsketcher/bicriteria_cur.py


import numpy as np
from numpy.random import default_rng
from numpy.linalg import pinv, slogdet
from scipy.sparse.linalg import svds
from scipy.sparse import isspmatrix


def bicriteria_cur(
    X,
    d_rows,
    d_cols,
    rank=None,
    random_state=None,
    regularization=0.0,
    max_iter=6
):
    """
    Greedy Bicriteria CUR: Joint optimization of row and column selection.
    Based on volume maximization (Boutsidis et al., 2014).

    1) Initialize row/column sets using leverage scores.
    2) Iteratively swap out rows/columns if they increase the submatrix volume det(W^T W).
    3) Return the CUR components (C, W, R).

    Parameters:
    - X (array or sparse matrix): Input data matrix (n x p)
    - d_rows (int): Number of rows to select
    - d_cols (int): Number of columns to select
    - rank (int, optional): Rank for partial SVD-based leverage scores
    - random_state (int, optional): Seed for reproducibility
    - regularization (float, optional): Diagonal regularizer for stable volume computations
    - max_iter (int, optional): Maximum number of refinement iterations

    Returns:
    - C (array): Selected columns (shape: n x d_cols)
    - W (array): Intersection submatrix (d_rows x d_cols)
    - R (array): Selected rows (d_rows x p)
    """
    rng = default_rng(random_state)
    n, p = X.shape

    # Validate user inputs
    if d_rows > n or d_cols > p:
        raise ValueError("Sample size exceeds matrix dimensions.")
    if rank is None:
        rank = min(n, p) - 1
    rank = max(1, min(rank, min(n, p) - 1))  # ensure rank is within [1, min(n,p)-1]

    # Handle dense vs. sparse SVD
    if isspmatrix(X):
        U, s, Vt = svds(X, k=rank)
    else:
        U, s, Vt = svds(X, k=rank)

    # Compute leverage-score based probabilities
    row_scores = np.sum(U**2, axis=1)
    row_probs = row_scores / np.sum(row_scores)

    col_scores = np.sum(Vt**2, axis=0)
    col_probs = col_scores / np.sum(col_scores)

    # ---- STEP 1: Initialize row & column sets using leverage scores ----
    selected_rows = rng.choice(n, size=d_rows, replace=False, p=row_probs)
    selected_cols = rng.choice(p, size=d_cols, replace=False, p=col_probs)

    # Helper function: compute "volume" = log(det(W^T W + regI))
    # Using log(det(.)) is more stable numerically.
    def volume_of_subset(rowset, colset):
        W_sub = X[np.ix_(rowset, colset)]
        # Compute W^T W with regularization
        Gram = W_sub.T @ W_sub + regularization * np.eye(W_sub.shape[1])
        sign, logdet_val = slogdet(Gram)
        # If sign < 0, volume is effectively 0 or negative => Return -inf to discourage it
        return -np.inf if sign <= 0 else logdet_val

    # ---- STEP 2: Iterative refinement to improve volume ----
    def try_improve_rows(rowset, colset):
        improved = False
        current_vol = volume_of_subset(rowset, colset)
        # We'll do a simple pass over all possible swaps
        for _ in range(len(rowset)):  # limit swaps per iteration
            # pick a row inside the set and one outside
            row_in = rng.choice(rowset)
            candidates = np.setdiff1d(np.arange(n), rowset)
            if candidates.size == 0:
                break
            row_out = rng.choice(candidates)
            # swap
            trial_set = np.copy(rowset)
            idx = np.where(trial_set == row_in)[0][0]
            trial_set[idx] = row_out
            vol_new = volume_of_subset(trial_set, colset)
            if vol_new > current_vol:
                current_vol = vol_new
                rowset = trial_set
                improved = True
        return rowset, improved

    def try_improve_cols(rowset, colset):
        improved = False
        current_vol = volume_of_subset(rowset, colset)
        for _ in range(len(colset)):
            col_in = rng.choice(colset)
            candidates = np.setdiff1d(np.arange(p), colset)
            if candidates.size == 0:
                break
            col_out = rng.choice(candidates)
            # swap
            trial_set = np.copy(colset)
            idx = np.where(trial_set == col_in)[0][0]
            trial_set[idx] = col_out
            vol_new = volume_of_subset(rowset, trial_set)
            if vol_new > current_vol:
                current_vol = vol_new
                colset = trial_set
                improved = True
        return colset, improved

    for _ in range(max_iter):
        row_before = np.copy(selected_rows)
        col_before = np.copy(selected_cols)

        # Try improving rows
        selected_rows, row_improved = try_improve_rows(selected_rows, selected_cols)
        # Try improving cols
        selected_cols, col_improved = try_improve_cols(selected_rows, selected_cols)

        # If no improvement in this iteration, stop
        if not (row_improved or col_improved):
            break

    # ---- STEP 3: Build final C, W, R ----
    C = X[:, selected_cols]              # shape: (n, d_cols)
    R = X[selected_rows, :]             # shape: (d_rows, p)
    W = X[np.ix_(selected_rows, selected_cols)]  # shape: (d_rows, d_cols)

    return C, W, R
