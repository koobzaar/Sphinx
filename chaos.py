import numpy as np
#from convertImageToDNA import ImagemPadrao


# Codificar a string "GATC" em números
codes = {'G': 0, 'A': 1, 'T': 2, 'C': 3}
seq = 'CTAG'
num_seq = [codes[c] for c in seq]
print(num_seq)

# Gerar uma sequência de valores caóticos
def logistic_map(x, r):
    return r * x * (1 - x)

x0 = 0.43323124
r = 3.9
n = 3
chaos_seq = [x0]
for i in range(n):
    x = logistic_map(chaos_seq[-1], r)
    chaos_seq.append(x)
print(chaos_seq)

# Normalizar a sequência de valores caóticos
normalized_seq = (chaos_seq - np.min(chaos_seq)) / (np.max(chaos_seq) - np.min(chaos_seq))

# Ordenar a sequência de valores caóticos em ordem crescente
sorted_seq = np.argsort(normalized_seq)

# Permutar a sequência de números que representa a string "GATC"

permuted_num_seq = [num_seq[i] for i in sorted_seq]
permuted_seq = ''.join([k for k, v in codes.items() if v in permuted_num_seq])

print(seq)
print(permuted_seq)