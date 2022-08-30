
# Compilador da Linguagem TPP - Analise Léxica
### Guilherme Vasco da Silva
### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
### Caixa Postal 15.064 – 91.501-970 – Campo Mourão – PR – Brasil

#### guilhermevasco@alunos.utfpr.edu.br

#### Resumo
Este trabalho foi realizado através do estudo de um código inicial, fornecido pelo professor, referente à operação de Análise Léxica do compilador da linguagem de programação TPP. A análise léxica é a primeira etapa do processo de compilação, onde são extraídos os tokens da linguagem em um determinado código. Estre trabalho descreve a linguagem TPP e o processo utilizado para a realização da análize lexica.

### 1. Introdução
A análise léxica é a primeira parte do processo de compilação, onde é realizada uma varredura no código fornecido, com o objetivo de converter os caracteres presentes no código em um conjunto de tokens. Os tokens são palavras chave e símbolos que representam as funções da linguagem, como: palavras reservadas (se, então, senão, repita, etc), símbolos de operações (+, -, *, /, etc), entre outros. Ao final de uma análise léxica, a saída esperada do processo é uma lista, em ordem, de todos os tokens presentes no código fornecido.

### 2. Objetivo
O objetivo da disciplina é o desenvolvimento de um compilador completo para a linguagem de programação TPP. Nesta primeira parte da disciplina o trabalho desenvolvido foi o desenvolvimento de uma ferramenta para a realização da análise léxica de códigos escritos na linguagem TPP e, para tal, foi utilizada a linguagem de programação Python, juntamente com a biblioteca PLY. A escolha dessa linguagem foi por ela, além de ser uma linguagem já utilizada anteriormente pelos alunos do curso, possui a biblioteca PLY, que fornece os recursos das ferramentas LEX e YACC, que auxiliam no processo de criação de um compilador.

### 3. Linguagem TPP
A linguagem utilizada durante a disciplina, e que será varrida neste trabalho pelo analisador léxico, será a TPP, que suporta dados inteiros e flutuantes e suporte a arranjos unidimensionais e bidimensionais. Nessa linguagem há a necessidade da especificação de tipos das variáveis locais e globais, porém as funções podem ter tipo omitido. A linguagem possui também operações de adição, multiplicação, subtração, divisão e também operadores lógicos E, OU e NÃO. Nas subseções a seguir serão detalhadas as características da linguagem.

#### 3.1 Tipos
A linguagem TPP suporta, para suas variáveis e funções, os tipos:
- Inteiro
- Flutuante
- Notação científica

#### 3.2 Operações
As operações matemáticas e lógicas suportadas pela linguagem TPP são:
|  **Operação** | **Símbolo** |
|:-------------:|:-----------:|
|      Soma     |      +      |
|   Subtração   |      -      |
| Multiplicação |      *      |
|    Divisão    |      /      |
|       E       |      &&     |
|       OU      |     \|\|    |
|    Negação    |      !      |

#### 3.3 Comparações
Também são possíveis comparações, com os símbolos:
|  **Operação**  | **Símbolo** |
|:--------------:|:-----------:|
|      Maior     |      >      |
|      Menor     |      <      |
| Maior ou igual |      >=     |
| Menor ou igual |      <=     |
|    Diferença   |      <>     |

#### 3.4 Palavras reservadas
Na linguagem TPP, são reservadas as palavras (em português e com acentos):
- **SE**
- **ENTÃO**
- **SENÃO**
- **FIM**
- **REPITA**
- **FLUTUANTE**
- **RETORNA**
- **ATÉ**
- **LEIA**
- **ESCREVA**
- **INTEIRO**

### 4. Ferramenta de análise
Como dito anteriormente, foi utilizada a linguagem Python, juntamente com a biblioteca PLY, para o desenvolvimento da ferramenta responsável pela análise léxica. Nas próximas subseções será discutida essa ferramenta.

#### 4.1 Vetores de auxílio
Para auxiliar na operação de varredura dos código, as traduções de todos os tokens e palavras reservadas são armazenadas em dois vetores, *tokens* e *reserved_words*, respectivamente, que podem ser vistos a seguir:
![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/tokens.PNG)
**Figura 1. Vetor auxiliar de tokens.**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/palavras.PNG)
**Figura 2. Vetor auxiliar de palavras reservadas.**

Por conta desses vetores, não é necessário aplicar regras para cada palavra reservada, pois se o token lido não for uma palavra reservada ele é, automaticamente, um ID.

#### 4.2 Expressões regulares
Para a realização do processo de varregura foram utilizadas expressões regulares para cada um dos símbolos da linguagem. O uso de expressões regulares é uma técnica que fornece uma forma lógica para identificação de cadeias de caracteres específicas. A Figura 3 mostra as expressões regulares que foram utilizadas para reconhecer dígitos, letras, sinais e afins (nota: as linhas com # estão comentadas, por conta disso, não estão sendo utilizadas).

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/expressoes-2.PNG)
**Figura 3. Expressões regulares para valores**

Já a Figura 4 mostra as expressões regulares utilizadas para reconhecimento dos símbolos conhecidos e operações.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/expressoes.PNG)
**Figura 4. Expressões regulares para símbolos e operações.**

