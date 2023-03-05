import numpy as np
from abc import ABC, abstractmethod

class NCA(ABC):
    @abstractmethod
    def map(self, x):
        pass

class NCA_Map(NCA):
    def __init__(self, alfa, beta):
        if alfa <= 0 or alfa > 1.57:
            raise ValueError("O valor de alfa deve estar entre 0 e 1.57")
        if beta < 5 or beta > 43:
            raise ValueError("O valor de beta deve estar entre 5 e 43")
        self.alfa = alfa
        self.beta = beta

    def map(self, x):
        if x <= 0 or x >= 1:
            raise ValueError("O valor de x deve estar entre 0 e 1")
        return (1 - self.beta**(-4)) * (1/np.tan(self.alfa/(1 + self.beta))) * ((1 + 1/self.beta)**self.beta) * np.tan(self.alfa*x) * (1 - x)**self.beta


