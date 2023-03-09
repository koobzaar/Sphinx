from functions.imageManipulator import importarImagem, recover_image
from functions.generateSecureKey import securekey
from functions.lorenzAttractor import update_lorentz, gen_chaos_seq, sequence_indexing
from functions.matrixManipulator import decompose_matrix, decompose_matrix, scramble
from functions.matrixDNAManipulator import dna_encode, key_matrix_encode, xor_operation, dna_decode

if (__name__ == "__main__"):
    caminhoImagem = importarImagem()

    chaveHash, larguraImagem, alturaImagem =  securekey(caminhoImagem)

    update_lorentz(chaveHash)

    matrizAzul, matrizVerde, matrizVermelha  = decompose_matrix(caminhoImagem)
    print(matrizAzul)
    matrizAzulCodificada ,matrizVerdeCodificada,matrizVermelhaCodificada = dna_encode(matrizAzul, matrizVerde,matrizVermelha)
    print(matrizAzulCodificada)
    matrizK = key_matrix_encode(chaveHash, matrizAzul)
    print(matrizK)
    matrizAzulFinal, matrizVerdeFinal, matrizVermelhaFinal = xor_operation(matrizAzulCodificada,matrizVerdeCodificada,matrizVermelhaCodificada,matrizK)
    print(matrizAzulFinal)
    x,y,z = gen_chaos_seq(larguraImagem, alturaImagem)

    fx,fy,fz = sequence_indexing(x,y,z)

    matrizAzulEmbaralhada, matrizVerdeEmbaralhada, matrizVermelhaEmbaralhada = scramble(fx,fy,fz,matrizAzulFinal, matrizVerdeFinal, matrizVermelhaFinal)

    r,g,b=dna_decode(matrizVermelhaEmbaralhada,matrizVerdeEmbaralhada,matrizAzulEmbaralhada)
    print(r)
    img=recover_image(r, g, b,caminhoImagem)
