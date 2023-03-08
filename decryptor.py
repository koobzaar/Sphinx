import numpy as np
from PIL import Image


def loadImage(path):
    img = Image.open(path)
    img_array = np.array(img)
    print(len(img_array))
    print(len(img_array[0]))
    return img_array

def converter(numero):
        return '{:0>8}'.format(str(bin(numero))[2:])

def getBase(matrizBinaria):
        bases_nitrogenadas = {"00": "A", "01": "C", "10": "T", "11": "G"}
        base_nitrogenada = []
        for i in range(0, len(matrizBinaria), 2):
            par = matrizBinaria[i:i+2]
            base_nitrogenada.append(bases_nitrogenadas[par])
        return base_nitrogenada

def criarMatrizNitrogenada(imagem):
        matriz_r = []
        matriz_g = []
        matriz_b = []
        for i in range(len(imagem)):
            linha_r = []
            linha_g = []
            linha_b = []
            for j in range(len(imagem[i])):
                r, g, b = imagem[i][j]
                r_binario = converter(r)
                g_binario = converter(g)
                b_binario = converter(b)
                r_base = getBase(r_binario)
                g_base = getBase(g_binario)
                b_base = getBase(b_binario)
                linha_r.append(r_base)
                linha_g.append(g_base)
                linha_b.append(b_base)
            matriz_r.append(linha_r)
            matriz_g.append(linha_g)
            matriz_b.append(linha_b)
        
        return matriz_r, matriz_g, matriz_b


def imageDecrypt(path):
    matrizImagem = loadImage(path)
    [matrizNitrogenadaR, matrizNitrogenadaG, matrizNitrogenadaB] = criarMatrizNitrogenada(matrizImagem)
    

imageDecrypt("./imagem3.png")
