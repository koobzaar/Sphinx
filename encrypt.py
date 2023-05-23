import numpy as np
from functions.generateSecureKey import *
from functions.matrixManipulator import *
from functions.imageManipulator import *
from functions.lorenzAttractor import *
from functions.matrixDNAManipulator import *
from functions.matrixManipulator import *
from functions.console import *

if (__name__ == "__main__"):
    cls()
    lorenz_map = LorenzMap(a=10, b=2.667, c=28, x0=0, y0=0, z0=0, tmax=100)
    #self, a: float = 10, b: float = 2.667, c: float = 28, x0: float = 0, y0: float = 0, z0: float = 0, tmax: float = 100) -> None:
    showASCIIartHeader()
    selectedImagePath = select_image_path()
    encryptionKey, rows, columns = securekey(selectedImagePath)

    lorenz_map.update_initial_parameters(encryptionKey)
    blueChannel, greenChannel, redChannel = decompose_matrix(selectedImagePath)
    encodedBlueChannel, encodedGreenChannel, encodedRedChannel = dna_encode(blueChannel, greenChannel, redChannel)
    encodedKeyMatrix = key_matrix_encode(encryptionKey, blueChannel)
    finalBlueChannel, finalGreenChannel, finalRedChannel = xor_operation(encodedBlueChannel, encodedGreenChannel, encodedRedChannel, encodedKeyMatrix)
    chaosSeqX, chaosSeqY, chaosSeqZ = lorenz_map.generate_sequence(rows, columns)
    lorenz_map.plot_sequence(chaosSeqX, chaosSeqY, chaosSeqZ)
    indexedSeqX, indexedSeqY, indexedSeqZ = lorenz_map.index_sequence(chaosSeqX, chaosSeqY, chaosSeqZ)
    scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel = scramble(indexedSeqX, indexedSeqY, indexedSeqZ, finalBlueChannel, finalRedChannel, finalGreenChannel)
    decodedBlueChannel, decodedGreenChannel, decodedRedChannel = dna_decode(scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel)
    recoveredImage = save_encrypted_image(decodedBlueChannel, decodedGreenChannel, decodedRedChannel, selectedImagePath, encryptionKey)
