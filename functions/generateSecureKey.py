from PIL import Image
import hashlib

class Hash:
    def gerarHash(self, caminhoImagem):
        matrizImagem = Image.open(caminhoImagem)
        larguraImagem, alturaImagem = matrizImagem.size
        pix = matrizImagem.load()          
        plainimage = list()
        for linha in range(alturaImagem):
            for coluna in range(larguraImagem):
                for valoresPixelRGB in range(0,3):
                    plainimage.append(pix[linha, coluna][valoresPixelRGB])

        chaveHash = self.geraChaveHash(plainimage)
        return larguraImagem, alturaImagem, chaveHash

    def geraChaveHash(self, matrizImagem):
        chaveHash = hashlib.sha256()
        chaveHash.update(bytearray(matrizImagem))
        return chaveHash.hexdigest()
