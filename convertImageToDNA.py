from abc import ABC, abstractmethod
import matplotlib.image as img
import numpy as np
class BaseNitrogenada(ABC):
    @abstractmethod
    def getBase(self, par):
        pass

class BasesNitrogenadas(BaseNitrogenada):
    def getBase(self, binario):
        bases_nitrogenadas = {"00": "A", "01": "C", "10": "T", "11": "G"}
        base_nitrogenada = []
        for i in range(0, len(binario), 2):
            par = binario[i:i+2]
            base_nitrogenada.append(bases_nitrogenadas[par])
        return base_nitrogenada

class ConversorBinario(ABC):
    @abstractmethod
    def converter(self, numero):
        pass

class ConversorBinarioPadrao(ConversorBinario):
    def converter(self, numero):
        return '{:0>8}'.format(str(bin(numero))[2:])

class Imagem(ABC):
    @abstractmethod
    def lerImagem(self, caminho):
        pass

    @abstractmethod
    def criarMatrizNitrogenada(self, imagem):
        pass

class ImagemPadrao(Imagem):
    def lerImagem(self, caminho):
        return img.imread(caminho)
    def matriz_para_vetor(matriz):
    # Use o NumPy para criar um vetor a partir da matriz
        vetor = np.array(matriz).reshape(-1)
        return vetor

    def criarMatrizNitrogenada(self, imagem):
        bases_nitrogenadas = BasesNitrogenadas()
        conversor_binario = ConversorBinarioPadrao()
        matriz_r = []
        matriz_g = []
        matriz_b = []
        for i in range(len(imagem)):
            linha_r = []
            linha_g = []
            linha_b = []
            for j in range(len(imagem[i])):
                r, g, b = imagem[i][j]
                r_binario = conversor_binario.converter(r)
                g_binario = conversor_binario.converter(g)
                b_binario = conversor_binario.converter(b)
                r_base = bases_nitrogenadas.getBase(r_binario)
                g_base = bases_nitrogenadas.getBase(g_binario)
                b_base = bases_nitrogenadas.getBase(b_binario)
                linha_r.append(r_base)
                linha_g.append(g_base)
                linha_b.append(b_base)
            matriz_r.append(linha_r)
            matriz_g.append(linha_g)
            matriz_b.append(linha_b)
        vetor_r = ImagemPadrao.matriz_para_vetor(matriz_r)
        vetor_g = ImagemPadrao.matriz_para_vetor(matriz_g)
        vetor_b = ImagemPadrao.matriz_para_vetor(matriz_b)
        return vetor_r, vetor_g, vetor_b

