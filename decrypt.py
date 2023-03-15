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
    showASCIIartHeader()
    # Prompt user to select an image and input a hash key for encryption
    image_path = select_image_path()
    hash_key = input("Digite a chave de hash utilizada para encriptar a imagem: ")
    update_initial_parameters(hash_key) 
    image = cv2.imread(image_path)
    red_channel, green_channel, blue_channel = split_into_rgb_channels(image)
    num_rows, num_cols = red_channel.shape
    x_vals, y_vals, z_vals = generate_chaos_sequence(num_rows, num_cols)
    fx_vals, fy_vals, fz_vals = sequence_indexing(x_vals, y_vals, z_vals)
    matrix_key = key_matrix_encode(hash_key, blue_channel)
    blue_channel_enc, green_channel_enc, red_channel_enc = dna_encode(blue_channel, green_channel, red_channel)
    blue_channel_scrambled, green_channel_scrambled, red_channel_scrambled = scramble_new(fx_vals, fy_vals, fz_vals, blue_channel_enc, green_channel_enc, red_channel_enc)
    blue_channel_xor, red_channel_xor, green_channel_xor = xor_operation_new(blue_channel_scrambled, green_channel_scrambled, red_channel_scrambled, matrix_key)
    blue_channel_decoded, green_channel_decoded, red_channel_decoded = dna_decode(blue_channel_xor, green_channel_xor, red_channel_xor)
    save_decrypted_image(blue_channel_decoded, green_channel_decoded, red_channel_decoded, num_rows, num_cols, image_path)
