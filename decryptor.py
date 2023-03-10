import cv2
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import sys
from importlib import reload  
    
from functions.generateSecureKey import *
from functions.matrixManipulator import *
from functions.imageManipulator import *
from functions.lorenzAttractor import *
from functions.matrixDNAManipulator import *
from functions.matrixManipulator import *
from functions.console import *

def decrypt():
    cls()
    showASCIIartHeader()
    caminhoImagem = select_image_path()
    chaveHash = input("Digite a chave de hash utilizada para encriptar a imagem: ")
    update_lorentz(chaveHash) 
    img = cv2.imread(caminhoImagem)
    r,g,b=split_into_rgb_channels(img)
    p, q = r.shape
    x,y,z = gen_chaos_seq(p, q)
    fx,fy,fz = sequence_indexing(x,y,z)
    Mk = key_matrix_encode(chaveHash, b )
    benc,genc,renc=dna_encode(b,g,r)
    bs,gs,rs=scramble_new(fx,fy,fz,benc,genc,renc)
    bx,rx,gx=xor_operation_new(bs,gs,rs,Mk)
    blue,green,red=dna_decode(bx,gx,rx)
    save_decrypted_image(blue,green,red, p, q, caminhoImagem)   

decrypt()