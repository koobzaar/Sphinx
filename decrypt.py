import cv2
from importlib import reload  
from functions.generateSecureKey import *
from functions.matrixManipulator import *
from functions.imageManipulator import *
from functions.lorenzAttractor import *
from functions.matrixDNAManipulator import *
from functions.matrixManipulator import *
from functions.console import *

if (__name__ == "__main__"):
    cls()
    show_ascii_art_header()

    # Initialize objects
    lorenz_map = LorenzMap(a=10, b=2.667, c=28, x0=0, y0=0, z0=0, tmax=100)
    dna_encoder = DnaEncoder()
    dna_decoder = DnaDecoder()
    key_matrix_encoder = KeyMatrixEncoder()
    xor_operator = XorOperation()

    # Prompt user to select an image and input a hash key for encryption
    image_path = select_image_path()
    hash_key = input("Enter the hash key used to encrypt the image: ")

    # Update Lorenz map parameters with hash key
    lorenz_map.update_initial_parameters(hash_key)

    # Load image and split into RGB channels
    image = cv2.imread(image_path)
    blue_channel, green_channel, red_channel = split_into_rgb_channels(image)

    # Generate Lorenz map sequence
    num_rows, num_cols = blue_channel.shape
    x_vals, y_vals, z_vals = lorenz_map.generate_sequence(num_rows, num_cols)
    fx_vals, fy_vals, fz_vals = lorenz_map.index_sequence(x_vals, y_vals, z_vals)

    # Encode channels using DNA encoding
    blue_channel_enc, green_channel_enc, red_channel_enc = dna_encoder.encode(blue_channel, green_channel, red_channel)

    # Scramble channels using Lorenz map sequence
    blue_channel_scrambled, green_channel_scrambled, red_channel_scrambled = scramble(fx_vals, fy_vals, fz_vals, blue_channel_enc, green_channel_enc, red_channel_enc, True)

    # Encode key matrix using hash key and blue channel
    matrix_key = key_matrix_encoder.encode(hash_key, blue_channel)

    # Apply XOR operation to scrambled channels and key matrix
    blue_channel_xor, green_channel_xor, red_channel_xor = xor_operator.apply(blue_channel_scrambled, green_channel_scrambled, red_channel_scrambled, matrix_key)

    # Decode channels using DNA decoding
    blue_channel_decoded, green_channel_decoded, red_channel_decoded = dna_decoder.decode(blue_channel_xor, green_channel_xor, red_channel_xor)

    # Save decrypted image
    save_decrypted_image(blue_channel_decoded, green_channel_decoded, red_channel_decoded, num_rows, num_cols, image_path)
