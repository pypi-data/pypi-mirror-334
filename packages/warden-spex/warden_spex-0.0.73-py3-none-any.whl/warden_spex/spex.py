import base64
from collections.abc import Iterable
from hashlib import sha256

import numpy as np
from rbloom import Bloom  # pylint: disable=no-name-in-module

from warden_spex.models import SolverProof


class InvalidValueException(Exception): ...


def simple_hash_array(array: np.ndarray, decimals: int = 4) -> int:
    """
    Given a NumPy array as input and a number of significant decimals
    to consider, return an hash of it, representing the item to be
    inserted in the Bloom fikter.
    """

    assert isinstance(array, np.ndarray)

    # We encode floats to ints, retaining a fixed number of decimals.
    # Differences caused by different digits at a higher decimal position are ignored.
    # https://dassencio.org/98
    # https://stackoverflow.com/questions/14943817/does-stdhash-guarantee-equal-hashes-for-equal-floating-point-numbers
    #
    # Absolute to be able to cast to uint64 later
    array = np.abs(array) * (10**decimals)

    # Ensure the array is formatted in memory consistently with fixed type.
    # Array with little-endian unsigned integers of 8 bytes each.
    array = np.ascontiguousarray(array.astype("<u8"))

    # determine hash as bytes.
    hash_bytes = sha256(array.tobytes()).digest()

    # Return hash as int in the range expected by rbloom.
    # https://github.com/KenanHanke/rbloom?tab=readme-ov-file#documentation
    return int.from_bytes(hash_bytes[:16], "big") - 2**127


class Blossom:
    """
    Bloom filter with additional capabilities used by SPEX.
    """

    def __init__(
        self,
        expected_items: int = 1000,
        false_positive_rate: float = 0.01,
    ):
        """
        Create a Bloom filter with a certain number of expected items inserted, and
        an acceptable false positive rate.
        """

        self.inserted_items = 0
        self.expected_items = expected_items

        self.bloom = Bloom(
            expected_items=expected_items,
            false_positive_rate=false_positive_rate,
            hash_func=simple_hash_array,
        )

    def dump(self) -> bytes:
        """
        Serialize Bloom filter to a Base64 sequence of bytes.
        """
        return base64.b64encode(self.bloom.save_bytes())

    def is_hit(self, array: np.ndarray) -> bool:
        """
        Return True if the input `array` is a hit in the Bloom filter.
        """
        return array in self.bloom

    def add(self, array: np.ndarray):
        """
        Add `array` to the Bloom filter.
        """
        if self.inserted_items + 1 > self.expected_items:
            raise InvalidValueException("Bloom filter is full, increase `expected_items`")
        self.inserted_items += 1
        self.bloom.add(array)

    def add_items(self, items: Iterable):
        """
        Add `items` to the Bloom filter.
        """

        for item in items:
            self.add(item)

    @classmethod
    def load(cls, proof: SolverProof):
        """
        Load `proof` Bloom filter.
        """
        blossom = cls()
        blossom.bloom = Bloom.load_bytes(base64.b64decode(proof.bloomFilter), hash_func=simple_hash_array)
        return blossom

    def estimate_false_positive_rate(self):
        """
        Estimate the false positive rate of the current Bloom filter.
        """
        hits = 0
        n = 100000

        for _ in range(n):
            hits += np.random.rand(1) in self.bloom

        estimated = hits / n
        return estimated

    def verify_false_positive_rate(self, expected_rate=0.01, tolerance=0.01):
        """
        Decide if the estimated false positive rate is consistent with the expected value.
        """
        estimated = self.estimate_false_positive_rate()
        print(f"[debug] estimated={estimated} expected={expected_rate} tolerance={tolerance}")
        return expected_rate + tolerance >= estimated

    def make_proof(self):
        return SolverProof(countItems=self.inserted_items, bloomFilter=self.dump())
