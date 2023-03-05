from functions.ncamap import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt


epsilon = 0.1
alpha = 0.5
beta = 20
length = 600
iterations = 600

nca_map = NCA_Map(alpha, beta)

xn = np.random.uniform(0, 1, size=length)

for i in range(iterations):
    xn_new = np.empty_like(xn)
    for j in range(length):
        xn_i_plus_1 = xn[(j + 1) % length]
        xn_i_minus_1 = xn[(j - 1) % length]
        xn_new[j] = (1 - epsilon) * nca_map.map(xn[j]) + epsilon * (nca_map.map(xn_i_plus_1) + nca_map.map(xn_i_minus_1)) / 2
    xn = xn_new
plt.plot(range(length), xn)
plt.xlabel('Lattice site')
plt.ylabel('Value')
plt.title('Time evolution of the CML')
plt.show()