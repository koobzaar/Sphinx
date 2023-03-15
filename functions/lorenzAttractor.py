import textwrap
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from bisect import bisect_left as bsearch
from tqdm import tqdm
import matplotlib.pyplot as plt
import datetime

a, b, c = 10, 2.667, 28
x0, y0, z0 = 0, 0, 0
tmax = 100

def lorenz(X, t, a, b, c):
    x, y, z = X
    x_dot = -a*(x - y)
    y_dot = c*x - y - x*z
    z_dot = -b*z + x*y
    return x_dot, y_dot, z_dot

def update_initial_parameters(key):
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
    global x0, y0, z0
    x0 += t1 / 256
    y0 += t2 / 256
    z0 += t3 / 256



def generate_chaos_sequence(rows, columns):
    if not isinstance(rows, int) or not isinstance(columns, int):
        raise TypeError("rows and columns should be integers")
    if rows <= 0 or columns <= 0:
        raise ValueError("rows and columns should be positive integers")
    global initial_x, initial_y, initial_z, a_coefficient, b_coefficient, c_coefficient, total_steps
    total_steps = rows * columns * 4
    x_array = np.array((rows, columns * 4))
    y_array = np.array((rows, columns * 4))
    z_array = np.array((rows, columns * 4))
    time_array = np.linspace(0, tmax, total_steps)
    result_array = odeint(lorenz, (x0, y0, z0), time_array, args=(a, b, c))
    x_array, y_array, z_array = result_array.T
    x_array = x_array[:(total_steps)]
    y_array = y_array[:(total_steps)]
    z_array = z_array[:(total_steps)]
    return x_array, y_array, z_array

def sequence_indexing(x, y, z):
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(z, np.ndarray):
        raise ValueError("All input parameters must be NumPy arrays")
    if x.shape != y.shape or x.shape != z.shape:
        raise ValueError("All input arrays must have the same shape")
    if not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number) or not np.issubdtype(z.dtype, np.number):
        raise ValueError("All input arrays must have a numerical data type")
    
    n = len(x)
    fx = np.zeros((n), dtype=np.uint32)
    fy = np.zeros((n), dtype=np.uint32)
    fz = np.zeros((n), dtype=np.uint32)
    seq = sorted(x)
    for k1 in tqdm(range(0, n), desc="────█ Indexing Lorenz sequence for x..."):
        t = x[k1]
        k2 = bsearch(seq, t)
        fx[k1] = k2
    seq = sorted(y)
    for k1 in tqdm(range(0, n), desc="────█ Indexing Lorenz sequence for y..."):
        t = y[k1]
        k2 = bsearch(seq, t)
        fy[k1] = k2
    seq = sorted(z)
    for k1 in tqdm(range(0, n), desc="────█ Indexing Lorenz sequence for z..."):
        t = z[k1]
        k2 = bsearch(seq, t)
        fz[k1] = k2
    return fx, fy, fz

def get_filename_with_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y_%H-%M")

def plot(x, y, z):
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray) or not isinstance(z, np.ndarray):
        raise ValueError("All input parameters must be NumPy arrays")
    if x.shape != y.shape or x.shape != z.shape:
        raise ValueError("All input arrays must have the same shape")
    if not np.issubdtype(x.dtype, np.number) or not np.issubdtype(y.dtype, np.number) or not np.issubdtype(z.dtype, np.number):
        raise ValueError("All input arrays must have a numerical data type")
    
    fig = plt.figure()
    fig = plt.figure(figsize=(50, 50), dpi=400)
    ax = fig.add_subplot(111, projection='3d')
    s = 10
    N = len(x)
    c = np.linspace(0, 1, N)
    for i in tqdm(range(0, N - s, s), desc="────█ Plotting 3D graph..."):
        ax.plot(x[i:i + s + 1], y[i:i + s + 1], z[i:i + s + 1], color=(1 - c[i], c[i], 1), alpha=0.4)
    ax.set_axis_off()
    ax.set_facecolor('black')
    ax.azim = -20   # z rotation (default=270)
    ax.elev = 0    # x rotation (default=0)
    ax.dist = 7.5    # define perspective (default=10)
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_zlim(np.min(z), np.max(z))
    ax.set_aspect('equal')
    fig.patch.set_facecolor('black')
    
    plt.savefig(f'./chaotic_maps/{get_filename_with_timestamp()}_lorenz_graph.png', transparent=True)
