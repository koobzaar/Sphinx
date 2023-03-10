import hashlib
from PIL import Image
import numpy as np
from tqdm import tqdm 

def logistic_map(x,r):
    return r*x*(1-x)

def securekey(iname):
    img = Image.open(iname)
    m, n = img.size
    pix = np.array(img) 

    x0 = 0.5 
    r = 3.9 

    random_seq = [] 

    for i in tqdm(range(m*n*3), desc="──█ Gerando a chave hash utilizando os pixels originais da imagem e um mapa logistico..."): 
        x0 = logistic_map(x0,r) 
        random_seq.append(int(x0*255)) 

    random_seq = np.array(random_seq).reshape(m,n,3) 

    encrypted_img = pix ^ random_seq 

    key = hashlib.sha256() 
    key.update(encrypted_img) 
    return key.hexdigest(), m, n 