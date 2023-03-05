# 🧬Sphinx
Criptografia de imagens usando operações de sequência de DNA e caos espaço-temporal

## Introdução
Sphinx é um algoritmo de criptografia de imagem colorida baseado em operações de sequência de DNA, chaves de uso único e caos espaço-temporal. Este projeto tem como objetivo fornecer um método de criptografia seguro e eficiente para imagens coloridas, utilizando as propriedades únicas da computação de DNA.

## Explicação
Sphinx funciona gerando fluxos de chaves usando o CML baseado em mapa NCA, onde a função de hash SHA-256 é usada para atualizar os parâmetros do sistema e as condições iniciais combinando com a imagem simples e as chaves secretas. A imagem simples é então decomposta em componentes vermelho, verde e azul e convertida aleatoriamente em três matrizes de DNA pelas regras de codificação de DNA. Essas três matrizes de DNA são combinadas em uma nova matriz de DNA e, em seguida, permutações de linhas e colunas são realizadas nela. A matriz de DNA embaralhada é então dividida em três blocos iguais e operações de adição, subtração e XOR de DNA são implementadas nesses blocos de DNA. Finalmente, as matrizes de DNA são transformadas em matrizes decimais separadamente de acordo com as regras de decodificação de DNA. Um processo de difusão é realizado usando os fluxos de chaves para aumentar a segurança do criptossistema, resultando em uma imagem cifrada.

## Como funciona
O processo de criptografar uma imagem usando Sphinx é o seguinte:

- Gerar fluxos de chaves usando o CML baseado em mapa NCA e combiná-los com a imagem simples e as chaves secretas usando a função de hash SHA-256.
- Decompor a imagem simples em componentes vermelho, verde e azul e convertê-las aleatoriamente em três matrizes de DNA usando as regras de codificação de DNA.
- Combinar as três matrizes de DNA em uma nova matriz de DNA e realizar permutações de linhas e colunas.
- Dividir a matriz de DNA embaralhada em três blocos iguais e implementar operações de adição, subtração e XOR de DNA nesses blocos.
- Transformar as matrizes de DNA em matrizes decimais separadamente de acordo com as regras de decodificação de DNA.
- Realizar um processo de difusão usando os fluxos de chaves para aumentar a segurança e obter a imagem cifrada.


## Objetivos
O principal objetivo do Sphinx é fornecer um método seguro e eficiente de criptografia de imagens coloridas usando operações de sequência de DNA e caos espaço-temporal. Ao utilizar as propriedades únicas da computação de DNA e da teoria do caos, Sphinx tem como objetivo aumentar a segurança dos métodos de criptografia de imagens.
