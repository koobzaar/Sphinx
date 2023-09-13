

<img src="https://i.imgur.com/WKgapd6.jpg">
<img src="https://img.shields.io/github/last-commit/koobzaar/sphinx?style=for-the-badge">
<img src="https://img.shields.io/github/languages/code-size/koobzaar/sphinx?style=for-the-badge">
<img src="https://i.imgur.com/s1vbBhe.png" align="right"
     alt="Size Limit logo by Anton Lovchikov" width="250" height="148">

Sphinx é uma demonstração de como usar **mapas caóticos e DNA** para encriptar arquivos de imagem. O objetivo é criar uma chave segura e aleatória que possa ser usada para cifrar e decifrar uma imagem usando uma operação XOR. A chave é gerada usando uma combinação do mapa logístico, um gerador de números aleatórios quânticos e o mapa de Lorenz. A chave é então codificada em uma sequência de nucleotídeos que representa DNA.

**[INFO]** O atractor que está disponível à direita deste readme foi criado utilizando as coordenadas `x`, `y` e `z` geradas para encriptar a imagem `1477351899v6iQb.jpg`. Esse atractor é **ÚNICO** para essa imagem.


<img src="https://i.imgur.com/gEuO1gw.jpg" alt="Size Limit logo by Anton Lovchikov" width="100%">


Algumas **características** de sistemas dinâmicos caóticos, principalmente o **Atractor de Lorenz**, são:

Algumas características desse método de criptografia são:

- **Mapas caóticos para gerar números aleatórios que são difíceis de prever ou reproduzir**: os mapas caóticos são funções matemáticas que produzem resultados imprevisíveis e sensíveis às condições iniciais. Um exemplo de mapa caótico é o mapa logístico, que é usado neste projeto.
- **Gerador de números aleatórios quânticos para adicionar mais entropia e segurança à chave**: o gerador de números aleatórios quânticos é um serviço online que fornece números aleatórios baseados em fenômenos quânticos, como o decaimento radioativo ou a polarização de fótons.
- **Attractor de Lorenz para aumentar a complexidade e a imprevisibilidade da chave**: o mapa de Lorenz é um sistema de equações diferenciais que descreve o comportamento caótico de um fluido. O mapa de Lorenz produz uma sequência de pontos que formam um padrão tridimensional chamado atrator de Lorenz.
- DNA como uma forma de codificar a chave em uma sequência de nucleotídeos.
  

## Metodologias

O projeto consiste em quatro módulos principais: `generateSecureKey.py`, `lorenzAttractor.py`, `matrixDNAManipulator.py` e `matrixManipulator.py`. Cada módulo contém várias funções e classes que são usadas para realizar as seguintes etapas:

- Gerar uma chave segura e aleatória usando o mapa logístico e um gerador de números aleatórios quânticos. O mapa logístico é uma função matemática que produz uma sequência de números aleatórios entre 0 e 1, dependendo dos parâmetros x e r. O gerador de números aleatórios quânticos é um serviço online que fornece números aleatórios baseados em fenômenos quânticos. A chave é formada pela concatenação dos números gerados pelo mapa logístico e pelo gerador quântico.
- Gerar uma sequência de pontos no mapa de Lorenz, que é um sistema de equações diferenciais que descreve o comportamento caótico de um fluido. O mapa de Lorenz é usado para adicionar mais complexidade e imprevisibilidade à chave. A sequência de pontos é obtida usando a função odeint da biblioteca scipy, que resolve numericamente as equações do mapa de Lorenz.
- Codificar a chave em uma sequência de nucleotídeos que representa DNA. Cada número da chave é convertido em um valor binário, que é então mapeado para um nucleotídeo (A, T, C ou G) usando um dicionário pré-definido. A sequência resultante é dividida em três matrizes, correspondendo aos canais vermelho, verde e azul do DNA.
- Encriptar uma imagem usando a chave codificada em DNA. A imagem é dividida em seus canais vermelho, verde e azul, que são então convertidos em matrizes de valores numéricos. Cada matriz é submetida a uma operação XOR com a matriz correspondente da chave, produzindo uma matriz encriptada. As matrizes encriptadas são então combinadas para formar a imagem encriptada.
  
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
## Conclusão
O projeto é uma demonstração de como usar mapas caóticos e DNA para encriptar arquivos de imagem. O projeto usa uma combinação do mapa logístico, um gerador de números aleatórios quânticos e o mapa de Lorenz para gerar uma chave segura e aleatória, que é então codificada em uma sequência de nucleotídeos que representa DNA. A chave é usada para encriptar uma imagem usando uma operação XOR. O projeto pode ter várias aplicações potenciais, como criptografia de dados, esteganografia ou biologia computacional. O projeto também ilustra a conexão entre a matemática, a física e a biologia, e como elas podem ser usadas para criar sistemas complexos e criativos.

# Créditos
The author of this project is **Bruno Bezerra Trigueiro**, currently affiliated with the **São Paulo State Technological College (FATEC)**. 
It's inspired by the following scientific publication:
https://www.sciencedirect.com/science/article/abs/pii/S0165168418300859

The author can be **contacted** through the email addresses [bruno.trigueiro@proton.me](mailto:bruno.trigueiro@proton.me) or [bruno.trigueiro@fatec.sp.gov.br](mailto:bruno.trigueiro@fatec.sp.gov.br).
Also, you can contact me at:
https://www.linkedin.com/in/brunotrigueiro/

 **Disclaimer:** 
 It is important to note that this project are of an academic nature and should not be interpreted as proven scientific facts.
 
