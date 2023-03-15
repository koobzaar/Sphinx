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
    showASCIIartHeader()
    selectedImagePath = select_image_path()
    encryptionKey, rows, columns = securekey(selectedImagePath)

    update_lorentz(encryptionKey)
    blueChannel, greenChannel, redChannel = decompose_matrix(selectedImagePath)
    encodedBlueChannel, encodedGreenChannel, encodedRedChannel = dna_encode(blueChannel, greenChannel, redChannel)
    encodedKeyMatrix = key_matrix_encode(encryptionKey, blueChannel)
    finalBlueChannel, finalGreenChannel, finalRedChannel = xor_operation(encodedBlueChannel, encodedGreenChannel, encodedRedChannel, encodedKeyMatrix)
    chaosSeqX, chaosSeqY, chaosSeqZ = gen_chaos_seq(rows, columns)
    plot(chaosSeqX, chaosSeqY, chaosSeqZ)
    indexedSeqX, indexedSeqY, indexedSeqZ = sequence_indexing(chaosSeqX, chaosSeqY, chaosSeqZ)
    scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel = scramble(indexedSeqX, indexedSeqY, indexedSeqZ, finalBlueChannel, finalRedChannel, finalGreenChannel)
    decodedBlueChannel, decodedGreenChannel, decodedRedChannel = dna_decode(scrambledBlueChannel, scrambledGreenChannel, scrambledRedChannel)
    recoveredImage = save_encrypted_image(decodedBlueChannel, decodedGreenChannel, decodedRedChannel, selectedImagePath, encryptionKey)
