# Compilador da Linguagem TPP - Geração de código intermediário
### Guilherme Vasco da Silva
### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
### Caixa Postal 15.064 – 91.501-970 – Campo Mourão – PR – Brasil

#### guilhermevasco@alunos.utfpr.edu.br

### Resumo
Este trabalho foi realizado como parte final do processo de compilação de códigos na linguagem TPP, trazendo a função de geração de código intermediário, gerando um código bitcode (.bc) e uma versão executável do programa em TPP compilado.

### 1. Introdução
A geração de código intermediário é a etapa final do processo de compilação, onde o código fonte, já verificado nos aspectos léxico, sintático e semântico, é transformado em código interpretável pela máquina. Como o código deve passar pelas análises anteriores, será garantido que o código executado pelo gerador de código intermediário será correto, sme ter erros sintáticos, léxicos ou semânticos. Para possibilitar a geração de código intermediário, será utilizado o compilador desenvolvido nas duas primeiras etapas da disciplina, que já realiza a análise léxica, sintática e semântica. A partir da AST gerada pela análise sintática, será realizada a análise semântica, que irá gerar uma tabela de símbolos e uma árvore podada, que será utilizada para a geração de código intermediário.

### 2. Objetivo
O objetivo da disciplina é o desenvolvimento de um compilador completo para a linguagem de programação TPP. O compilador deve ser capaz de realizar a análise léxica, sintática e semântica, gerando uma AST e uma tabela de símbolos. A partir desses dados, deve ser gerado um código intermediário, que poderá ser interpretado por uma máquina real (ou virtual). O objetivo da geração de código intermediário é a execução do código fonte, que já foi verificado nos aspectos léxico, sintático e semântico, percorrendo a árvore podada gerada na etapa de análise semântica.

### 3. Geração de código
A geração de código, como visto anteriormente, é a etapa final do processo de compilação, onde o código fonte, já verificado nos aspectos léxico, sintático e semântico, é transformado em código interpretável pela máquina. Como o código deve passar pelas análises anteriores, será garantido que o código executado pelo gerador de código intermediário será correto, sem ter erros sintáticos, léxicos ou semânticos. Assim, o código gerado pelo gerador de código intermediário será executado sem erros, caso hajam erros, eles serão detectados nas análises anteriores e retornados antes da execução da geração de código, não gerando código executável.

Para a realização da geração de código, a árvore podada do código de entrada, gerada na fase de análise semântica, será percorrida e o código gerado será escrito em um arquivo de saída, que será um código *bitcode* (.bc) e uma versão executável do programa em TPP compilado. A geração de um bitcode é feita possível através do LLVM (*Low Level Virtual Machine*), que é utilizado para prover Módulos, Funções, Blocos e Instruções ao código, possibilitando a geração de um código interpretável por máquina através do *bitcode* gerado.

#### 3.1 Módulos
Um módulo representa um representa um arquivo com código fonte ou uma unidade de tradução. Todo o restante do código deve estar dentro de um módulo, incluindo as Funções, que contém partes do código.

#### 3.2 Funções
Uma função é uma parte do código que pode ser chamada por outras partes do código. Uma função pode ser chamada por outras funções, ou por um bloco. Uma função pode conter Blocos, que são partes do código que podem ser executadas, e Instruções, que são as ações que podem ser executadas. Uma função pode conter outras funções, que podem ser chamadas por ela.

#### 3.3 Blocos
Um bloco (ou *Basic Block*) é uma parte do código que pode ser executada. Um bloco pode conter Instruções, que são as ações que podem ser executadas. Para fins de melhor compreensão, um bloco é um pedaço contínuo de instruções.

#### 3.4 Instruções
Uma intrução é uma operação única e expressa em um código. Uma instrução pode ser uma operação aritmética, uma operação lógica, uma operação de atribuição, uma operação de entrada e saída, uma operação de controle de fluxo, uma operação de chamada de função, entre outras. Uma instrução pode ser executada por um bloco.

### 4. Implementação
A implementação do compilador foi realizada em Python, utilizando a biblioteca *llvmlite*, que é uma biblioteca Python para o LLVM. Também foi necessária a instalação do compilador da linguagem C, *clang* (*clang-11*), que é utilizado para compilar o código gerado pelo compilador. Para possibilitar a geração de código, foram criadas diferentes funções, que são chamadas de acordo com o tipo de nó da árvore podada. Cada função é responsável por gerar o código de acordo com o tipo de nó da árvore podada, levando em conta os possíveis, módulos, funções, blocos e instruções da linguagem TPP. A seguir, será apresentada a estrutura do código, com as funções e suas responsabilidades.

#### 4.1 Estrutura do código
O código se inicia através do retorno da análise semântica, obtendo as variáveis *root* (raíz da árvore), *message_list* (mensagens geradas pela análise), *func_list* (lista de funções obtidas) e *var_list* (lista de variáveis obtidas). Essas variáveis serão percorridas através das funções de geração de código para poder gerar o arquivo bitcode. Caso hajam mensagens de erro (*ERROR*) na variável *message_list*, o código não será gerado e as mensagens serão exibidas na tela. Caso não haja mensagens de erro, o código será gerado e o arquivo bitcode será escrito no arquivo *<nome_do_arquivo>.bc*.

Caso não hajam erros, o código chama a função *geração*, enviando de atributo a variável *root* obtida da análise semântica. Essa função é responsável por percorrer os nós filhos da árvore e verificar se são declarações de função ou de variáveis, chamando a função adequada de acordo com o tipo de nó, como visto na Figura 1.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P4__Guilherme_Vasco_1603019/relatorio/img/geracao.png)

**Figura 1. Função *geração* no código desenvolvido.**

A função *dec_variavel_global* vvincula uma variável como global, ela é somente chamada na função *geração*, como visto na Figura 1, pois se a variável for declarada dentro de outra função (não global) será chamada por outro trecho de código e não será filha diretamente do nó raíz.

Já a função *dec_funcoes* é chamada para declaração de funções e cria o escopo de acordo com elas, preenchendo os blocos que existirem dentro das funções e chamando a função *dec_variavel_local* para declarar as variáveis locais dentro de seu escopo. Essa função também é chamada na função *geração*, como visto na Figura 1.

A função *arvore* é responsável por percorrer os nós da árvore podada e chamar a função adequada de acordo com o tipo de instrução, bloco, ou função que é encontrado no nó. Essa função é chamada por outras funções, como *dec_funcoes*.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P4__Guilherme_Vasco_1603019/relatorio/img/arvore.png)

**Figura 2. Função *arvore* no código desenvolvido.**

Na Figura 2 é possível visualizar que as opções de funções são: *retorno_codigo*, *leia_codigo*, *escreva_codigo*, *atribuicao_codigo*, *se_codigo*, *repita_codigo* e *chamada_funcao_codigo*, responsáveis por retornar valores no código, ler valores enviados pelo terminal, imprimir valores no terminal, atribuir valores a variáveis, criar estruturas condicionais, criar estruturas de repetição e chamar funções, respectivamente. Cada uma dessas funções é responsável por gerar o código de acordo com a instrução que está sendo executada, chamando o *builder* do LLVM para gerar o código adequado em linguagem de máquina.

Também foram implementadas as funções auxiliares *get_variavel_lista* (Figura 3) e *get_tipo* (Figura 4), que são responsáveis por verificar se uma variável existe na lista de variáveis, retornando o valor dela e obter o tipo de uma variável, respectivamente. Essas funções auxiliares são chamadas por outras funções ao longo do código.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P4__Guilherme_Vasco_1603019/relatorio/img/get_variavel.png)

**Figura 3. Função *get_variavel_lista* no código desenvolvido.**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P4__Guilherme_Vasco_1603019/relatorio/img/tipo.png)

**Figura 4. Função *get_tipo* no código desenvolvido.**

Como pode ser visto na Figura 4, é necessário a chamada de uma biblioteca *ir* para identificar o tipo a ser utilizado na linguagem de máquina. Essa biblioteca *ir* é a chamada do LLVM (LLVM IR) no código, utilizando a estrutura do tipo IR por permitr a especificação de estruturas identificadas e literais.

Após percorrer a árvore e executar a função *geracao* por completo, é criado um arquivo de nome *<nome_do_arquivo>.ll* com o código gerado em linguagem de máquina, que pode ser executado por um compilador de LLVM, como o *llc*. A execução desse código é realizada, com auxílio do compilador *clang* através de chamadas de comandos na função *main*, com os comandos utilizados podendo ser vistos na Figura 5.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P4__Guilherme_Vasco_1603019/relatorio/img/cmd.png)

**Figura 5. Comandos do terminal executados pelo código desenvolvido.**

Na Figura 5 também pode ser vista a chamada ao arquivo *io-helper*, que é responsável por criar as funções de leitura e escrita no terminal, que são utilizadas no código gerado.

### 5. Execução

#### 5.1 Testes

#### 5.2 Resultados esperados e obtidos

### 6. Conclusões

### Referências
Gonçalves, R. A. (2022) “Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Semântica (Trabalho – 3ª parte)”, https://moodle.utfpr.edu.br/pluginfile.php/2647538/mod_resource/content/19/trabalho-03.md.article.pdf.
Louden, K. C. (2004) “Análise Sintática Ascendente”, Em: Compiladores: princípios e práticas., EUA.
Beazley, D. M. (2021) “PLY (Python Lex-Yacc)”, https://www.dabeaz.com/ply/ply.html
Johnson, S. C. (1979) Yacc: Yet Another Compiler-Compiler.
Astanin, S. (2012) “python-tabulate”, https://pypi.org/project/tabulate/