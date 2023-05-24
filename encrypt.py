import argparse
import numpy as np
from functions.generateSecureKey import *
from functions.matrixManipulator import *
from functions.imageManipulator import *
from functions.lorenzAttractor import *
from functions.matrixDNAManipulator import *
from functions.matrixManipulator import *
from functions.console import *

parser = argparse.ArgumentParser(description="Encrypt an image using the Lorenz Attractor and DNA encoding.")
parser.add_argument('--plot', action='store_true', help="Plot the Lorenz Attractor.");
if (__name__ == "__main__"):
    args = parser.parse_args()
    cls()
    
    lorenz_map = LorenzMap(a=10, b=2.667, c=28, x0=0, y0=0, z0=0, tmax=100)
    dna_encoder = DnaEncoder()
    dna_decoder = DnaDecoder()
    key_matrix_encoder = KeyMatrixEncoder()
    xor_operator = XorOperation()
    #self, a: float = 10, b: float = 2.667, c: float = 28, x0: float = 0, y0: float = 0, z0: float = 0, tmax: float = 100) -> None:
    show_ascii_art_header()
    selectedImagePath = select_image_path()
    encryptionKey, rows, columns = securekey(selectedImagePath, args.plot)

    # Update the LorenzMap object's initial parameters with the encryption key
    lorenz_map.update_initial_parameters(encryptionKey)

    # Decompose the selected image into its blue, green, and red channels
    blueChannel, greenChannel, redChannel = decompose_matrix(selectedImagePath)
    encodedBlueChannel, encodedGreenChannel, encodedRedChannel = dna_encoder.encode(blueChannel, greenChannel, redChannel)
    encodedKeyMatrix = key_matrix_encoder.encode(encryptionKey, blueChannel)
    finalBlueChannel, finalGreenChannel, finalRedChannel = xor_operator.apply(encodedBlueChannel, encodedGreenChannel, encodedRedChannel, encodedKeyMatrix)
    chaosSeqX, chaosSeqY, chaosSeqZ = lorenz_map.generate_sequence(rows, columns)
    # if args.plot:
    #     lorenz_map.plot_sequence(chaosSeqX, chaosSeqY, chaosSeqZ)
    indexedSeqX, indexedSeqY, indexedSeqZ = lorenz_map.index_sequence(chaosSeqX, chaosSeqY, chaosSeqZ)

    # Scramble the encoded channels using the indexed chaotic sequence
    scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel = scramble(indexedSeqX, indexedSeqY, indexedSeqZ, finalBlueChannel, finalRedChannel, finalGreenChannel, False)
    decodedBlueChannel, decodedGreenChannel, decodedRedChannel = dna_decoder.decode(scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel)
    recoveredImage = save_encrypted_image(decodedBlueChannel, decodedGreenChannel, decodedRedChannel, selectedImagePath, encryptionKey)
