# matrixsketcher/_utils.py


import warnings


def _is_power_of_two(n):
    """Check if n is a power of two (n > 0)."""
    return (n & (n - 1) == 0) and n > 0


def _validate_rank(rank, max_dim, method_name):
    """Warn if rank > max_dim, clamp if needed."""
    if rank > max_dim:
        warnings.warn(
            f"Requested rank {rank} exceeds maximum possible dimension {max_dim} "
            f"in {method_name}. Using rank={max_dim} instead.",
            RuntimeWarning
        )
        return max_dim
    return rank
