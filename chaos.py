import numpy as np
from convertImageToDNA import ImagemPadrao
import matplotlib.pyplot as plt
#from convertImageToDNA import ImagemPadrao

imagem = ImagemPadrao()
image = imagem.lerImagem("./image.jpg")
print(len(image))
print(len(image[0]))
print(len(image[0][0]))
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

# Seguindo o seguinte dicionario, transforma cada base nitrogenada em binario:  {"00": "A", "01": "C", "10": "T", "11": "G"}
def retornaVetorBinario(vetor_nitrogenado):
    vetor_binario = []
    codes = {'G': '00', 'A': '01', 'T': '10', 'C': '11'}
    for i in range(len(vetor_nitrogenado)):
        vetor_binario.append(codes[vetor_nitrogenado[i]])
    return vetor_binario

# Agrupa a cada 4 bits 
def retornaVetorAgrupado(vetor_binario):
    vetor_agrupado = []
    for i in range(0,len(vetor_binario),4):
        vetor_agrupado.append(vetor_binario[i]+vetor_binario[i+1]+vetor_binario[i+2]+vetor_binario[i+3])
    return vetor_agrupado

# Transforma cada elemento do array em um inteiro
def retornaVetorInteiro(vetor_agrupado):
    vetor_inteiro = []
    for i in range(len(vetor_agrupado)):
        vetor_inteiro.append(int(vetor_agrupado[i],2))
    return vetor_inteiro

# Verifica se existe um valor do vetor maior que 255. Se existir, printa um erro
def verificaVetor(vetor_inteiro):
    for i in range(len(vetor_inteiro)):
        if vetor_inteiro[i] > 255:
            print("Erro")
            break
    return vetor_inteiro

vetor_binario_r = retornaVetorBinario(permuted_seq_r)
vetor_binario_g = retornaVetorBinario(permuted_seq_g)
vetor_binario_b = retornaVetorBinario(permuted_seq_b)
grouped_vector_r = retornaVetorAgrupado(vetor_binario_r)
grouped_vector_g = retornaVetorAgrupado(vetor_binario_g)
grouped_vector_b = retornaVetorAgrupado(vetor_binario_b)
integer_vector_r = retornaVetorInteiro(grouped_vector_r)
integer_vector_g = retornaVetorInteiro(grouped_vector_g)
integer_vector_b = retornaVetorInteiro(grouped_vector_b)
integer_vector_r = verificaVetor(integer_vector_r)
integer_vector_g = verificaVetor(integer_vector_g)
integer_vector_b = verificaVetor(integer_vector_b)

# Cria uma matriz com os valores do vetor de cada cor correspondente. A matriz deve ter as dimensoes originais
def retornaMatriz(vetor_r,vetor_g,vetor_b, width, height):
    matriz = []
    for i in range(height):
        matriz.append([])
        for j in range(width):
            matriz[i].append([vetor_r[i*width+j],vetor_g[i*width+j],vetor_b[i*width+j]])
    return matriz
   

matriz = retornaMatriz(integer_vector_r,integer_vector_g,integer_vector_b, len(image[0]), len(image))
print(len(matriz))
print(len(matriz[0]))
print(len(matriz[0][0]))

from PIL import Image

def exibir_imagem(matriz_pixels):
    # criar objeto de imagem a partir da matriz de pixels
    imagem = Image.fromarray(np.uint8(matriz_pixels))
    # armazena a imagem
    imagem.save('imagem.png')
    # exibir imagem
    imagem.show()
