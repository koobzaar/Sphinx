import cv2
import numpy as np
from tqdm import tqdm

def split_into_rgb_channels(image):
  red = image[:,:,2]
  green = image[:,:,1]
  blue = image[:,:,0]
  return red, green, blue

def decompose_matrix(iname):
    image = cv2.imread(iname)
    blue,green,red = split_into_rgb_channels(image)
    for values, channel in zip((red, green, blue), (2,1,0)):
        img = np.zeros((values.shape[0], values.shape[1]), dtype = np.uint8)
        img[:,:] = (values)
        if channel == 0:
            B = np.asmatrix(img)
        elif channel == 1:
            G = np.asmatrix(img)
        else:
            R = np.asmatrix(img)
    return B,G,R

def scramble(fx, fy, fz, b, g, r, new_version):
    p, q = b.shape
    size = p * q
    bx, gx, rx, bx_s, gx_s, rx_s = b.reshape(size), g.reshape(size), r.reshape(size), b.reshape(size), g.reshape(size), r.reshape(size)
    bx, gx, rx, bx_s, gx_s, rx_s = bx.astype(str), gx.astype(str), rx.astype(str), bx_s.astype(str), gx_s.astype(str), rx_s.astype(str)
    if new_version:
        for i in tqdm(range(size), desc="────█ Desembaralhando a matriz vermelha..."):
            idx = fz[i]
            bx_s[idx] = bx[i]
        for i in tqdm(range(size), desc="────█ Desembaralhando a matriz verde..."):
            idx = fy[i]
            gx_s[idx] = gx[i]
        for i in tqdm(range(size), desc="────█ Desembaralhando a matriz azul..."):
            idx = fx[i]
            rx_s[idx] = rx[i]
    else:
        for i in tqdm(range(size), desc="────█ Shuffling red matrix..."):
            idx = fx[i]
            rx_s[i] = rx[idx]
        for i in tqdm(range(size), desc="────█ Shuffling green matrix..."):
            idx = fy[i]
            gx_s[i] = gx[idx]
        for i in tqdm(range(size), desc="────█ Shuffling blue matrix..."):
            idx = fz[i]
            bx_s[i] = bx[idx]

    b_s = np.chararray((p, q))
    g_s = np.chararray((p, q))
    r_s = np.chararray((p, q))

    b_s = bx_s.reshape(p, q)
    g_s = gx_s.reshape(p, q)
    r_s = rx_s.reshape(p, q)

    return b_s, g_s, r_s