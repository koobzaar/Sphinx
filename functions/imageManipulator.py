import tkinter as tk
from tkinter import filedialog
import cv2
import pyperclip
import numpy as np
import os
import datetime


def select_image_path() -> str:
    """Returns the path to the selected image."""
    path = "NULL"
    root = tk.Tk()
    print("[INFO] Select the image you want to encrypt.")
    root.withdraw()
    path = filedialog.askopenfilename()
    if path != "NULL":
        print("[OK] Image loaded: " + path + ".\n[OK] Image dimensions: " + str(cv2.imread(path).shape) + ".")
    else:
        print("[ERROR] An error has occurred while loading the image.")
    return path


def get_filename_with_timestamp():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    return f"encrypted_image_{date_str}_{time_str}"


def save_encrypted_image(b: list, g: list, r: list, image_path: str, hash_key: str):
    img = cv2.imread(image_path)
    img[:, :, 0], img[:, :, 1], img[:, :, 2] = b, g, r
    output_folder = "./encrypted_output/"
    os.makedirs(output_folder, exist_ok=True)
    file_name = get_filename_with_timestamp()
    cv2.imwrite(f"{output_folder}{file_name}.png", img)
    print(f"[SUCCESS] Encrypted image saved as: {file_name}.png in the 'encrypted_output' folder.")
    pyperclip.copy(hash_key)
    print(f"[INFO] The hash key (required to decrypt) was saved to your clipboard.\n[INFO] Your hash key is: {hash_key}")


def save_decrypted_image(blue: list, green: list, red: list, p: int, q:int, original_image_path: str):
    green,red = red, green

    img=np.zeros((p,q,3),dtype=np.uint8)
    img[:,:,0] = red
    img[:,:,1] = green
    img[:,:,2] = blue
    output_folder = "./decrypted_output/"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cv2.imwrite((output_folder + os.path.basename(original_image_path).removesuffix('.png') + "_decrypted.png"), img)
    print("[SUCCESS] Decrypted image saved as: " + str((os.path.basename(original_image_path)+"_decrypted.png")) + " in the 'decrypted_output' folder.")