from functions.imageManipulator import importarImagem, recover_image
from functions.generateSecureKey import securekey
from functions.lorenzAttractor import update_lorentz, gen_chaos_seq, sequence_indexing
from functions.matrixManipulator import decompose_matrix, decompose_matrix, scramble
from functions.matrixDNAManipulator import dna_encode, key_matrix_encode, xor_operation, dna_decode
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
if (__name__ == "__main__"):
    cls()
    with open('header', 'r') as f:
        header = f.read()
    print(header)
    print("Esperando pelo input de uma imagem...")
    caminhoImagem = importarImagem()

    chaveHash, larguraImagem, alturaImagem =  securekey(caminhoImagem)

    update_lorentz(chaveHash)

    matrizAzul, matrizVerde, matrizVermelha  = decompose_matrix(caminhoImagem)
    matrizAzulCodificada ,matrizVerdeCodificada,matrizVermelhaCodificada = dna_encode(matrizAzul, matrizVerde,matrizVermelha)
    matrizK = key_matrix_encode(chaveHash, matrizAzul)
    matrizAzulFinal, matrizVerdeFinal, matrizVermelhaFinal = xor_operation(matrizAzulCodificada,matrizVerdeCodificada,matrizVermelhaCodificada,matrizK)
    x,y,z = gen_chaos_seq(larguraImagem, alturaImagem)

    fx,fy,fz = sequence_indexing(x,y,z)

    matrizAzulEmbaralhada, matrizVerdeEmbaralhada, matrizVermelhaEmbaralhada = scramble(fx,fy,fz,matrizAzulFinal, matrizVerdeFinal, matrizVermelhaFinal)

    r,g,b=dna_decode(matrizVermelhaEmbaralhada,matrizVerdeEmbaralhada,matrizAzulEmbaralhada)
    img=recover_image(r, g, b,caminhoImagem)
