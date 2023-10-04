import os
import tempfile
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "sphinx-mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import odeint


@dataclass
class LorenzMap:
    """Generate Lorenz attractor sequences for the experiment permutation step."""

    a: float
    b: float
    c: float
    x0: float
    y0: float
    z0: float
    tmax: float

    def generate_sequence(self, rows: int, columns: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return Lorenz coordinates sized for DNA-encoded image channels."""
        total_steps = rows * columns * 4
        time_array = np.linspace(0, self.tmax, total_steps, dtype=float)
        result_array = odeint(
            self._lorenz,
            (self.x0, self.y0, self.z0),
            time_array,
            args=(self.a, self.b, self.c),
            mxstep=5000,
        )
        x_array, y_array, z_array = result_array.T
        return x_array[:total_steps], y_array[:total_steps], z_array[:total_steps]

    def index_sequence(
        self, x: np.ndarray, y: np.ndarray, z: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Convert Lorenz coordinates into stable permutation indices."""
        return (
            np.argsort(x, kind="stable").astype(np.uint32),
            np.argsort(y, kind="stable").astype(np.uint32),
            np.argsort(z, kind="stable").astype(np.uint32),
        )

    def plot_sequence(
        self, x_values: np.ndarray, y_values: np.ndarray, z_values: np.ndarray, output_dir: str | Path = "lorenz_attractor_graphs"
    ) -> Path:
        """Save a Lorenz attractor SVG for analysis."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        fig = plt.figure(figsize=(12, 12), dpi=300)
        ax = fig.add_subplot(111, projection="3d")
        ax.set_axis_off()
        ax.set_facecolor("black")

        step_size = 10
        num_points = len(x_values)
        color_values = np.linspace(0, 1, num_points)
        for index in range(0, num_points - step_size, step_size):
            x_segment = x_values[index : index + step_size + 1]
            y_segment = y_values[index : index + step_size + 1]
            z_segment = z_values[index : index + step_size + 1]
            color = (1 - color_values[index], color_values[index], 1)
            ax.plot(x_segment, y_segment, z_segment, color=color, alpha=0.4)

        file_path = output_path / f"{self.get_filename_with_timestamp()}.svg"
        fig.savefig(file_path, transparent=True, format="svg")
        plt.close(fig)
        return file_path

    def update_initial_parameters(self, key: str) -> None:
        """Adjust initial Lorenz coordinates from a 256-bit hex token."""
        if not isinstance(key, str):
            raise TypeError("key should be a string.")
        if len(key) != 64:
            raise ValueError("key should be a 256-bit hexadecimal string.")

        try:
            int(key, 16)
        except ValueError as exc:
            raise ValueError("key should contain hexadecimal characters only.") from exc

        key_bin = bin(int(key, 16))[2:].zfill(256)
        key_chunks = textwrap.wrap(key_bin, 8)

        t1 = t2 = t3 = 0
        for chunk in key_chunks[:11]:
            t1 ^= int(chunk, 2)
        for chunk in key_chunks[11:22]:
            t2 ^= int(chunk, 2)
        for chunk in key_chunks[22:]:
            t3 ^= int(chunk, 2)

        self.x0 += t1 / 256
        self.y0 += t2 / 256
        self.z0 += t3 / 256

    @staticmethod
    def _lorenz(position: tuple[float, float, float], _: float, a: float, b: float, c: float) -> tuple[float, float, float]:
        x, y, z = position
        x_dot = -a * (x - y)
        y_dot = c * x - y - x * z
        z_dot = -b * z + x * y
        return x_dot, y_dot, z_dot

    @staticmethod
    def get_filename_with_timestamp() -> str:
        """Return a timestamped filename stem for Lorenz plots."""
        return datetime.now().strftime("lorenz_%Y-%m-%d_%H-%M-%S")
