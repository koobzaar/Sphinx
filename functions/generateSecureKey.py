import hashlib
from PIL import Image
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import datetime
import os
def logistic_map(x, r):
    return r * x * (1 - x)


def generate_random_seq(shape, x0, r):
    m, n, _ = shape
    random_seq = []

    for i in tqdm(range(m * n * 3), desc="──█ Generating the hash key using the original pixels of the image and a logistic map..."):
        x0 = logistic_map(x0, r)
        random_seq.append(int(x0 * 255))

    return np.array(random_seq).reshape(shape)


def encrypt_image(pix, random_seq):
    return pix ^ random_seq


def generate_key_and_dimensions(encrypted_img):
    key = hashlib.sha256()
    key.update(encrypted_img)
    return key.hexdigest(), *encrypted_img.shape[:2]

def convert_to_jpg(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != "RGB":
            print("────█ Converting image to RGB...")
            img = img.convert("RGB")
        # Get the file name and extension
        file_name, file_ext = os.path.splitext(image_path)
        # Save as JPEG
        jpg_path = file_name + ".jpg"
        img.save(jpg_path, "JPEG")
        # Open the JPEG and return as PIL Image object
        with Image.open(jpg_path) as jpg_img:
            return jpg_img.copy()

def securekey(iname, plot):
    img = convert_to_jpg(image_path=iname)
    pix = np.array(img)
    x0 = input("────█ Enter x0 (press enter to use default value of 0.5): ")
    if x0 == "":
        x0 = 0.5
        print("──█ Using default value of x0 = 0.5")
    else:
        x0 = float(x0)
        print(f"────█ Using x0 = {x0}")
    r = input("────█ Enter r (press enter to use default value of 3.9): ")
    if r == "":
        r = 3.9
        print("──█ Using default value of r = 3.9")
    else:
        r = float(r)
        print(f"────█ Using r = {r}")
    random_seq = generate_random_seq(pix.shape, x0, r)
    encrypted_img = encrypt_image(pix, random_seq)
    key = generate_key_and_dimensions(encrypted_img)
    m, n, _ = pix.shape
    if(plot):
        plot_logistic_map(x0, r, m * n * 3)
    return key

def get_filename_with_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y_%H-%M")

def plot_logistic_map(x0, r, n):
    x = x0
    iterations = n
    logistic_map_values = []

    for i in tqdm(range(iterations), desc="────█ Plotting logistic map..."):
        logistic_map_values.append(x)
        x = logistic_map(x, r)

    fig, ax = plt.subplots()
    ax.plot(logistic_map_values, "b,", alpha=0.5)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Logistic Map Value")
    ax.set_title(f"Logistic Map with x0={x0} and r={r}")

    plt.savefig(f'./logistic_maps/{get_filename_with_timestamp()}_lorenz_graph.svg', dpi=300, format='svg')
    plt.close(fig)