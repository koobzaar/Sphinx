import hashlib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .generateSecureKey import DEFAULT_R, DEFAULT_X0, derive_experiment_key, plot_logistic_map
from .imageManipulator import merge_rgb_channels, split_rgb_channels
from .matrixDNAManipulator import DnaDecoder, DnaEncoder, apply_dna_operation, invert_dna_operation
from .ncaCml import NcaCmlConfig, derive_key_material


@dataclass(frozen=True)
class EncryptionConfig:
    """Configuration for the image-encryption experiment pipeline."""

    x0: float = DEFAULT_X0
    r: float = DEFAULT_R
    offline: bool = True
    plot: bool = False
    anu_api_key: str | None = None
    tile_size: int = 64
    nca_cml: NcaCmlConfig = field(default_factory=NcaCmlConfig)


@dataclass(frozen=True)
class EncryptionResult:
    token: str
    encrypted_image: np.ndarray
    logistic_plot_path: Path | None = None
    lorenz_plot_path: Path | None = None


@dataclass(frozen=True)
class DecryptionResult:
    token: str
    decrypted_image: np.ndarray


def _derive_tile_token(token: str, row_offset: int, column_offset: int) -> str:
    seed_material = f"{token}:{row_offset}:{column_offset}".encode("utf-8")
    return hashlib.sha256(seed_material).hexdigest()


def _iter_tiles(rows: int, columns: int, tile_size: int) -> list[tuple[int, int, slice, slice]]:
    if tile_size <= 0:
        return [(0, 0, slice(0, rows), slice(0, columns))]

    tiles: list[tuple[int, int, slice, slice]] = []
    for row_offset in range(0, rows, tile_size):
        for column_offset in range(0, columns, tile_size):
            row_slice = slice(row_offset, min(row_offset + tile_size, rows))
            column_slice = slice(column_offset, min(column_offset + tile_size, columns))
            tiles.append((row_offset, column_offset, row_slice, column_slice))
    return tiles


def _combine_dna_rows(red_matrix: np.ndarray, green_matrix: np.ndarray, blue_matrix: np.ndarray) -> np.ndarray:
    rows, columns = red_matrix.shape
    combined = np.empty((rows * 3, columns), dtype=np.uint8)
    combined[0::3] = red_matrix
    combined[1::3] = green_matrix
    combined[2::3] = blue_matrix
    return combined


def _split_dna_rows(combined_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return combined_matrix[0::3], combined_matrix[1::3], combined_matrix[2::3]


def _diffuse_dna_rows(
    red_matrix: np.ndarray,
    green_matrix: np.ndarray,
    blue_matrix: np.ndarray,
    row_operations: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    red_result = np.empty_like(red_matrix)
    green_result = np.empty_like(green_matrix)
    blue_result = np.empty_like(blue_matrix)

    for row_index, operation in enumerate(row_operations):
        red_row = red_matrix[row_index]
        green_row = green_matrix[row_index]
        blue_row = blue_matrix[row_index]
        if operation == 0:
            red_out = apply_dna_operation(red_row, green_row, "add")
            green_out = apply_dna_operation(green_row, blue_row, "sub")
            blue_out = apply_dna_operation(blue_row, red_out, "xor")
        elif operation == 1:
            red_out = apply_dna_operation(red_row, green_row, "sub")
            green_out = apply_dna_operation(green_row, blue_row, "xor")
            blue_out = apply_dna_operation(blue_row, red_out, "add")
        else:
            red_out = apply_dna_operation(red_row, green_row, "xor")
            green_out = apply_dna_operation(green_row, blue_row, "add")
            blue_out = apply_dna_operation(blue_row, red_out, "sub")

        red_result[row_index] = red_out
        green_result[row_index] = green_out
        blue_result[row_index] = blue_out

    return red_result, green_result, blue_result


def _invert_dna_rows(
    red_matrix: np.ndarray,
    green_matrix: np.ndarray,
    blue_matrix: np.ndarray,
    row_operations: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    red_result = np.empty_like(red_matrix)
    green_result = np.empty_like(green_matrix)
    blue_result = np.empty_like(blue_matrix)

    for row_index, operation in enumerate(row_operations):
        red_row = red_matrix[row_index]
        green_row = green_matrix[row_index]
        blue_row = blue_matrix[row_index]
        if operation == 0:
            blue_in = invert_dna_operation(blue_row, red_row, "xor")
            green_in = invert_dna_operation(green_row, blue_in, "sub")
            red_in = invert_dna_operation(red_row, green_in, "add")
        elif operation == 1:
            blue_in = invert_dna_operation(blue_row, red_row, "add")
            green_in = invert_dna_operation(green_row, blue_in, "xor")
            red_in = invert_dna_operation(red_row, green_in, "sub")
        else:
            blue_in = invert_dna_operation(blue_row, red_row, "sub")
            green_in = invert_dna_operation(green_row, blue_in, "add")
            red_in = invert_dna_operation(red_row, green_in, "xor")

        red_result[row_index] = red_in
        green_result[row_index] = green_in
        blue_result[row_index] = blue_in

    return red_result, green_result, blue_result


def _pixel_diffusion(
    red_matrix: np.ndarray,
    green_matrix: np.ndarray,
    blue_matrix: np.ndarray,
    ks1: np.ndarray,
    ks2: np.ndarray,
    ks3: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    red_cipher = ((np.bitwise_xor(red_matrix, ks1).astype(np.uint16) + ks2.astype(np.uint16)) % 256).astype(np.uint8)
    green_cipher = (
        (np.bitwise_xor(green_matrix, ks2).astype(np.uint16) + red_cipher.astype(np.uint16)) % 256
    ).astype(np.uint8)
    blue_cipher = (
        (np.bitwise_xor(blue_matrix, green_cipher).astype(np.uint16) + ks3.astype(np.uint16)) % 256
    ).astype(np.uint8)
    return red_cipher, green_cipher, blue_cipher


def _invert_pixel_diffusion(
    red_matrix: np.ndarray,
    green_matrix: np.ndarray,
    blue_matrix: np.ndarray,
    ks1: np.ndarray,
    ks2: np.ndarray,
    ks3: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    blue_plain = np.bitwise_xor(((blue_matrix.astype(np.int16) - ks3.astype(np.int16)) % 256).astype(np.uint8), green_matrix)
    green_plain = np.bitwise_xor(((green_matrix.astype(np.int16) - red_matrix.astype(np.int16)) % 256).astype(np.uint8), ks2)
    red_plain = np.bitwise_xor(((red_matrix.astype(np.int16) - ks2.astype(np.int16)) % 256).astype(np.uint8), ks1)
    return red_plain, green_plain, blue_plain


def _encrypt_tile(
    red_channel: np.ndarray,
    green_channel: np.ndarray,
    blue_channel: np.ndarray,
    token: str,
    config: EncryptionConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, Path | None]:
    key_material = derive_key_material(red_channel.shape[0], red_channel.shape[1], token, config.nca_cml)
    dna_encoder = DnaEncoder()
    dna_decoder = DnaDecoder()

    encoded_red, encoded_green, encoded_blue = dna_encoder.encode(
        red_channel,
        green_channel,
        blue_channel,
        key_material.rules,
    )
    combined = _combine_dna_rows(encoded_red, encoded_green, encoded_blue)
    shuffled = combined[:, key_material.column_permutation]
    shuffled_red, shuffled_green, shuffled_blue = _split_dna_rows(shuffled)
    diffused_red, diffused_green, diffused_blue = _diffuse_dna_rows(
        shuffled_red,
        shuffled_green,
        shuffled_blue,
        key_material.row_operations,
    )
    decoded_red, decoded_green, decoded_blue = dna_decoder.decode(
        diffused_red,
        diffused_green,
        diffused_blue,
        key_material.rules.decode_rules,
    )
    cipher_red, cipher_green, cipher_blue = _pixel_diffusion(
        decoded_red,
        decoded_green,
        decoded_blue,
        key_material.ks1,
        key_material.ks2,
        key_material.ks3,
    )
    return cipher_red, cipher_green, cipher_blue, None


def _decrypt_tile(
    red_channel: np.ndarray,
    green_channel: np.ndarray,
    blue_channel: np.ndarray,
    token: str,
    config: EncryptionConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    key_material = derive_key_material(red_channel.shape[0], red_channel.shape[1], token, config.nca_cml)
    dna_encoder = DnaEncoder()
    dna_decoder = DnaDecoder()

    diffused_red, diffused_green, diffused_blue = _invert_pixel_diffusion(
        red_channel,
        green_channel,
        blue_channel,
        key_material.ks1,
        key_material.ks2,
        key_material.ks3,
    )
    encoded_red, encoded_green, encoded_blue = dna_encoder.encode(
        diffused_red,
        diffused_green,
        diffused_blue,
        key_material.rules.decode_rules,
    )
    shuffled_red, shuffled_green, shuffled_blue = _invert_dna_rows(
        encoded_red,
        encoded_green,
        encoded_blue,
        key_material.row_operations,
    )
    combined = _combine_dna_rows(shuffled_red, shuffled_green, shuffled_blue)
    unshuffled = combined[:, key_material.column_inverse_permutation]
    red_plain_dna, green_plain_dna, blue_plain_dna = _split_dna_rows(unshuffled)
    return dna_decoder.decode(
        red_plain_dna,
        green_plain_dna,
        blue_plain_dna,
        key_material.rules,
    )


def encrypt_image(
    image: np.ndarray,
    config: EncryptionConfig,
    random_bytes: bytes | None = None,
) -> EncryptionResult:
    """Encrypt an RGB image using the repository's experiment pipeline."""
    token, rows, columns = derive_experiment_key(
        image,
        x0=config.x0,
        r=config.r,
        offline=config.offline,
        api_key=config.anu_api_key,
        random_bytes=random_bytes,
    )

    logistic_plot_path = None
    if config.plot:
        logistic_plot_path = plot_logistic_map(config.x0, config.r, rows * columns * 3)

    red_channel, green_channel, blue_channel = split_rgb_channels(image)
    lorenz_plot_path = None
    encrypted_red = np.empty_like(red_channel)
    encrypted_green = np.empty_like(green_channel)
    encrypted_blue = np.empty_like(blue_channel)

    for row_offset, column_offset, row_slice, column_slice in _iter_tiles(rows, columns, config.tile_size):
        tile_token = _derive_tile_token(token, row_offset, column_offset)
        tile_red, tile_green, tile_blue, tile_plot_path = _encrypt_tile(
            red_channel[row_slice, column_slice],
            green_channel[row_slice, column_slice],
            blue_channel[row_slice, column_slice],
            tile_token,
            config,
        )
        encrypted_red[row_slice, column_slice] = tile_red
        encrypted_green[row_slice, column_slice] = tile_green
        encrypted_blue[row_slice, column_slice] = tile_blue
        if lorenz_plot_path is None:
            lorenz_plot_path = tile_plot_path

    return EncryptionResult(
        token=token,
        encrypted_image=merge_rgb_channels(encrypted_red, encrypted_green, encrypted_blue),
        logistic_plot_path=logistic_plot_path,
        lorenz_plot_path=lorenz_plot_path,
    )


def decrypt_image(image: np.ndarray, token: str, config: EncryptionConfig | None = None) -> DecryptionResult:
    """Decrypt an RGB image using the repository's experiment pipeline."""
    active_config = config or EncryptionConfig()
    red_channel, green_channel, blue_channel = split_rgb_channels(image)
    rows, columns = red_channel.shape
    decrypted_red = np.empty_like(red_channel)
    decrypted_green = np.empty_like(green_channel)
    decrypted_blue = np.empty_like(blue_channel)

    for row_offset, column_offset, row_slice, column_slice in _iter_tiles(rows, columns, active_config.tile_size):
        tile_token = _derive_tile_token(token, row_offset, column_offset)
        tile_red, tile_green, tile_blue = _decrypt_tile(
            red_channel[row_slice, column_slice],
            green_channel[row_slice, column_slice],
            blue_channel[row_slice, column_slice],
            tile_token,
            active_config,
        )
        decrypted_red[row_slice, column_slice] = tile_red
        decrypted_green[row_slice, column_slice] = tile_green
        decrypted_blue[row_slice, column_slice] = tile_blue

    return DecryptionResult(
        token=token,
        decrypted_image=merge_rgb_channels(decrypted_red, decrypted_green, decrypted_blue),
    )
