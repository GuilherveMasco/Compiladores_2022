
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

### 5. Autômatos e expressões regulares
Uma expressao regular define formalmente um padrão, mostrando quais os sub-padrões ou expressões regulares que a formam, com qual regularidade ou sequencia cada uma delas aparece, e quais sao os diferentes sub-padrões que podem ser reconhecidos em uma mesma posição do padrão.
Qualquer expressão regular pode ser convertida em um autômato finito que ela descreve. Assim podemos converter qualquer uma das expressões regulares utilizadas na ferramenta (citadas anteriormente) em autômatos finitos. 
Para demonstrar isso, podemos utilizar a expressão utilizada para reconhecer números inteiros (DIGITO) que é: ([0 - 9]). O autômato dessa expressão pode ser visto na Figura 5.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/auto-digito.PNG)

**Figura 5. Autômato resultante da expressão ([0 - 9])**

Para a identificação de palavras reservadas também é possível utilizar autômatos, como pode ser visto na Figura 6.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/auto-inteiro.PNG)

**Figura 6. Autômato para reconhecimento da palavra reservada "inteiro".**

### 6. Varredura
A varredura é realizada na função main do código, ela se baseia em ler o arquivo de entrada, valor-por-valor, enquanto houver valor no arquivo. Essa leitura utiliza a função de análise léxica do PLY, lexer. O lexer possibilita a conversão do valor lido para token e a obtenção da sua tradução a partir das expressões regulares e vetores auxiliares.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/main.PNG)

**Figura 7. Realização da varredura, por uso do lexer, na função main.**

### 7. Execução
Para realizar a execução do programa é necessário, primeiramente, possuir o Python e a biblioteca PLY instalados. A instalação da biblioteca PLY, com o Python já instalado, é possível através do comando *pip install ply*.
Os arquivos disponibilizados para execução são lextab.py (gerado pela biblioteca PLY) e o tpplex.py, que é a ferramenta de análise léxica. Está disponibilizada, também, uma pasta com códigos a serem usados de exemplo (lexica-testes).
A execução do programa é, então, realizada executando o arquivo tpplex.py com o Python, utilizando o comando *python tpplex.py <ARQUIVO.tpp>*, onde <ARQUIVO.tpp> deve ser substituído pelo nome do arquivo que se deseja ser varrido.

#### 7.1 Exemplo de execução
Para exemplo de execução, será utilizado o arquivo *fat.tpp*, disponibilizado na pasta *lexica-testes*. Com os dois arquivos na mesma pasta, o comando para execução será: *python tpplex.py fat.tpp*.
O resultado esperado após a execução é:

    INTEIRO
    DOIS_PONTOS
    ID
    FLUTUANTE
    DOIS_PONTOS
    ID
    ABRE_COLCHETE
    NUM_INTEIRO
    FECHA_COLCHETE
    INTEIRO
    ID
    ABRE_PARENTESE
    INTEIRO
    DOIS_PONTOS
    ID
    FECHA_PARENTESE
    INTEIRO
    DOIS_PONTOS
    ID
    SE
    ID
    MAIOR
    NUM_INTEIRO
    ENTAO
    ID
    ATRIBUICAO
    NUM_INTEIRO
    REPITA
    ID
    ATRIBUICAO
    ID
    MULTIPLICACAO
    ID
    ID
    ATRIBUICAO
    ID
    MENOS
    NUM_INTEIRO
    ATE
    ID
    IGUAL
    NUM_INTEIRO
    RETORNA
    ABRE_PARENTESE
    ID
    FECHA_PARENTESE
    SENAO RETORNA
    ABRE_PARENTESE
    NUM_INTEIRO
    FECHA_PARENTESE
    FIM
    FIM
    INTEIRO
    ID
    ABRE_PARENTESE
    FECHA_PARENTESE
    LEIA
    ABRE_PARENTESE
    ID
    FECHA_PARENTESE
    ESCREVA
    ABRE_PARENTESE
    ID
    ABRE_PARENTESE
    ID
    FECHA_PARENTESE
    FECHA_PARENTESE
    RETORNA
    ABRE_PARENTESE
    NUM_INTEIRO
    FECHA_PARENTESE
    FIM
Se a execução do programa estiver correta, esse resultado deve ser idêntico ao arquivo, também disponibilizado na mesma pasta, de nome *fat.tpp.out*.

#### 7.2 Testes
Para verificar o funcionamento do programa, foi realizada uma bateria de testes com 32 algoritmos na linguagem TPP, fornecidos e comparados com os arquivos de saídas esperadas, também fornecidos, na pasta *lexica-testes*. O teste geral foi realizado através do comando *run-tests.sh*, onde o resultado obtido foi:

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P1__Guilherme_Vasco_1603019/relatorio/img/testes.PNG)

**Figura 8. Bateria de testes realizada.**

Na Figura 8 é possível ver, pelo nome do arquivo, qual a função de cada um dos algoritmos em TPP. Na frente do nome é mostrado um “[OK]”, que confirma que a execução foi um sucesso e o resultado compatível com a saída esperada.

### 8. Conclusões
A ferramenta desenvolvida para análise léxica da linguagem TPP se provou eficiente, sendo testado nos arquivos de teste fornecidos sem erros de execução e a saída foi de acordo com o esperado. A biblioteca PLY tornou possível a criação da ferramenta, por possuir funções específicas para análise léxica, o maior trabalho restante é o de obter e organizar os tokens e palavras reservadas da linguagem, bem as expressões regulares necessárias.
O resultado final obtido foi um analisador léxico adequado para ser utilizado na disciplina e pronto para auxiliar na próxima etapa do compilador da linguagem TPP.

### Referências
Gonçalves, R. A. (2021) “Análise Léxica”, https://colab.research.google.com/github/rogerioag/tutorial-de-compiladores/blob/ma ster/tppcompiler/01-compiladores-analise-lexica-tpplex.ipynb. Acessado em agosto de 2022.
Gonçalves, R. A. (2021) “Execução dos Testes da Análise Léxica”, https://colab.research.google.com/drive/1GDRMrJZVDuYzPaaO923zuMLPgxv_Oe DI?usp=sharing#scrollTo=BzQXw87XsjOp. Acessado em agosto de 2022.
Beazley, D. M. (2021) “PLY (Python Lex-Yacc)”, https://www.dabeaz.com/ply/ply.html. Acessado em agosto de 2022.