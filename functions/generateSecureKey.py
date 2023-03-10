from PIL import Image
import hashlib
from tqdm import tqdm

def securekey(iname):
    img = Image.open(iname)
    m, n = img.size
    pix = img.load()          
    plainimage = []
    for y in tqdm(range(n), desc="──█ Gerando chave hash..."):
        for x in range(m):
            for k in range(0, 3):
                plainimage.append(pix[x,y][k])    
    key = hashlib.sha256()
    key.update(bytearray(plainimage))
    return key.hexdigest(), m, n
