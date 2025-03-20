from hashlib import sha256

import numpy as np


def first_significant_digit_position(a: np.ndarray) -> np.ndarray:
    """
    Computes the position of the first significant digit for each element in the array.
    """
    a = np.abs(a.astype(np.float64))  # Ensure float and use absolute values
    a[a == 0] = np.nan  # Avoid log10 issues with zero
    d = np.floor(np.log10(a))
    return np.abs(np.nan_to_num(d).astype(np.int64))


def custom_arange(a: float, b: float, step: float = 1) -> np.ndarray:
    """
    Generates an array from a to b (inclusive) with a given step size.
    """
    if a > b:
        a, b = b, a  # Swap values if needed
    return np.arange(a, b + step, step)  # Ensure upper bound inclusion


def hash_array(a: np.ndarray, epsilon: float = 0.0001, base: int = 1000) -> list:
    """
    Discretizes the input array within an epsilon range and hashes it to a 128-bit integer.
    Ensures numerical stability by scaling, flooring, and applying modulo within 64-bit limits.
    """
    # Determine the position of the first significant digit in epsilon
    n = first_significant_digit_position(np.array([epsilon]))

    # Compute lower and upper bounds
    a_bounds = np.column_stack((a - epsilon, a + epsilon)).flatten()

    # Discretize the bounds by scaling and flooring
    a_quant = np.floor(a_bounds * 10**n)

    # Generate integer ranges for each bound pair.
    # The `base` component helps ensure unique hash insertions in a Bloom filter
    # for duplicate values in the array. If not using a Bloom filter,
    # the term (i * base / 2) can be omitted.
    a_ranges = [i * base / 2 + custom_arange(a_quant[i], a_quant[i + 1]) for i in range(0, len(a_quant), 2)]

    # Apply modulo to ensure values remain within 64-bit integer limits
    a_mods = [(a_range % 2**63).astype(np.int64) for a_range in a_ranges]

    # Flatten the ranges and convert to contiguous unsigned 64-bit array
    a_mems = [np.ascontiguousarray(a_mod.astype("<u8")) for a_mod in a_mods]

    # Compute SHA-256 hashes and extract 128-bit integers
    h = [
        {
            int.from_bytes(sha256(a_mem[i].tobytes()).digest()[:16], byteorder="big", signed=True)
            for i in range(len(a_mem))
        }
        for a_mem in a_mems
    ]

    return h


def check_validity(h1: list, h2: list) -> bool:
    """
    Checks whether there is at least one common hash value between corresponding sets in h1 and h2.
    """
    assert len(h1) == len(h2), "Hash lists must have the same length."
    return all(bool(h1[i] & h2[i]) for i in range(len(h1)))
