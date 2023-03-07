# Load the Python libraries
import numpy as np
import math
from collections import Counter
import numpy as np
# Load plotting libraries
import matplotlib.pyplot as plt
from PIL import Image
import colorsys
# This function gets a random number from a uniform distribution between the two input values [min_value, max_value] inclusively
def get_random_number(min_value, max_value):
    range = max_value - min_value
    num = np.random.uniform(0, 1)
    return min_value + range * num
# Function that creates a series of numbers using chaos theory
def get_chaos_list(seed, n):
    numList = []
    k = 3.9976543219876543210
    x = seed
    print(seed)
    
    for i in range(n):
        x = x * k * (1 - x)
        numList += [x]
    
    # Return x and y
    return np.arange(len(numList)), numList
# Function that plot a (x, y) series of points
def plot_line_chart(x, y, x_label, y_label, title):
    plt.figure(figsize = (16, 4))
    plt.plot(x, y, label = y_label)
    plt.xlabel(x_label, fontsize = 11)
    plt.ylabel(y_label, fontsize = 11)
    plt.title(title, size=14)
    plt.legend(loc = 'upper right')
    plt.show()

# Create and plot 100 random-chaos numbers
seed = get_random_number(0, 1)
x, y = get_chaos_list(seed, 100)
print (x, y)
#plot_line_chart(x, y, '$x$', '$chaos(x)$', 'Numbers created with the Chaos Function')

def g(x, alfa, beta): 
	return (1 - beta**(-4)) * (1/math.tan(alfa / (1 + beta))) * ((1 + 1 / beta)**beta) * math.tan(alfa * x) * (1 - x)**beta

import matplotlib.pyplot as plt

# Create an array of 1000 numbers between 0 and 1
x = np.linspace(0, 1, 1000)
alfa = 1.3
beta = 6
y = [g(i, alfa, beta) for i in x]

# Create a plot
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph of g(x)')
plt.show()




