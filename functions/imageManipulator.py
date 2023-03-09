import tkinter as tk
from tkinter import filedialog
import cv2
import time

def importarImagem():
    return filedialog.askopenfilename()    

def recover_image(r, g, b, iname):
    img = cv2.imread(iname)
    img[:,:,2] = r
    img[:,:,1] = g
    img[:,:,0] = b
    cv2.imwrite(("./"+str( time.time() )+ ".jpg"), img)
    print("[SUCESSO] Imagem encriptada com sucesso.")
    return img