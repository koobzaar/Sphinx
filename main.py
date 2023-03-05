from functions.ncamap import *
epsilon = 0.5

def f(x, ncamapFunc):
    return (1-epsilon*ncamapFunc(x))+(epsilon*(ncamapFunc(x+1)+ncamapFunc(x-1)))/2