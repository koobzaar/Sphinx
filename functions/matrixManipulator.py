import numpy as np


def _apply_permutation(channel: np.ndarray, permutation: np.ndarray, inverse: bool) -> np.ndarray:
    flat_channel = channel.reshape(-1)
    if flat_channel.size != permutation.size:
        raise ValueError("Permutation size must match the flattened channel size.")

    if inverse:
        restored = np.empty_like(flat_channel)
        restored[permutation] = flat_channel
        return restored.reshape(channel.shape)

    return flat_channel[permutation].reshape(channel.shape)


def scramble(
    red_permutation: np.ndarray,
    green_permutation: np.ndarray,
    blue_permutation: np.ndarray,
    red_channel: np.ndarray,
    green_channel: np.ndarray,
    blue_channel: np.ndarray,
    inverse: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply or reverse the Lorenz-based channel permutation."""
    return (
        _apply_permutation(red_channel, red_permutation, inverse),
        _apply_permutation(green_channel, green_permutation, inverse),
        _apply_permutation(blue_channel, blue_permutation, inverse),
    )
