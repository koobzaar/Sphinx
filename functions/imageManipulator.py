import numpy as np
from datetime import datetime
from pathlib import Path

from PIL import Image


def load_rgb_image(image_path: str | Path) -> np.ndarray:
    """Load an image and return an RGB uint8 array."""
    with Image.open(image_path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.uint8)


def split_rgb_channels(image: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return image channels in explicit RGB order."""
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected an RGB image with shape (rows, columns, 3).")
    return image[:, :, 0], image[:, :, 1], image[:, :, 2]


def merge_rgb_channels(red: np.ndarray, green: np.ndarray, blue: np.ndarray) -> np.ndarray:
    """Merge separate RGB channels into a single RGB image."""
    if red.shape != green.shape or green.shape != blue.shape:
        raise ValueError("RGB channels must have matching shapes.")
    return np.dstack((red, green, blue)).astype(np.uint8)


def save_rgb_image(image: np.ndarray, output_path: str | Path) -> Path:
    """Save an RGB image to disk."""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image, mode="RGB").save(destination)
    return destination


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_encrypted_image(image: np.ndarray, image_path: str | Path, output_dir: str | Path = "encrypted_output") -> Path:
    """Save an encrypted image using a timestamped filename."""
    source = Path(image_path)
    output_path = Path(output_dir) / f"{source.stem}_encrypted_{_timestamp()}.png"
    return save_rgb_image(image, output_path)


def save_decrypted_image(image: np.ndarray, image_path: str | Path, output_dir: str | Path = "decrypted_output") -> Path:
    """Save a decrypted image using a stable filename."""
    source = Path(image_path)
    output_path = Path(output_dir) / f"{source.stem}_decrypted.png"
    return save_rgb_image(image, output_path)
