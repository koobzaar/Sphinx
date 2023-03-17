

<img src="https://i.imgur.com/WKgapd6.jpg">
<img src="https://img.shields.io/github/last-commit/koobzaar/sphinx?style=for-the-badge">
<img src="https://img.shields.io/github/languages/code-size/koobzaar/sphinx?style=for-the-badge">
<img src="https://i.imgur.com/s1vbBhe.png" align="right"
     alt="Size Limit logo by Anton Lovchikov" width="250" height="148">

Sphinx é um **crypter de imagens coloridas**. Esse método utiliza o **atractor de Lorenz**, que é um **sistema dinâmico não linear** que descreve o comportamento do movimento de fluidos e gases, e as **bases nitrogenadas**, que são moléculas presentes no **DNA** e **RNA**. Ao combinar esses elementos, o Sphinx é capaz de transformar imagens em um formato codificado que só pode ser decifrado com a utilização da chave **RSA** correta. 

**[INFO]** O atractor que está disponível à direita deste readme foi criado utilizando as coordenadas `x`, `y` e `z` geradas para encriptar a imagem `1477351899v6iQb.jpg`. Esse atractor é **ÚNICO** para essa imagem.


<img src="https://i.imgur.com/gEuO1gw.jpg" alt="Size Limit logo by Anton Lovchikov" width="100%">


Algumas **características** de sistemas dinâmicos caóticos, principalmente o **Atractor de Lorenz**, são:

- **Sensibilidade às condições iniciais**: *pequenas variações* nas condições iniciais podem levar a grandes diferenças nos resultados.
- **Ciclos atratores**: os sistemas caóticos podem apresentar ciclos atratores complexos, muitas vezes fractais, que podem ser difíceis de prever ou entender.    
- **Não periódicos**: ao contrário dos sistemas periódicos, os sistemas caóticos não apresentam padrões repetitivos ou previsíveis.
    
- **Dinâmica caótica**: os sistemas caóticos são caracterizados por uma dinâmica complexa e não linear, que pode ser difícil de modelar ou entender matematicamente.

## Bases nitrogenadas

<img src="https://upload.wikimedia.org/wikipedia/commons/1/16/DNA_orbit_animated.gif" align="left"
     alt="Size Limit logo by Anton Lovchikov" width="70" height="108">

As **nucleobases**, também conhecidas como **bases nitrogenadas** ou **simplesmente bases**, são compostos biológicos que contêm nitrogênio e formam nucleosídeos, que, por sua vez, são componentes de nucleotídeos. 
Todos esses monômeros constituem os blocos **básicos de construção dos ácidos nucleicos.** A capacidade das nucleobases de formar pares de base e empilhar uma sobre a outra leva diretamente à formação de estruturas helicoidais de cadeia longa, como o ácido ribonucleico (RNA) e o ácido desoxirribonucleico (DNA). Cinco nucleobases - adenina (A), citosina (C), guanina (G), timina (T) e uracila (U) - são chamadas de primárias ou canônicas.

## Como e por que utilizar bases nitrogenadas?
### Por quê?
O motivo para usar DNA para encriptar uma imagem é devido às propriedades únicas da Computação em DNA, tais como a **densidade de informação extraordinária**, o paralelismo maciço e o **consumo ultra baixo de energia**. Essas características permitem que o DNA seja usado como um meio para codificar e processar informações de forma **altamente eficiente e segura**. Além disso, a combinação de codificação de DNA com sistemas caóticos permite a criação de algoritmos de criptografia de imagem mais eficientes e seguros, já que a natureza **imprevisível** e aleatória dos sistemas caóticos pode ser utilizada para gerar chaves de criptografia mais robustas.
### Como?
Primeiro, é necessário transformar **cada valor de pixel RGB em binário**. 
O processo de transformar valores RGB em binário é relativamente simples. Primeiramente, deve-se **converter cada valor RGB individualmente em binário**, o que resulta em **três sequências binárias de 8 bits cada**. Por exemplo, o valor **RGB (143, 234, 97)** seria convertido em binário como **(10001111, 11101010, 01100001**).

Em seguida, para assimilar esses valores binários a uma base nitrogenada, é preciso agrupar os **8 bits de cada valor RGB em grupos de 2 bits**. Isso resulta em **quatro grupos de 2 bits para cada valor RGB**.

Assim, o valor RGB (143, 234, 97) seria agrupado da seguinte forma:

- **10001111** seria dividido em **4 grupos de 2 bits**: **10 00 11 11**
- **11101010** seria dividido em **4 grupos de 2 bits**: **11 10 10 10**
- **01100001** seria dividido em **4 grupos de 2 bits**: **01 10 00 01**

A partir desses grupos de 2 bits, é possível **assimilar cada grupo a uma das quatro bases nitrogenadas**, sendo elas: Adenina ( A ), Timina ( T ), Citosina ( C ) e Guanina ( G ).

Assim, considerando o binário **10001101** (10 00 11 01)
- o grupo **10 seria assimilado à base A**
- o grupo **00 seria assimilado à base T**
- o grupo **11 seria assimilado à base C**
- o grupo **01 seria assimilado à base G**

Com isso, **teríamos a sequência de bases nitrogenadas correspondentes ao valor RGB (143, 234, 97).** 
- 143 = 10001111 = 10 00 11 11 = A T C C = ATCC
- 234 = 11101010 = 11 10 10 10 = C A A A = CAAA
- 97 = 01100001 = 01 10 00 01 = G A T G = GATG

**RGB (ATCC, CAAA, GATG).**

## Instalação e uso
- Clone os arquivos deste repositório para uma pasta em seu computador

*Em seu terminal, utilize o seguinte comando para clonar os arquivos deste repositório:*
```bash
git clone https://github.com/koobzaar/Sphinx.git
```
-  Instale os requirements para obter todas as dependências do projeto.

*Na pasta do projeto, execute o seguinte comando para instalar as dependências:*
```bash
pip install -r requirements.txt
```
### Encriptar uma imagem
-  Rode o arquivo `encr.py` para encriptar uma imagem qualquer.
```bash
python encrypt.py
```
Será aberto seu revelador de arquivos para você selecionar a imagem que você deseja encriptar.
Após selecionar e abrir a imagem, o processo de encriptação será iniciado. Sua imagem encriptada pode ser encontrada posteriormente na pasta `./encrypted_output`.

**[ATENÇÃO]** Quando acabar a encriptação, será gerado uma chave Hash. Essa chave Hash é NECESSÁRIA para decriptar a imagem posteriormente.

### Decriptar uma imagem
O processo de decriptar é praticamente igual ao de encriptar. Importe a imagem encriptada e insira a chave hash no terminal. A diferença é que você deve usar o decrypt.py:
```bash
python decrypt.py
```

# Créditos
The author of this project is **Bruno Bezerra Trigueiro**, currently affiliated with the **São Paulo State Technological College (FATEC)**. 
It's inspired by the following scientific publication:
https://www.sciencedirect.com/science/article/abs/pii/S0165168418300859

The author can be **contacted** through the email addresses [bruno.trigueiro@proton.me](mailto:bruno.trigueiro@proton.me) or [bruno.trigueiro@fatec.sp.gov.br](mailto:bruno.trigueiro@fatec.sp.gov.br).
Also, you can contact me at:
https://www.linkedin.com/in/brunotrigueiro/

 **Disclaimer:** 
 It is important to note that this project are of an academic nature and should not be interpreted as proven scientific facts.
 
