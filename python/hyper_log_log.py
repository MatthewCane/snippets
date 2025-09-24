import hashlib
import math
from hashlib import sha1
from random import choice, randint
from string import ascii_letters
from sys import getsizeof
from typing import TYPE_CHECKING, Callable

from bitarray import bitarray, util

# We can't import this typehint normally so we need to do this weird thing
HASH = hashlib._hashlib.HASH  # ty: ignore[unresolved-attribute]

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer


class HyperLogLog:
    """A pure Python implementation of HyperLogLog"""

    def __init__(
        self,
        hashing_algo: Callable[["ReadableBuffer"], HASH] = sha1,
        register_bits: int = 14,
    ):
        """Initialize the HyperLogLog data structure.

        args:
            hashing_algo: The hashing algorithm to use to calculate cardinality.
            register_bits: The number of bits to use for the registers. This determines the number of registers as 2^register_bits.
        """
        self.algo = hashing_algo
        self.register_bits = register_bits

        # Calculate the number of registers we will need
        self.register_length = 2**register_bits

        # Initialize the registers to zero
        self.registers: list[int] = [0 for _ in range(self.register_length)]

        # We need to know the bit length of the algo later so calculate this now
        self.hash_bit_length = self.algo().digest_size * 8

    def get_bucket_and_cardinality(self, data: str) -> tuple[int, int]:
        """
        Returns a tuple consisting of the bucket and the cardinality of
        the data.

        The cardinailty is the location of the first 1 in hash, excluding
        the bits used to find the registers.
        """
        # 1. Hash the data
        digest = self.algo(data.encode()).digest()
        # 2. Convert the digest to a bitarray
        bits = bitarray(digest)
        # 3. Split the bitarray into the bucket and the suffix
        suffix = bits[self.register_bits :]
        bucket = util.ba2int(bits[: self.register_bits])

        # 4. Set the default to the max cardinalty, which would be the length of
        # the suffix + 1 if the suffix was all zeros
        cardinality = len(suffix) + 1

        for idx, bit in enumerate(suffix):
            if bit == 1:
                cardinality = idx + 1
                break

        return (bucket, cardinality)

    def ingest(self, data: str) -> None:
        """Process data and add the result to the buckets."""
        bucket, cardinality = self.get_bucket_and_cardinality(data)

        if self.registers[bucket] < cardinality:
            self.registers[bucket] = cardinality

    def estimate(self) -> int:
        # Calculate the alpha constant based on number of registers
        m = self.register_length
        if m == 16:
            alpha_m = 0.673
        elif m == 32:
            alpha_m = 0.697
        elif m == 64:
            alpha_m = 0.709
        else:
            alpha_m = 0.7213 / (1 + 1.079 / m)

        # 1. Raw estimation using the harmonic mean
        sum_inverse_powers = sum(2 ** (-reg) for reg in self.registers)
        raw_estimate = alpha_m * (m**2) / sum_inverse_powers

        # 2. Small range correction
        if raw_estimate < 2.5 * m:
            zero_registers = self.registers.count(0)
            if zero_registers != 0:
                corrected_estimate = m * math.log(m / zero_registers)
            else:
                corrected_estimate = (
                    raw_estimate  # No correction needed if all registers are non-zero
                )
            return int(corrected_estimate)

        # 3. Large range correction
        elif raw_estimate > (2**self.hash_bit_length) / 30:
            corrected_estimate = -(2**self.hash_bit_length) * math.log(
                1 - raw_estimate / (2**self.hash_bit_length)
            )
            return int(corrected_estimate)

        # 4. Intermediate range: no correction needed, return the raw estimate
        else:
            return int(raw_estimate)


def test() -> None:
    for rb in [4, 8, 10, 14]:
        estimates = []
        for _ in range(10):
            data = [
                "".join([choice(ascii_letters) for _ in range(10)]) for _ in range(1000)
            ]
            data = [*data, *data]
            hll = HyperLogLog(register_bits=rb)
            for d in data:
                hll.ingest(d)
            estimates.append(hll.estimate())

        print(f"Registers: {hll.register_length}")
        print(f"Estimates: {max(estimates)=}, {min(estimates)=}")
        print(
            f"Error Range: +/- {abs(((float(max(estimates)) - min(estimates)) / min(estimates)) * 100):.2f}%"
        )
        avg = int(sum(estimates) / len(estimates))
        print(f"Average Estimate: {avg}")
        print(
            f"Average Error: {abs(((float(avg) - len(set(data))) / len(set(data))) * 100):.2f}%"
        )
        print(f"Real Total: {len(data)}")
        print(f"Real Unique: {len(set(data))}\n")


def sized():
    def new_ip() -> str:
        return (
            f"{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}.{randint(0, 255)}"
        )

    data = [new_ip() for _ in range(1_000_000)]
    print("For 1 million IP addresses:")
    print(f"Size of set: {getsizeof(set(data)):3,} bytes")

    hll = HyperLogLog()

    for d in data:
        hll.ingest(d)

    print(f"Size of HLL: {getsizeof(hll):3,} bytes")


if __name__ == "__main__":
    test()
    sized()
