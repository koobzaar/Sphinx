from abc import ABC, abstractmethod
from bisect import bisect_left as bsearch
import datetime
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.integrate import odeint
import string
from tqdm import tqdm
from typing import List, Tuple
import textwrap
import os
class ChaoticMap(ABC):
    @abstractmethod
    def generate_sequence(self, rows: int, columns: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        pass
    
    @abstractmethod
    def index_sequence(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        pass
    
    @abstractmethod
    def plot_sequence(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, filename: str) -> None:
        pass

class LorenzMap(ChaoticMap):
    def __init__(self, a: float, b: float, c: float, x0: float, y0: float, z0: float, tmax: float) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.tmax = tmax
    
    def generate_sequence(self, rows: int, columns: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        total_steps = rows * columns * 4
        time_array = np.linspace(0, self.tmax, total_steps)
        result_array = odeint(self.lorenz, (self.x0, self.y0, self.z0), time_array, args=(self.a, self.b, self.c))
        x_array, y_array, z_array = result_array.T
        x_array = x_array[:(total_steps)]
        y_array = y_array[:(total_steps)]
        z_array = z_array[:(total_steps)]
        return x_array, y_array, z_array
    
    def index_sequence(self, x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        n = len(x)
        x_indices = np.zeros((n), dtype=np.uint32)
        y_indices = np.zeros((n), dtype=np.uint32)
        z_indices = np.zeros((n), dtype=np.uint32)
        sorted_x = sorted(x)
        sorted_y = sorted(y)
        sorted_z = sorted(z)
        for i, x_val in tqdm(enumerate(x), desc="────█ Indexing Lorenz sequence for x..."):
            x_index = bsearch(sorted_x, x_val)
            x_indices[i] = x_index
        for i, y_val in tqdm(enumerate(y), desc="────█ Indexing Lorenz sequence for y..."):
            y_index = bsearch(sorted_y, y_val)
            y_indices[i] = y_index
        for i, z_val in tqdm(enumerate(z), desc="────█ Indexing Lorenz sequence for z..."):
            z_index = bsearch(sorted_z, z_val)
            z_indices[i] = z_index
        return x_indices, y_indices, z_indices
    
    def plot_sequence(self, x_values: np.ndarray, y_values: np.ndarray, z_values: np.ndarray) -> None:
        # Create a figure with a size of 20x20 inches and a DPI of 400
        fig = plt.figure(figsize=(20, 20), dpi=400)
        
        # Create a 3D axis object
        ax = fig.add_subplot(111, projection='3d')
        
        # Set the axis off
        ax.set_axis_off()
        
        # Set the face color of the axis to black
        ax.set_facecolor('black')
        
        # Set the perspective of the plot to a distance of 7.5
        ax.dist = 7.5
        
        # Set the x, y, and z limits of the plot to the minimum and maximum values of the input arrays
        ax.set_xlim(np.min(x_values), np.max(x_values))
        ax.set_ylim(np.min(y_values), np.max(y_values))
        ax.set_zlim(np.min(z_values), np.max(z_values))
        
        # Iterate over the range of the length of the input arrays, incrementing by a step size of `s`
        step_size = 10
        num_points = len(x_values)
        color_values = np.linspace(0, 1, num_points)
        for i in tqdm(range(0, num_points - step_size, step_size), desc="────█ Plotting 3D graph..."):
            # Plot a line segment between each point in the range and the next point in the range
            x_segment = x_values[i:i + step_size + 1]
            y_segment = y_values[i:i + step_size + 1]
            z_segment = z_values[i:i + step_size + 1]
            color = (1 - color_values[i], color_values[i], 1)
            ax.plot(x_segment, y_segment, z_segment, color=color, alpha=0.4)
        
        ax.set_aspect('equal')
        
        # Save the plot as an SVG file with a filename that includes a timestamp
        filename = self.get_filename_with_timestamp()
        if not os.path.exists('lorenz_attractor_graphs'):
            os.makedirs('lorenz_attractor_graphs')
        plt.savefig(f'lorenz_attractor_graphs/{filename}', transparent=True, format="svg")

    def lorenz(self, X, t, a, b, c):
        x, y, z = X
        x_dot = -a*(x - y)
        y_dot = c*x - y - x*z
        z_dot = -b*z + x*y
        return x_dot, y_dot, z_dot

    def generate_chaos_sequence(self, rows: int, columns: int, filename: str) -> None:
        x, y, z = self.generate_sequence(rows, columns)
        fx, fy, fz = self.index_sequence(x, y, z)
        self.plot_sequence(x, y, z, f'./chaotic_maps/{filename}.svg')

    def update_initial_parameters(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key should be a string")
        if len(key) != 64:
            raise ValueError("key should be a 256-bit hexadecimal string")

        key_bin = bin(int(key, 16))[2:].zfill(256)  # covert hex key digest to binary
        k = {}  # key dictionary
        key_32_parts = textwrap.wrap(key_bin, 8)  # slicing key into 8 parts
        num = 1
        
        for i in key_32_parts:
            k[f"k{num}"] = i
            num += 1
        t1 = t2 = t3 = 0
        for i in range(1, 12):
            t1 ^= int(k[f"k{i}"], 2)
        for i in range(12, 23):
            t2 ^= int(k[f"k{i}"], 2)
        for i in range(23, 33):
            t3 ^= int(k[f"k{i}"], 2)
        self.x0 += t1 / 256
        self.y0 += t2 / 256
        self.z0 += t3 / 256


    def get_filename_with_timestamp(self) -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"encrypted_file_{timestamp}_{random_string}.svg"
        return filename
