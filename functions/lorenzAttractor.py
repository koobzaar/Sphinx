import textwrap
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from bisect import bisect_left as bsearch
from tqdm import tqdm
a, b, c = 10, 2.667, 28
x0, y0, z0 = 0, 0, 0
tmax, N = 100, 10000

def lorenz(X, t, a, b, c):
    x, y, z = X
    x_dot = -a*(x - y)
    y_dot = c*x - y - x*z
    z_dot = -b*z + x*y
    return x_dot, y_dot, z_dot

def update_lorentz (key):
    key_bin = bin(int(key, 16))[2:].zfill(256)  #covert hex key digest to binary
    k={}                                        #key dictionary
    key_32_parts=textwrap.wrap(key_bin, 8)      #slicing key into 8 parts
    num=1
    for i in key_32_parts:
        k["k{0}".format(num)]=i
        num = num + 1
    t1 = t2 = t3 = 0
    for i in range (1,12):
        t1=t1^int(k["k{0}".format(i)],2)
    for i in range (12,23):
        t2=t2^int(k["k{0}".format(i)],2)
    for i in range (23,33):
        t3=t3^int(k["k{0}".format(i)],2)   
    global x0 ,y0, z0
    x0=x0 + t1/256            
    y0=y0 + t2/256            
    z0=z0 + t3/256   

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
    for k1 in tqdm(range(0,n), desc="────█ Indexando sequencia de Lorenz para x..."):
            t = x[k1]
            k2 = bsearch(seq, t)
            fx[k1]=k2
    seq=sorted(y)
    for k1 in tqdm(range(0,n), desc="────█ Indexando sequencia de Lorenz para y..."):
            t = y[k1]
            k2 = bsearch(seq, t)
            fy[k1]=k2
    seq=sorted(z)
    for k1 in tqdm(range(0,n), desc="────█ Indexando sequencia de Lorenz para z..."):
            t = z[k1]
            k2 = bsearch(seq, t)
            fz[k1]=k2
    return fx,fy,fz
def plot(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    s = 100
    c = np.linspace(0,1,N)
    for i in range(0,N-s,s):
        ax.plot(x[i:i+s+1], y[i:i+s+1], z[i:i+s+1], color=(1-c[i],c[i],1), alpha=0.4)
    ax.set_axis_off()
    plt.show()