from dataclasses import dataclass

import numpy as np


BASE_SYMBOLS = np.array(["A", "C", "G", "T"], dtype="<U1")

# Rules are stored as bit-pair -> base-index maps, using bit-pair order 00, 01, 10, 11.
RULE_BIT_TO_BASE = np.array(
    [
        [0, 1, 2, 3],
        [0, 2, 1, 3],
        [1, 0, 3, 2],
        [2, 0, 3, 1],
        [1, 3, 0, 2],
        [2, 3, 0, 1],
        [3, 1, 2, 0],
        [3, 2, 1, 0],
    ],
    dtype=np.uint8,
)
RULE_BASE_TO_BIT = np.argsort(RULE_BIT_TO_BASE, axis=1).astype(np.uint8)


DNA_OPERATION_TABLES = {
    "xor": np.array(
        [
            [2, 3, 0, 1],
            [3, 2, 1, 0],
            [0, 1, 2, 3],
            [1, 0, 3, 2],
        ],
        dtype=np.uint8,
    ),
    "add": np.array(
        [
            [3, 0, 1, 2],
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
        ],
        dtype=np.uint8,
    ),
    "sub": np.array(
        [
            [1, 2, 3, 0],
            [0, 1, 2, 3],
            [3, 0, 1, 2],
            [2, 3, 0, 1],
        ],
        dtype=np.uint8,
    ),
}


def _build_left_inverse(table: np.ndarray) -> np.ndarray:
    inverse = np.empty_like(table)
    for left in range(4):
        for right in range(4):
            inverse[table[left, right], right] = left
    return inverse


DNA_LEFT_INVERSES = {
    name: _build_left_inverse(table) for name, table in DNA_OPERATION_TABLES.items()
}


def _pair_bits(bit_matrix: np.ndarray) -> np.ndarray:
    paired_bits = bit_matrix.reshape(bit_matrix.shape[0], -1, 2)
    return ((paired_bits[:, :, 0] << 1) | paired_bits[:, :, 1]).astype(np.uint8)


def _unpair_bits(pair_matrix: np.ndarray) -> np.ndarray:
    bit_matrix = np.empty((pair_matrix.shape[0], pair_matrix.shape[1] * 2), dtype=np.uint8)
    bit_matrix[:, 0::2] = pair_matrix >> 1
    bit_matrix[:, 1::2] = pair_matrix & 1
    return bit_matrix


def _normalize_rule(rule: int) -> int:
    if rule < 0 or rule > 7:
        raise ValueError("DNA rule must be between 0 and 7.")
    return int(rule)


def encode_channel(channel: np.ndarray, rule: int) -> np.ndarray:
    """Encode a uint8 image channel into DNA indices using one of the 8 valid rules."""
    normalized_rule = _normalize_rule(rule)
    bit_pairs = _pair_bits(np.unpackbits(channel.astype(np.uint8), axis=1))
    return RULE_BIT_TO_BASE[normalized_rule][bit_pairs]


def decode_channel(dna_matrix: np.ndarray, rule: int) -> np.ndarray:
    """Decode a DNA-index matrix into a uint8 image channel using the selected rule."""
    normalized_rule = _normalize_rule(rule)
    bit_pairs = RULE_BASE_TO_BIT[normalized_rule][dna_matrix.astype(np.uint8)]
    return np.packbits(_unpair_bits(bit_pairs), axis=1)


def apply_dna_operation(left: np.ndarray, right: np.ndarray, operation: str) -> np.ndarray:
    """Apply a DNA operation to two DNA-index matrices."""
    table = DNA_OPERATION_TABLES[operation]
    return table[left.astype(np.uint8), right.astype(np.uint8)]


def invert_dna_operation(result: np.ndarray, right: np.ndarray, operation: str) -> np.ndarray:
    """Recover the left operand of a DNA operation from the result and the right operand."""
    inverse = DNA_LEFT_INVERSES[operation]
    return inverse[result.astype(np.uint8), right.astype(np.uint8)]


@dataclass(frozen=True)
class DnaRules:
    red: int
    green: int
    blue: int

    @property
    def decode_rules(self) -> "DnaRules":
        return DnaRules(7 - self.red, 7 - self.green, 7 - self.blue)


class DnaEncoder:
    """Encode RGB channels into DNA indices using per-channel rules."""

    def encode(
        self,
        red_matrix: np.ndarray,
        green_matrix: np.ndarray,
        blue_matrix: np.ndarray,
        rules: DnaRules,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            encode_channel(red_matrix, rules.red),
            encode_channel(green_matrix, rules.green),
            encode_channel(blue_matrix, rules.blue),
        )


class DnaDecoder:
    """Decode DNA-index matrices into uint8 RGB channels using per-channel rules."""

    def decode(
        self,
        red_matrix: np.ndarray,
        green_matrix: np.ndarray,
        blue_matrix: np.ndarray,
        rules: DnaRules,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            decode_channel(red_matrix, rules.red),
            decode_channel(green_matrix, rules.green),
            decode_channel(blue_matrix, rules.blue),
        )
