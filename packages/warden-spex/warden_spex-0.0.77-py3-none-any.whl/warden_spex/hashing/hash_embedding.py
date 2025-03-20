from hashlib import sha256
from itertools import combinations

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import euclidean


def spex_lsh_m(A: NDArray[np.float64], V: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Implementation of the SPEX-LSH-M algorithm. Given an array A and a set of vantage points V,
    returns a set of hashes that represent A based on its distance ranking relative to the vantage points.
    """

    # Compute the set of distances D
    D = [euclidean(A, v) for v in V]

    # Generate index pairs (j, k) for unique combinations where j < k
    I = list(combinations(range(len(D)), 2))  # noqa: E741

    # Compute comparisons of all possible inequalities
    C = np.array([(2 * i + (D[j] < D[k])) % 2**63 for i, (j, k) in enumerate(I)], dtype=np.int64)

    # Hash comparisons
    H = [int.from_bytes(sha256(c.tobytes()).digest()[:16], byteorder="big", signed=True) for c in C]
    return np.array(H)


def jaccard_index(X: NDArray[np.float64], Y: NDArray[np.float64]) -> np.float64:
    set_X = set(X)
    set_Y = set(Y)

    intersection = len(set_X & set_Y)
    union = len(set_X | set_Y)

    return np.float64(intersection / union if union != 0 else 0)
