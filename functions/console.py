import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def showASCIIartHeader():
    with open('./header', 'r') as f:
        header = f.read()
    print(header)