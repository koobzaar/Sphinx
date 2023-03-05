import numpy as np
from abc import ABC, abstractmethod

class NCA(ABC):
    @abstractmethod
    def map(self, x):
        pass

class NCA_Map(NCA):
    def __init__(self, alfa, beta):
        if alfa < 0 or alfa >= 1.4:
            raise ValueError("The value of alfa must be between 0 and 1.4")
        if alfa >= 1.4 and alfa < 1.5:
            if beta < 9 or beta > 38:
                raise ValueError("The value of beta must be between 9 and 38")
        elif alfa >= 1.5 and alfa < 1.57:
            if beta < 3 or beta > 15:
                raise ValueError("The value of beta must be between 3 and 15")
        elif alfa >= 1.57:
            raise ValueError("The value of alfa must be less than 1.57")
        else:
            if beta < 5 or beta > 43:
                raise ValueError("The value of beta must be between 5 and 43")

        self.alfa = alfa
        self.beta = beta

    def map(self, x):
        if x < 0 or x > 1:
            raise ValueError("O valor de x deve estar entre 0 e 1")
        return (1 - self.beta**(-4)) * (1/np.tan(self.alfa/(1 + self.beta))) * ((1 + 1/self.beta)**self.beta) * np.tan(self.alfa*x) * (1 - x)**self.beta


