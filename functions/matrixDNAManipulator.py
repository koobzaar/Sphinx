#DNA-Encoding RULE #1 A = 00, T=01, G=10, C=11
dna={}
dna["00"]="A"
dna["01"]="T"
dna["10"]="G"
dna["11"]="C"
dna["A"]=[0,0]
dna["T"]=[0,1]
dna["G"]=[1,0]
dna["C"]=[1,1]
#DNA xor
dna["AA"]=dna["TT"]=dna["GG"]=dna["CC"]="A"
dna["AG"]=dna["GA"]=dna["TC"]=dna["CT"]="G"
dna["AC"]=dna["CA"]=dna["GT"]=dna["TG"]="C"
dna["AT"]=dna["TA"]=dna["CG"]=dna["GC"]="T"
import numpy as np
from tqdm import tqdm
from typing import Tuple

def dna_encode(red_matrix, green_matrix, blue_matrix):
    red_matrix = np.unpackbits(red_matrix, axis=1)
    green_matrix = np.unpackbits(green_matrix, axis=1)
    blue_matrix = np.unpackbits(blue_matrix, axis=1)
    m, n = red_matrix.shape
    encoded_red = np.chararray((m, int(n/2)))
    encoded_green = np.chararray((m, int(n/2)))
    encoded_blue = np.chararray((m, int(n/2)))
    matrix_names = ["red", "green", "blue"]
    index = -1
    for color, encoded in zip((red_matrix, green_matrix, blue_matrix), 
                              (encoded_red, encoded_green, encoded_blue)):
        idx = 0
        index+=1
        for j in tqdm(range(0, m), desc="────█ Encoding "+matrix_names[index]+" matrix into nucleotides..."):
            for i in range(0, n, 2):
                encoded[j, idx] = dna["{0}{1}".format(color[j, i], color[j, i+1])]
                idx += 1
                if i == n-2:
                    idx = 0
                    break
    
    encoded_red = encoded_red.astype(str)
    encoded_green = encoded_green.astype(str)
    encoded_blue = encoded_blue.astype(str)
    return encoded_red, encoded_green, encoded_blue


def key_matrix_encode(key,b):
    b = np.unpackbits(b,axis=1)
    m,n = b.shape
    key_bin = bin(int(key, 16))[2:].zfill(256)
    Mk = np.zeros((m,n),dtype=np.uint8)
    x=0
    for j in tqdm(range(0,m), desc="──█ Usando a chave hash para gerar uma matriz binaria Mk..."):
            for i in range(0,n):
                Mk[j,i]=key_bin[x%256]
                x+=1
    
    Mk_enc=np.chararray((m,int(n/2)))
    idx=0
    for j in tqdm(range(0,m), desc="────█ Codificando a matriz binaria Mk em nucleotidios..."):
        for i in range(0,n,2):
            if idx==(n/2):
                idx=0
            Mk_enc[j,idx]=dna["{0}{1}".format(Mk[j,i],Mk[j,i+1])]
            idx+=1
    Mk_enc=Mk_enc.astype(str)
    return Mk_enc
def xor_operation(b,g,r,mk):
    m,n = b.shape
    bx=np.chararray((m,n))
    gx=np.chararray((m,n))
    rx=np.chararray((m,n))
    b=b.astype(str)
    g=g.astype(str)
    r=r.astype(str)
    for i in tqdm(range(0,m), desc="────█ Aplicando XOR nas matrizes R, G e B..."):
        for j in range (0,n):
            bx[i,j] = dna["{0}{1}".format(b[i,j],mk[i,j])]
            gx[i,j] = dna["{0}{1}".format(g[i,j],mk[i,j])]
            rx[i,j] = dna["{0}{1}".format(r[i,j],mk[i,j])]
         
    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    return bx,gx,rx 

def dna_decode(b,g,r):
    m,n = b.shape
    r_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    g_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    b_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    for color,dec in zip((b,g,r),(b_dec,g_dec,r_dec)):
        for j in tqdm(range(0,m),desc="────█ Decodificando nucleotidios..."):
            for i in range(0,n):
                dec[j,2*i]=dna["{0}".format(color[j,i])][0]
                dec[j,2*i+1]=dna["{0}".format(color[j,i])][1]
    b_dec=(np.packbits(b_dec,axis=-1))
    g_dec=(np.packbits(g_dec,axis=-1))
    r_dec=(np.packbits(r_dec,axis=-1))
    return b_dec,g_dec,r_dec

def xor_operation_new(b,g,r,mk):
    m,n = b.shape
    bx=np.chararray((m,n))
    gx=np.chararray((m,n))
    rx=np.chararray((m,n))
    b=b.astype(str)
    g=g.astype(str)
    r=r.astype(str)
    for i in tqdm(range(0,m), desc="────█ Aplicando XOR nas matrizes R, G e B..."):
        for j in range (0,n):
            bx[i,j] = dna["{0}{1}".format(b[i,j],mk[i,j])]
            gx[i,j] = dna["{0}{1}".format(g[i,j],mk[i,j])]
            rx[i,j] = dna["{0}{1}".format(r[i,j],mk[i,j])]
         
    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    return bx,gx,rx 