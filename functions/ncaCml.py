import hashlib
import math
from dataclasses import dataclass

import numpy as np

from .matrixDNAManipulator import DnaRules


DEFAULT_X1_0 = 0.394857698348593
DEFAULT_X2_0 = 0.762757068948018
DEFAULT_X3_0 = 0.689837458934875
DEFAULT_ALPHA_0 = 1.526564542335471
DEFAULT_BETA_0 = 3.143892438432545
DEFAULT_EPSILON_0 = 0.274355311340238


@dataclass(frozen=True)
class NcaCmlConfig:
    """Configuration inspired by the paper's recommended parameter set."""

    alpha_0: float = DEFAULT_ALPHA_0
    beta_0: float = DEFAULT_BETA_0
    epsilon_0: float = DEFAULT_EPSILON_0
    x1_0: float = DEFAULT_X1_0
    x2_0: float = DEFAULT_X2_0
    x3_0: float = DEFAULT_X3_0
    burn_in: int = 1000
    theta_1: int = 6
    theta_2: int = 6
    theta_3: int = 6
    tau_1: int = 10
    tau_2: int = 9
    tau_3: int = 11
    sigma_1: int = 12
    sigma_2: int = 11
    sigma_3: int = 13


@dataclass(frozen=True)
class NcaKeyMaterial:
    """All dynamic values required by the paper-shaped encryption pipeline."""

    digest: str
    rules: DnaRules
    row_operations: np.ndarray
    column_permutation: np.ndarray
    column_inverse_permutation: np.ndarray
    ks1: np.ndarray
    ks2: np.ndarray
    ks3: np.ndarray


def compute_summary_vector(image: np.ndarray) -> np.ndarray:
    """Compute the paper's summary vector SV = mod(B + G, 256) xor R."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected an RGB image with shape (rows, columns, 3).")

    red = image[:, :, 0].astype(np.uint16).reshape(-1)
    green = image[:, :, 1].astype(np.uint16).reshape(-1)
    blue = image[:, :, 2].astype(np.uint16).reshape(-1)
    return (np.bitwise_xor((blue + green) % 256, red)).astype(np.uint8)


def derive_tile_digest(tile_secret: str) -> str:
    """Derive a deterministic one-time digest for a tile from the caller-provided secret."""
    return hashlib.sha256(tile_secret.encode("utf-8")).hexdigest()


def _wrap_unit_interval(value: float) -> float:
    wrapped = value % 1.0
    return min(max(wrapped, 1e-9), 1 - 1e-9)


def _clamp_parameters(alpha: float, beta: float, epsilon: float) -> tuple[float, float, float]:
    safe_alpha = min(max(alpha, 1.0), 1.569)
    safe_beta = min(max(beta, 3.0), 15.0)
    safe_epsilon = min(max(epsilon, 1e-6), 0.999999)
    return safe_alpha, safe_beta, safe_epsilon


def update_initial_parameters(digest: str, config: NcaCmlConfig) -> tuple[float, float, float, float, float, float]:
    """Update the NCA-CML parameters using the digest decomposition from the paper."""
    digest_bytes = bytes.fromhex(digest)
    d = [int(value) for value in digest_bytes]
    denominator = (2**12) * 10

    alpha = config.alpha_0 - (((d[0] + d[1]) ^ (d[2] + d[3] + d[4])) / denominator)
    beta = config.beta_0 + (((d[5] + d[6]) & (d[7] + d[8] + d[9])) / denominator)
    epsilon = config.epsilon_0 + (((d[10] + d[11]) ^ (d[12] + d[13] + d[14])) / denominator)
    x1 = config.x1_0 - (((d[15] + d[16]) & (d[17] + d[18] + d[19])) / denominator)
    x2 = config.x2_0 + (((d[20] + d[21] + d[22]) ^ (d[23] + d[24] + d[25])) / denominator)
    x3 = config.x3_0 - (((d[26] + d[27] + d[28]) ^ (d[29] + d[30] + d[31])) / denominator)

    alpha, beta, epsilon = _clamp_parameters(alpha, beta, epsilon)
    return alpha, beta, epsilon, _wrap_unit_interval(x1), _wrap_unit_interval(x2), _wrap_unit_interval(x3)


def _safe_tan(value: float) -> float:
    tangent = math.tan(value)
    if abs(tangent) < 1e-9:
        tangent = 1e-9 if tangent >= 0 else -1e-9
    return tangent


def nca_map(value: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """Evaluate the NCA map used as the local map inside the coupled lattice."""
    clipped = np.clip(value.astype(float), 1e-9, 1 - 1e-9)
    cot_term = 1.0 / _safe_tan(alpha / (1.0 + beta))
    denominator = beta * np.tan(alpha * clipped) * np.power(1.0 - clipped, beta)
    denominator = np.where(np.abs(denominator) < 1e-9, np.sign(denominator) * 1e-9 + (denominator == 0) * 1e-9, denominator)
    result = 1.0 - (beta ** -4) * ((cot_term * (1.0 + 1.0 / beta)) / denominator)
    return np.mod(result, 1.0)


def generate_cml_sequences(
    rows: int,
    columns: int,
    digest: str,
    config: NcaCmlConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate three chaotic sequences with a 3-site NCA-based CML."""
    alpha, beta, epsilon, x1, x2, x3 = update_initial_parameters(digest, config)
    total_values = config.burn_in + (4 * rows * columns)
    state = np.array([x1, x2, x3], dtype=float)
    retained = np.empty((3, total_values - config.burn_in), dtype=float)

    for iteration in range(total_values):
        mapped = nca_map(state, alpha, beta)
        next_state = (
            (1.0 - epsilon) * mapped
            + (epsilon / 2.0) * (np.roll(mapped, 1) + np.roll(mapped, -1))
        )
        state = np.mod(next_state, 1.0)
        if iteration >= config.burn_in:
            retained[:, iteration - config.burn_in] = state

    return retained[0], retained[1], retained[2]


def postprocess_sequence(sequence: np.ndarray, theta: int) -> np.ndarray:
    """Improve the raw chaotic sequence distribution as described in the paper."""
    scaled = (10**theta) * sequence
    return scaled - np.round(scaled)


def _sequence_position(sequence: np.ndarray, one_based_index: int) -> float:
    return float(sequence[(one_based_index - 1) % len(sequence)])


def _sequence_window(sequence: np.ndarray, start_one_based: int, length: int) -> np.ndarray:
    indices = ((np.arange(length) + start_one_based - 1) % len(sequence)).astype(int)
    return sequence[indices]


def _perm_to_keystream(permutation: np.ndarray, rows: int, columns: int) -> np.ndarray:
    return (permutation.reshape(rows, columns) % 256).astype(np.uint8)


def derive_key_material(rows: int, columns: int, tile_secret: str, config: NcaCmlConfig) -> NcaKeyMaterial:
    """Derive rules, permutations, and key streams for a single image tile."""
    digest = derive_tile_digest(tile_secret)
    x1, x2, x3 = generate_cml_sequences(rows, columns, digest, config)
    x1p = postprocess_sequence(x1, config.theta_1)
    x2p = postprocess_sequence(x2, config.theta_2)
    x3p = postprocess_sequence(x3, config.theta_3)

    mn = rows * columns
    r1 = int((_sequence_position(x3p, mn) * (10**config.tau_1)) % 8)
    r2 = int((_sequence_position(x1p, rows + columns) * (10**config.tau_2)) % 8)
    r3 = int((_sequence_position(x2p, 3 * mn) * (10**config.tau_3)) % 8)

    row_operations = np.empty(rows, dtype=np.uint8)
    for row_index in range(rows):
        one_based_row = row_index + 1
        value = (
            _sequence_position(x3p, rows + (2 * one_based_row)) * (10**config.sigma_1)
            + _sequence_position(x1p, columns + (3 * one_based_row)) * (10**config.sigma_2)
            + _sequence_position(x2p, (5 * rows) + (one_based_row * columns)) * (10**config.sigma_3)
        )
        row_operations[row_index] = int(np.fix(value) % 3)

    column_key = np.concatenate(
        [
            _sequence_window(x3p, columns, columns),
            _sequence_window(x2p, 3 * rows, columns),
            _sequence_window(x1p, rows + columns, 2 * columns),
        ]
    )
    column_permutation = np.argsort(column_key, kind="stable").astype(np.uint32)
    column_inverse_permutation = np.argsort(column_permutation, kind="stable").astype(np.uint32)

    k1 = np.argsort(_sequence_window(x1p, 1, mn), kind="stable").astype(np.uint32)
    k2 = np.argsort(_sequence_window(x2p, mn + 1, mn), kind="stable").astype(np.uint32)
    k3 = np.argsort(_sequence_window(x3p, (2 * mn) + 1, mn), kind="stable").astype(np.uint32)

    return NcaKeyMaterial(
        digest=digest,
        rules=DnaRules(r1, r2, r3),
        row_operations=row_operations,
        column_permutation=column_permutation,
        column_inverse_permutation=column_inverse_permutation,
        ks1=_perm_to_keystream(k1, rows, columns),
        ks2=_perm_to_keystream(k2, rows, columns),
        ks3=_perm_to_keystream(k3, rows, columns),
    )
