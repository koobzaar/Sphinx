import numpy as np
from tqdm import tqdm

class DnaEncoder:
    def __init__(self):
        self.dna = {
            "00": "A",
            "01": "T",
            "10": "G",
            "11": "C",
            "A": [0, 0],
            "T": [0, 1],
            "G": [1, 0],
            "C": [1, 1],
            "AA": "A",
            "TT": "A",
            "GG": "A",
            "CC": "A",
            "AG": "G",
            "GA": "G",
            "TC": "G",
            "CT": "G",
            "AC": "C",
            "CA": "C",
            "GT": "C",
            "TG": "C",
            "AT": "T",
            "TA": "T",
            "CG": "T",
            "GC": "T"
        }

    def encode(self, blue_matrix, green_matrix, red_matrix):
            red_matrix = np.unpackbits(red_matrix, axis=1)
            green_matrix = np.unpackbits(green_matrix, axis=1)
            blue_matrix = np.unpackbits(blue_matrix, axis=1)
            m, n = red_matrix.shape
            encoded_red_matrix = np.chararray((m, int(n/2)))
            encoded_green_matrix = np.chararray((m, int(n/2)))
            encoded_blue_matrix = np.chararray((m, int(n/2)))
            matrix_names = ["red", "green", "blue"]
            for color, encoded, matrix_name in zip((red_matrix, green_matrix, blue_matrix), 
                                                   (encoded_red_matrix, encoded_green_matrix, encoded_blue_matrix),
                                                   matrix_names):
                idx = 0
                for j in tqdm(range(0, m), desc=f"Encoding {matrix_name} matrix into nucleotides..."):
                    for i in range(0, n, 2):
                        encoded[j, idx] = self.dna[f"{color[j, i]}{color[j, i+1]}"]
                        idx += 1
                        if i == n-2:
                            idx = 0
                            break
            
            encoded_red_matrix = encoded_red_matrix.astype(str)
            encoded_green_matrix = encoded_green_matrix.astype(str)
            encoded_blue_matrix = encoded_blue_matrix.astype(str)
            return encoded_red_matrix, encoded_green_matrix, encoded_blue_matrix


class KeyMatrixEncoder:
    def __init__(self):
        self.dna = {
            "00": "A",
            "01": "T",
            "10": "G",
            "11": "C",
            "A": [0, 0],
            "T": [0, 1],
            "G": [1, 0],
            "C": [1, 1]
        }

    def encode(self, key, matrix):
        matrix = np.unpackbits(matrix, axis=1)
        m, n = matrix.shape
        key_bin = bin(int(key, 16))[2:].zfill(256)
        Mk = np.zeros((m, n), dtype=np.uint8)
        x = 0
        for j in tqdm(range(0, m), desc="Using a hash key to generate a binary matrix Mk..."):
            for i in range(0, n):
                Mk[j, i] = key_bin[x % 256]
                x += 1

        Mk_enc = np.chararray((m, int(n/2)))
        idx = 0
        for j in tqdm(range(0, m), desc="Encoding the binary matrix Mk into nucleotides..."):
            for i in range(0, n, 2):
                if idx == (n/2):
                    idx = 0
                Mk_enc[j, idx] = self.dna["{0}{1}".format(Mk[j, i], Mk[j, i+1])]
                idx += 1
        Mk_enc = Mk_enc.astype(str)
        return Mk_enc


class XorOperation:
    def __init__(self):
        self.dna = {
            "00": "A",
            "01": "T",
            "10": "G",
            "11": "C",
            "A": [0, 0],
            "T": [0, 1],
            "G": [1, 0],
            "C": [1, 1],
            "AA": "A",
            "TT": "A",
            "GG": "A",
            "CC": "A",
            "AG": "G",
            "GA": "G",
            "TC": "G",
            "CT": "G",
            "AC": "C",
            "CA": "C",
            "GT": "C",
            "TG": "C",
            "AT": "T",
            "TA": "T",
            "CG": "T",
            "GC": "T"
        }

    def apply(self, b, g, r, mk):
        m,n = b.shape
        bx=np.chararray((m,n))
        gx=np.chararray((m,n))
        rx=np.chararray((m,n))
        b=b.astype(str)
        g=g.astype(str)
        r=r.astype(str)
        for i in tqdm(range(0,m), desc="────█ Applying XOR to the R, G, and B matrices..."):
            for j in range (0,n):
                bx[i,j] = self.dna["{0}{1}".format(b[i,j],mk[i,j])]
                gx[i,j] = self.dna["{0}{1}".format(g[i,j],mk[i,j])]
                rx[i,j] = self.dna["{0}{1}".format(r[i,j],mk[i,j])]
            
        bx=bx.astype(str)
        gx=gx.astype(str)
        rx=rx.astype(str)
        return bx,gx,rx 


class DnaDecoder:
    def __init__(self):
        self.dna = {
            "00": "A",
            "01": "T",
            "10": "G",
            "11": "C",
            "A": [0, 0],
            "T": [0, 1],
            "G": [1, 0],
            "C": [1, 1]
        }

    def decode(self, b, g, r):
        m,n = b.shape
        r_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
        g_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)
        b_dec= np.ndarray((m,int(n*2)),dtype=np.uint8)

        for color,dec in zip((b,g,r),(b_dec,g_dec,r_dec)):
            for j in tqdm(range(0,m),desc="────█ Decoding nucleotides..."):
                for i in range(0,n):
                    dec[j,2*i]=self.dna["{0}".format(color[j,i])][0]
                    dec[j,2*i+1]=self.dna["{0}".format(color[j,i])][1]

        b_dec=(np.packbits(b_dec,axis=-1))
        g_dec=(np.packbits(g_dec,axis=-1))
        r_dec=(np.packbits(r_dec,axis=-1))
        return b_dec,g_dec,r_dec