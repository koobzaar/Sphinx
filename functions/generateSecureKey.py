import hashlib
import json
import math
import os
import secrets
import tempfile
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "sphinx-mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .ncaCml import compute_summary_vector


ANU_API_URL = "https://api.quantumnumbers.anu.edu.au"
DEFAULT_X0 = 0.5
DEFAULT_R = 3.9


def logistic_map(x: float, r: float) -> float:
    """Return the next state for the logistic map."""
    if not 0 < x < 1:
        raise ValueError("x0 must be between 0 and 1.")
    if not 0 < r <= 4:
        raise ValueError("r must be between 0 and 4.")
    return r * x * (1 - x)


def generate_random_seq(shape: tuple[int, ...], x0: float, r: float) -> np.ndarray:
    """Generate a pseudo-random uint8 sequence from the logistic map."""
    total_values = int(np.prod(shape))
    random_values = np.empty(total_values, dtype=np.uint8)
    current_value = x0

    for index in range(total_values):
        current_value = logistic_map(current_value, r)
        random_values[index] = int(current_value * 255) & 0xFF

    return random_values.reshape(shape)


def xor_image(pixels: np.ndarray, random_seq: np.ndarray) -> np.ndarray:
    """Apply a byte-wise XOR between an image and a generated sequence."""
    return np.bitwise_xor(pixels, random_seq)


def resolve_anu_api_key(explicit_key: str | None = None) -> str | None:
    """Return an ANU API key from an explicit value or environment."""
    if explicit_key:
        return explicit_key
    return os.getenv("SPHINX_ANU_API_KEY") or os.getenv("ANU_API_KEY")


def get_random_bytes(length: int, offline: bool = True, api_key: str | None = None) -> bytes:
    """Return random bytes from the local secrets module or the ANU QRNG API."""
    if length <= 0:
        raise ValueError("length must be a positive integer.")

    if offline:
        return secrets.token_bytes(length)

    resolved_api_key = resolve_anu_api_key(api_key)
    if not resolved_api_key:
        raise ValueError(
            "ANU online mode requires an API key. Set SPHINX_ANU_API_KEY or pass --anu-api-key."
        )

    word_count = math.ceil(length / 2)
    query = urllib.parse.urlencode({"length": word_count, "type": "hex16", "size": 4})
    request = urllib.request.Request(
        f"{ANU_API_URL}?{query}",
        headers={"x-api-key": resolved_api_key},
        method="GET",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        result_json = json.loads(response.read().decode("utf-8"))

    if not result_json.get("success"):
        raise RuntimeError(result_json.get("message", "ANU QRNG API returned an unknown error."))

    random_hex = "".join(result_json["data"])
    return bytes.fromhex(random_hex)[:length]


def derive_experiment_key(
    image_array: np.ndarray,
    x0: float = DEFAULT_X0,
    r: float = DEFAULT_R,
    offline: bool = True,
    api_key: str | None = None,
    random_bytes: bytes | None = None,
) -> tuple[str, int, int]:
    """Derive the experiment token used by the permutation/XOR pipeline."""
    if image_array.ndim != 3 or image_array.shape[2] != 3:
        raise ValueError("image_array must be an RGB image with shape (rows, columns, 3).")

    summary_vector = compute_summary_vector(image_array)
    digest_length = 32
    entropy_source = random_bytes if random_bytes is not None else get_random_bytes(digest_length, offline, api_key)
    if len(entropy_source) < digest_length:
        raise ValueError("random_bytes must contain at least 32 bytes.")

    digest = hashlib.sha256(summary_vector.tobytes() + entropy_source[:digest_length]).digest()
    rows, columns = image_array.shape[:2]
    return digest.hex(), rows, columns


def get_filename_with_timestamp() -> str:
    """Return a sortable timestamp for analysis outputs."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def plot_logistic_map(x0: float, r: float, iterations: int, output_dir: str | Path = "logistic_maps") -> Path:
    """Save a logistic-map plot used for experiment analysis."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    current_value = x0
    logistic_map_values = np.empty(iterations, dtype=float)
    for index in range(iterations):
        logistic_map_values[index] = current_value
        current_value = logistic_map(current_value, r)

    fig, ax = plt.subplots()
    ax.plot(logistic_map_values, "b,", alpha=0.5)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Logistic map value")
    ax.set_title(f"Logistic map analysis (x0={x0}, r={r})")

    file_path = output_path / f"{get_filename_with_timestamp()}_logistic_map.svg"
    fig.savefig(file_path, dpi=300, format="svg")
    plt.close(fig)
    return file_path
