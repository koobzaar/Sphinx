import numpy as np
import matplotlib.image as img
import hashlib
import cv2
from scipy.integrate import odeint
from bisect import bisect_left as bsearch
from PIL import Image
dna = {'00': 'A', '01': 'T', '10': 'G', '11': 'C', 'A': [0, 0], 'T': [0, 1], 'G': [1, 0], 'C': [1, 1], 'AA': 'A', 'TT': 'A', 'GG': 'A', 'CC': 'A', 'AG': 'G', 'GA': 'G', 'TC': 'G', 'CT': 'G', 'AC': 'C', 'CA': 'C', 'GT': 'C', 'TG': 'C', 'AT': 'T', 'TA': 'T', 'CG': 'T', 'GC': 'T'}
tmax, N = 100, 10000
def carregaImagemEmMatriz(caminho):
    imagem = img.imread(caminho)
    return imagem

def separaMatrizEmCanais(matriz):
    red = matriz[:,:,2]
    green = matriz[:,:,1]
    blue = matriz[:,:,0]
    return red, green, blue

def converteDecimalParaBinario(numero):
        return '{:0>8}'.format(str(bin(numero))[2:])

def convert_to_binary_matrices(r, g, b):
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)

    M, N = r.shape
    A = np.zeros((M, 8*N), dtype=np.int8)
    B = np.zeros((M, 8*N), dtype=np.int8)
    C = np.zeros((M, 8*N), dtype=np.int8)

    for i in range(M):
        for j in range(N):
            r_binary = np.binary_repr(r[i,j], width=8)
            g_binary = np.binary_repr(g[i,j], width=8)
            b_binary = np.binary_repr(b[i,j], width=8)
            for k in range(8):
                A[i, j*8+k] = int(r_binary[k])
                B[i, j*8+k] = int(g_binary[k])
                C[i, j*8+k] = int(b_binary[k])

    return A, B, C

def join_elements(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        row = []
        for j in range(0, len(matrix[i]), 2):
            pair = (matrix[i][j], matrix[i][j+1])
            row.append(pair)
        new_matrix.append(row)
    return new_matrix

def transformaParBinarioEmDNA(matriz):
    matrizDNA = [[0 for _ in range(len(matriz[0]))] for _ in range(len(matriz))]
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == (0, 0):
                matrizDNA[i][j] = "A"
            elif matriz[i][j] == (0, 1):
                matrizDNA[i][j] = "T"
            elif matriz[i][j] == (1, 0):
                matrizDNA[i][j] = "C"
            elif matriz[i][j] == (1, 1):
                matrizDNA[i][j] = "G"
    return matrizDNA


def key_matrix_encode(key,b):
    b = np.unpackbits(b,axis=1)
    m,n = b.shape
    key_bin = bin(int(key, 16))[2:].zfill(256)
    Mk = np.zeros((m,n),dtype=np.uint8)
    x=0
    for j in range(0,m):
            for i in range(0,n):
                Mk[j,i]=key_bin[x%256]
                x+=1
    
    Mk_enc=np.chararray((m,int(n/2)))
    idx=0
    for j in range(0,m):
        for i in range(0,n,2):
            if idx==(n/2):
                idx=0
            Mk_enc[j,idx]=dna["{0}{1}".format(Mk[j,i],Mk[j,i+1])]
            idx+=1
    Mk_enc=Mk_enc.astype(str)
    return Mk_enc

def xor_operation(r,g,b,mk):
    print(r)
    m,n = [len(b),len(b[0])]
    bx=np.chararray((m,n))
    gx=np.chararray((m,n))
    rx=np.chararray((m,n))
    b=b.array(b,)
    g=g.array(str)
    r=r.array(str)
    for i in range(0,m):
        for j in range (0,n):
            bx[i,j] = dna["{0}{1}".format(b[i,j],mk[i,j])]
            gx[i,j] = dna["{0}{1}".format(g[i,j],mk[i,j])]
            rx[i,j] = dna["{0}{1}".format(r[i,j],mk[i,j])]
         
    bx=bx.astype(str)
    gx=gx.astype(str)
    rx=rx.astype(str)
    return rx,gx,bx 

def lorenz(X, t, a, b, c):
    x, y, z = X
    x_dot = -a*(x - y)
    y_dot = c*x - y - x*z
    z_dot = -b*z + x*y
    return x_dot, y_dot, z_dot

def gen_chaos_seq(m,n):
    global x0,y0,z0,a,b,c,N
    N=m*n*4
    x= np.array((m,n*4))
    y= np.array((m,n*4))
    z= np.array((m,n*4))
    t = np.linspace(0, tmax, N)
    f = odeint(lorenz, (x0, y0, z0), t, args=(a, b, c))
    x, y, z = f.T
    x=x[:(N)]
    y=y[:(N)]
    z=z[:(N)]
    return x,y,z

def sequence_indexing(x,y,z):
    n=len(x)
    fx=np.zeros((n),dtype=np.uint32)
    fy=np.zeros((n),dtype=np.uint32)
    fz=np.zeros((n),dtype=np.uint32)
    seq=sorted(x)
    for k1 in range(0,n):
            t = x[k1]
            k2 = bsearch(seq, t)
            fx[k1]=k2
    seq=sorted(y)
    for k1 in range(0,n):
            t = y[k1]
            k2 = bsearch(seq, t)
            fy[k1]=k2
    seq=sorted(z)
    for k1 in range(0,n):
            t = z[k1]
            k2 = bsearch(seq, t)
            fz[k1]=k2
    return fx,fy,fz

def scramble(fx,fy,fz,r,g,b):
    p,q=b.shape
    size = p*q
    bx=b.reshape(size).astype(str)
    gx=g.reshape(size).astype(str)
    rx=r.reshape(size).astype(str)
    bx_s=np.chararray((size))
    gx_s=np.chararray((size))
    rx_s=np.chararray((size))

    for i in range(size):
            idx = fz[i]
            bx_s[i] = bx[idx]
    for i in range(size):
            idx = fy[i]
            gx_s[i] = gx[idx]
    for i in range(size):
            idx = fx[i]
            rx_s[i] = rx[idx]     
    bx_s=bx_s.astype(str)
    gx_s=gx_s.astype(str)
    rx_s=rx_s.astype(str)
    
    b_s=np.chararray((p,q))
    g_s=np.chararray((p,q))
    r_s=np.chararray((p,q))

    b_s=bx_s.reshape(p,q)
    g_s=gx_s.reshape(p,q)
    r_s=rx_s.reshape(p,q)
    return r_s,g_s,b_s

def dna_decode(r,g,b):
    m,n = b.shape
    r_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    g_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    b_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
    for color,dec in zip((b,g,r),(b_dec,g_dec,r_dec)):
        for j in range(0,m):
            for i in range(0,n):
                dec[j,2*i]=dna["{0}".format(color[j,i])][0]
                dec[j,2*i+1]=dna["{0}".format(color[j,i])][1]
    b_dec=(np.packbits(b_dec,axis=-1))
    g_dec=(np.packbits(g_dec,axis=-1))
    r_dec=(np.packbits(r_dec,axis=-1))
    return b_dec,g_dec,r_dec

def recover_image(r,g,b,iname):
    img = cv2.imread(iname)
    img[:,:,2] = r
    img[:,:,1] = g
    img[:,:,0] = b
    cv2.imwrite(("enc.jpg"), img)
    return img



def processaImagem(caminho):
    matriz = carregaImagemEmMatriz(caminho)
    # splits the plain-image into the red, green, blue components
    matrizSomenteVermelho, matrizSomenteVerde, matrizSomenteAzul = separaMatrizEmCanais(matriz)
    # Convert the matrices 𝑅, 𝐺 and 𝐵 into three binary matrices 𝑅̃, 𝐺̃ and 𝐵̃ with size 𝑀 × 8𝑁, respectively.
    matrizBinariaVermelho, matrizBinariaVerde, matrizBinariaAzul = convert_to_binary_matrices(matrizSomenteVermelho, matrizSomenteVerde, matrizSomenteAzul)
    # Convert the binary matrices 𝑅̃, 𝐺̃ and 𝐵̃ into three DNA sequences 𝑅̃̃, 𝐺̃̃ and 𝐵̃̃ with size 𝑀 × 4𝑁, respectively.
    matrizParBinarioR = join_elements(matrizBinariaVermelho)
    matrizParBinarioG = join_elements(matrizBinariaVerde)
    matrizParBinarioB = join_elements(matrizBinariaAzul)
    # Convert the binary pairs 𝑅̃̃, 𝐺̃̃ and 𝐵̃̃  into DNA sequences 𝑅̃̃̃, 𝐺̃̃̃ and 𝐵̃̃̃, respectively.
    matrizDNAVermelho = transformaParBinarioEmDNA(matrizParBinarioR)
    matrizDNAVerde = transformaParBinarioEmDNA(matrizParBinarioG)
    matrizDNAAzul = transformaParBinarioEmDNA(matrizParBinarioB)
    encodedMatrixR =  key_matrix_encode(getInicialConditionsForChaoticFunction("./image.jpg", "senha123"), matrizSomenteVermelho)
    
    matrizFinalVermelha, matrizFinalVerde, matrizFinalAzul = xor_operation(matrizDNAVermelho, matrizDNAVerde, matrizDNAAzul, encodedMatrixR)
    x, y, z = gen_chaos_seq(len(matriz),len(matriz[0]))
    fx, fy, fz = sequence_indexing(x,y,z)
    matrizVermelhaEmbaralhada, matrizVerdeEmbaralhada, matrizAzulEmbaralhada = scramble(fx,fy,fz,matrizFinalVermelha, matrizFinalVerde, matrizFinalAzul)
    r, g, b = dna_decode(matrizVermelhaEmbaralhada, matrizVerdeEmbaralhada, matrizAzulEmbaralhada)
    recover_image(r,g,b,"./imagemEncriptada.jpg")


























def getInicialConditionsForChaoticFunction(imagePath, secretKey):
    with open(imagePath, "rb") as f:
        imageHash = hashlib.sha256(f.read()).hexdigest()
    secretKeyHash = hashlib.sha256(secretKey.encode('utf-8')).hexdigest()
    combined_hash = imageHash + secretKeyHash
    # hash combined hash
    combined_hash = hashlib.sha256(combined_hash.encode('utf-8')).hexdigest()
    return combined_hash

def chaotic_function(x, r):
    return r * x * (1 - x)

x0 = getInicialConditionsForChaoticFunction("./image.jpg", "senha123")
r = 3.9
processaImagem("./image.jpg")