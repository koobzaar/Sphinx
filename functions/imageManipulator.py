import tkinter as tk
from tkinter import filedialog
import cv2
import time
import pyperclip
import numpy as np
import os
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

def save_encrypted_image(b: list, g: list, r: list, image_path: str, hash_key: str):
    """Encrypts the image and saves it as a PNG file in the 'encrypted_output' folder.
    
    Args:
    - b: list representing the blue channel
    - g: list representing the green channel
    - r: list representing the red channel
    - image_path: string representing the path to the original image
    - hash_key: string representing the hash key
    """
    img = cv2.imread(image_path)
    img[:, :, 2] = r
    img[:, :, 1] = g
    img[:, :, 0] = b
    cv2.imwrite(("./encrypted_output/" + str(int(time.time())) + ".png"), img)
    print("[SUCCESS] Encrypted image saved as: " + str(int(time.time())) + ".png in the 'encrypted_output' folder.\n[INFO] The hash key (required to decrypt) was saved to your clipboard.\n[INFO] Your hash key is: " + hash_key)
    pyperclip.copy(hash_key)

def save_decrypted_image(blue: list, green: list, red: list, p: int, q:int, original_image_path: str):
    green,red = red, green
    img=np.zeros((p,q,3),dtype=np.uint8)
    img[:,:,0] = red
    img[:,:,1] = green
    img[:,:,2] = blue
    cv2.imwrite(("decrypter_output/"+os.path.basename(original_image_path).removesuffix('.png')+"_decrypted.png"), img)
    print("[SUCCESS] Decrypted image saved as: " + str((os.path.basename(original_image_path)+"_decrypted.png")) + ".png in the 'decrypted_output' folder.")