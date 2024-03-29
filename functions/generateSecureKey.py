import hashlib
from PIL import Image
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import datetime
import os
import subprocess
from dotenv import dotenv_values
import json
import secrets
from .console import show_ANU_logo
def logistic_map(x, r):
    return r * x * (1 - x)


def generate_random_seq(shape, x0, r):
    m, n, _ = shape
    random_seq = []

    for i in tqdm(range(m * n * 3), desc="[PRIVATE KEY] ──█ Generating a random sequence of numbers using the logistic map."):
        x0 = logistic_map(x0, r)
        random_seq.append(int(x0 * 255))

    return np.array(random_seq).reshape(shape)


def xor_image(pix, random_seq):
    return pix ^ random_seq


def get_big_hex16_number(array_length,offline):
    if(offline):
        print("\n\n[XXXXXXXXX]> [OFFLINE MODE] | ───█  - using Python's secrets module to generate a random sequence of numbers.")
        result = secrets.token_hex(array_length)
        result_json = {"success": True, "data": result}   
        print("[XXXXXXXXX]> [OFFLINE MODE] | ───█  -  The sequence of quantum random numbers has been generated.\n\n") 
    else:
        print("\n\n[OOOOOOOO]> [ONLINE MODE] | ───█  - using the Australian National University API to generate a random sequence of numbers.")
        show_ANU_logo()
        env_vars = dotenv_values(".env")
        api_key = env_vars["API_KEY"]
        api_url = "https://api.quantumnumbers.anu.edu.au"
        data_type = "hex16"
        block_size = "4"
        print("\n\n[OOOOOOOO]> [ONLINE MODE] | ───█  - connecting...")
        curl_command = f'curl -X GET -H "x-api-key:{api_key}" "{api_url}?length={array_length}&type={data_type}&size={block_size}"'
        result = subprocess.check_output(curl_command, shell=True)
        result_json = json.loads(result)
        if(result_json["success"] == False):
            print("\n\n[ERROR] ────█ Australian National University returned an error on their API. The process cannot be completed.")
            print(result_json["message"])
            exit(1)
        else:
            print("\n[OOOOOOOO]> [ONLINE MODE] | ───█  - Quantum random numbers generated successfully.\n\n")
    return result_json["data"]

def generate_key_and_dimensions(encrypted_img, offline):
    key = hashlib.sha256()
    key.update(encrypted_img)
    random_numbers = get_big_hex16_number(len(key.hexdigest()), offline)
    # Concatenate the random numbers into a single string
    random_numbers = "".join(random_numbers)
    # Convert the string to bytes
    random_numbers = bytes.fromhex(random_numbers)
    # Convert the key to bytes
    key = bytes.fromhex(key.hexdigest())
    # Merge the key and the random numbers
    merged_bytes = bytes([a ^ b for a, b in zip(key, random_numbers)])
    return merged_bytes.hex(), *encrypted_img.shape[:2]

def convert_to_jpg(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode != "RGB":
            print("[PRIVATE KEY] ────█ Converting image to RGB...")
            img = img.convert("RGB")
        # Get the file name and extension
        file_name, file_ext = os.path.splitext(image_path)
        # Save as JPEG
        jpg_path = file_name + ".jpg"
        img.save(jpg_path, "JPEG")
        # Open the JPEG and return as PIL Image object
        with Image.open(jpg_path) as jpg_img:
            return jpg_img.copy()

def securekey(iname, plot, offline):
    img = convert_to_jpg(image_path=iname)
    pix = np.array(img)
    x0 = input("[PRIVATE KEY] ────█ Enter x0 (press enter to use default value of 0.5): ")
    if x0 == "":
        x0 = 0.5
        print("[PRIVATE KEY] ──█ Using default value of x0 = 0.5")
    else:
        x0 = float(x0)
        print(f"[PRIVATE KEY] ────█ Using x0 = {x0}")
    r = input("[PRIVATE KEY] ────█ Enter r (press enter to use default value of 3.9): ")
    if r == "":
        r = 3.9
        print("[PRIVATE KEY] ──█ Using default value of r = 3.9")
    else:
        r = float(r)
        print(f"[PRIVATE KEY] ────█ Using r = {r}")
    random_seq = generate_random_seq(pix.shape, x0, r)
    encrypted_img = xor_image(pix, random_seq)
    key = generate_key_and_dimensions(encrypted_img, offline)
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

    for i in tqdm(range(iterations), desc="[PRIVATE KEY] ────█ Plotting logistic map..."):
        logistic_map_values.append(x)
        x = logistic_map(x, r)

    fig, ax = plt.subplots()
    ax.plot(logistic_map_values, "b,", alpha=0.5)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Logistic Map Value")
    ax.set_title(f"Logistic Map with x0={x0} and r={r}")

    plt.savefig(f'./logistic_maps/{get_filename_with_timestamp()}_lorenz_graph.svg', dpi=300, format='svg')
    plt.close(fig)