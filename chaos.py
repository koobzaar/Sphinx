import numpy as np
from convertImageToDNA import ImagemPadrao
#from convertImageToDNA import ImagemPadrao

imagem = ImagemPadrao()
image = imagem.lerImagem("./image.jpg")

[vetor_nitrogenada_r,vetor_nitrogenada_g,vetor_nitrogenada_b] = imagem.criarMatrizNitrogenada(image)

codes = {'G': 0, 'A': 1, 'T': 2, 'C': 3}
print(vetor_nitrogenada_r)
def retornaVetorCodificado(vetor_nitrogenado):
    vetor_codificado = []
    codes = {'G': 0, 'A': 1, 'T': 2, 'C': 3}
    for i in range(len(vetor_nitrogenado)):
        vetor_codificado.append(codes[vetor_nitrogenado[i]])
    return vetor_codificado

def chaotic_sort(seq, x0=0.41233114, r=3.9):
    n = len(seq) - 1
    chaos_seq = [x0]
    for i in range(n):
        x = logistic_map(chaos_seq[-1], r)
        chaos_seq.append(x)

    # Normalizar a sequência de valores caóticos
    normalized_seq = (chaos_seq - np.min(chaos_seq)) / (np.max(chaos_seq) - np.min(chaos_seq))

    # Ordenar a sequência de valores caóticos em ordem crescente
    sorted_seq = np.argsort(normalized_seq)

    # Permutar a sequência de números que representa a string "GATC"
    permuted_num_seq = [seq[i] for i in sorted_seq]

    # Converter de volta para as letras ATCG
    permuted_seq = []
    for num in permuted_num_seq:
        if num == 0:
            permuted_seq.append('G')
        elif num == 1:
            permuted_seq.append('A')
        elif num == 2:
            permuted_seq.append('T')
        elif num == 3:
            permuted_seq.append('C')

    return permuted_seq

def logistic_map(x, r):
    return r * x * (1 - x)



num_seq_r = retornaVetorCodificado(vetor_nitrogenada_r)
num_seq_g = retornaVetorCodificado(vetor_nitrogenada_g)
num_seq_b = retornaVetorCodificado(vetor_nitrogenada_b)

permuted_seq_r = chaotic_sort(num_seq_r)
permuted_seq_g = chaotic_sort(num_seq_g)
permuted_seq_b = chaotic_sort(num_seq_b)

