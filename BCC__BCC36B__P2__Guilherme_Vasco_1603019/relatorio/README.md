
# Compilador da Linguagem TPP - Analise Sintática
### Guilherme Vasco da Silva
### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
### Caixa Postal 15.064 – 91.501-970 – Campo Mourão – PR – Brasil

#### guilhermevasco@alunos.utfpr.edu.br

#### Resumo
Este trabalho foi realizado através do estudo de um código inicial, fornecido pelo professor, referente à operação de Análise Sintática do compilador da linguagem de programação TPP. A análise sintática é a segunda etapa do processo de compilação, onde os tokens gerados na Análise Léxica são utilizados para gerar uma árvore sintática.

### 1. Introdução
A análise sintática é a segunda etapa do processo de compilação, ela dá continuidade direta da análise léxica, pegando os tokens gerados nessa primeira análise e utilizando eles para a geração de uma árvore sintática, que possui toda a estrutura do código de entrada. Cada nó da árvore sintática é formada por suas expressões regulares, tokens e valores, de maneira que nas folhas da árvore pode ser encontrado o código completo.

### 2. Objetivo
O objetivo da disciplina é o desenvolvimento de um compilador completo para a linguagem de programação TPP. A primeira parte do objetivo foi realizada com a análise léxica, já a segunda parte se trata da análise sintática, que visa gerar a árvore sintática do código do programa fornecido, para ser utilizada na etapa seguinte da compilação do programa.
Para o desenvolvimento da ferramenta de análise sintática foi utilizada a linguagem de programação *Python*, complementada pelas bibliotecas *Graphviz*, *Anytree* e *PLY*.
### 3. Gramática
Para a definição de regras de uma linguagem livre de contexto, em forma teztual, pode ser utilizado o padrão *Backus-Naur Form* (BNF). De acordo com o padrão BNF, a linguagem TPP pode ser descrita pela seguinte tabela de tokens:

|                              |                                                                                         |
|------------------------------|-----------------------------------------------------------------------------------------|
|                programa ::=  | lista_declaracoes                                                                       |
|       lista_declaracoes ::=  | lista_declaracoes declaracao \| declaracao                                              |
|               declaracao ::= | declaracao_variaveis \| inicializacao_variaveis \| declaracao_funcao                    |
|     declaracao_variaveis ::= | tipo ":" lista_variaveis                                                                |
|  inicializacao_variaveis ::= | atribuicao                                                                              |
|          lista_variaveis ::= | lista_variaveis "," var  \| var                                                         |
|                      var ::= | ID \| ID indice                                                                         |
|                   indice ::= | indice "[" expressao "]" \| "[" expressao "]"                                           |
|                     tipo ::= | INTEIRO \| FLUTUANTE                                                                    |
|        declaracao_funcao ::= | tipo cabecalho  \| cabecalho                                                            |
|                cabecalho ::= | ID "(" lista_parametros ")" corpo FIM                                                   |
|         lista_parametros ::= | lista_parametros "," parametro \| parametro \| vazio                                    |
|                parametro ::= | tipo ":" ID \|  parametro "[" "]"                                                       |
|                    corpo ::= | corpo acao  \| vazio                                                                    |
|                     acao ::= | expressao \| declaracao_variaveis \| se \| repita \| leia \| escreva \| retorna \| erro |
|                       se ::= | SE expressao ENTAO corpo FIM \| SE expressao ENTAO corpo SENAO corpo FIM                |
|                   repita ::= | REPITA corpo ATE expressao                                                              |
|               atribuicao ::= | var ":=" expressao                                                                      |
|                     leia ::= | LEIA "(" var ")"                                                                        |
|                  escreva ::= | ESCREVA "(" expressao ")"                                                               |
|                  retorna ::= | RETORNA "(" expressao ")"                                                               |
|                expressao ::= | expressao_logica \| atribuicao                                                          |
|         expressao_logica ::= | expressao_simples \| expressao_logica operador_logico expressao_simples                 |
|        expressao_simples ::= | expressao_aditiva \| expressao_simples operador_relacional expressao_aditiva            |
|        expressao_aditiva ::= | expressao_multiplicativa \| expressao_aditiva operador_soma expressao_multiplicativa    |
| expressao_multiplicativa ::= | expressao_unaria \| expressao_multiplicativa operador_multiplicacao expressao_unaria    |
|         expressao_unaria ::= | fator \| operador_soma fator \| operador_negacao fator                                  |
|      operador_relacional ::= | "<" \| ">"  \| "="  \| "<>"  \| "<="  \| ">="                                           |
|            operador_soma ::= | "+" \| "-"                                                                              |
|          operador_logico ::= | "&&" \| "\|\|"                                                                          |
|         operador_negacao ::= | "!"                                                                                     |
|   operador_multiplicacao ::= | "*" \| "/"                                                                              |
|                    fator ::= | "(" expressao ")" \| var \| chamada_funcao \| numero                                    |
|                   numero ::= | NUM_INTEIRO \| NUM_PONTO_FLUTUANTE \| NUM_NOTACAO_CIENTIFICA                            |
|           chamada_funcao ::= | ID "(" lista_argumentos ")"                                                             |
|        lista_argumentos  ::= | lista_argumentos "," expressao \| expressao \| vazio                                    |

A partir dessa tabela é possível gerar os diagramas sintáticos a seguir:

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/programa.png)

**Figura 1. Regra para programa**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/lista_declaracoes.png)

**Figura 2. Regra para lista_declaracoes**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/declaracao.png)

**Figura 3. Regra para declaracao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/declaracao_variaveis.png)

**Figura 4. Regra para declaracao_variaveis**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/inicializacao_variaveis.png)

**Figura 5. Regra para inicializacao_variaveis**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/lista_variaveis.png)

**Figura 6. Regra para lista_variaveis**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/var.png)

**Figura 7. Regra para var**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/indice.png)

**Figura 8. Regra para indice**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/tipo.png)

**Figura 9. Regra para tipo**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/declaracao_funcao.png)

**Figura 10. Regra para declaracao_funcao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/cabecalho.png)

**Figura 11. Regra para cabecalho**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/lista_parametros.png)

**Figura 12. Regra para lista_parametros**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/parametro.png)

**Figura 13. Regra para parametro**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/corpo.png)

**Figura 14. Regra para corpo**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/acao.png)

**Figura 15. Regra para acao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/se.png)

**Figura 16. Regra para se**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/repita.png)

**Figura 17. Regra para repita**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/atribuicao.png)

**Figura 18. Regra para atribuicao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/leia.png)

**Figura 19. Regra para leia**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/escreva.png)

**Figura 20. Regra para escreva**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/retorna.png)

**Figura 21. Regra para retorna**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao.png)

**Figura 22. Regra para expressao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao_logica.png)

**Figura 23. Regra para expressao_logica**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao_simples.png)

**Figura 24. Regra para expressao_simples**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao_aditiva.png)

**Figura 25. Regra para expressao_aditiva**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao_multiplicativa.png)

**Figura 26. Regra para xpressao_multiplicativa**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/expressao_unaria.png)

**Figura 27. Regra para expressao_unaria**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/operador_relacional.png)

**Figura 28. Regra para operador_relacional**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/operador_soma.png)

**Figura 29. Regra para operador_soma**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/operador_logico.png)

**Figura 30. Regra para operador_logico**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/operador_negacao.png)

**Figura 31. Regra para operador_negacao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/operador_multiplicacao.png)

**Figura 32. Regra para operador_multiplicacao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/fator.png)

**Figura 33. Regra para fator**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/numero.png)

**Figura 34. Regra para numero**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/chamada_funcao.png)

**Figura 35. Regra para chamada_funcao**

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/lista_argumentos.png)

**Figura 36. Regra para lista_argumentos**

### 4. Árvore Sintática
A ferramenta desenvolvida para análise sintática da linguagem TPP realiza a análise de forma LALR(1), ou Look-Ahead LR, implementado pela biblioteca YACC. Esta forma de análise consegue diminuir os estados da tabela final, gerando menos estados que outros formatos.
A ferramenta utiliza o MyTree, parte da biblioteca Anytree, para a geração gráfica da árvore sintática. 
A árvore sintática é composta por nós, esses nós são criados na ferramenta dentro de um construtor na classe MyNode, para ele é passado nome, pai, ID, tipo, label e filhos e o construtor cria o nó a partir dessas informações.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/mynode.PNG)

**Figura 37. Criação de um nó na ferramenta através do MyTree.**

### 5. Implementação
Juntamente ao MyTree, foi utilizada, para desenvolvimento da ferramenta, a biblioteca YACC (Yet Another Compiler Complier), parte da biblioteca PLY.
Para a implementação, cada regra gramatical é definida por uma função, esta contendo um cabeçalho com a especificação gramatical apropriada.
Cada função aceita um único argumento *p* que é uma sequência contendo os valores de cada símbolo gramatical na regra correspondente da função.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/p_programa.PNG)

**Figura 38. Exemplo de função com o cabeçalho da regra *programa*.**

Cada função também pode ter sua função de tratamento de erro. Para tal função, também, deve ser definido o cabeçalho com as regras que serão responsáveis por chamar essa função. A função de erro, para ser chamada, deve seguir o padrão do nome da função de sucesso, com o termo *_error* logo a seguir.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/p_cabecalho_error.PNG)

**Figura 39. Exemplo de função de erro com o cabeçalho da regra *cabecalho*.**

Assim, para a ferramenta, foram fornecidas as regras e desenvolvidas as regras de erro para cada cabeçalho, considerando que não são todos os cabeçalhos onde é possível executar erros.
Ao longo da execução da análise em um código, são geradas diversas sub-árvores (referentes a cada cabeçalho), ao final, todas as sub-árvores são juntadas, formando a árvore sintática. Nas folhas da árvore sintática poderá ser encontrado o código de entrada completo.

### 6. Execução
Para a execução da ferramenta é necessário ter a linguagem de programação Python (versão 3) e as bibliotecas Graphviz, Anytree e PLY. A execução é realizada pelo comando *python tppparser.py <ARQUIVO.tpp>*, onde <ARQUIVO.tpp> deve ser substituído pelo nome do arquivo que se deseja ser varrido para geração da árvore.

#### 6.1 Testes
Juntamente ao código é fornecida a pasta *sintatica-testes*, que fornece diversos códigos na linguagem TPP para testes.
Executando o código *somavet.tpp* com o comando *python tppparser.py somavet.tpp* são gerados os arquivos de saída (no mesmo diretório):

*somavet.tpp.ast.dot*

*somavet.tpp.ast.png*

*somavet.tpp.ast2.png*

*somavet.tpp.unique.ast.dot*

*somavet.tpp.unique.ast.png*

Abrindo o arquivo *somavet.tpp.unique.ast.png* é possível ver a árvore sintática gerada, com o código completo nas folhas da árvore.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P2__Guilherme_Vasco_1603019/relatorio/img/somavet.tpp.unique.ast.png)

**Figura 40. Árvore sintática gerada pela ferramenta para o código *somavet.tpp***


### 7. Conclusões
A árvore sintática gerada pela ferramenta se mostrou funcional para as próximas etapas do processo de compilação dos códigos na linguagem TPP. Os testes mostraram que os códigos foram executados com sucesso e as árvores geradas corretamente.
As bibliotecas PLY e AnyTree facilitaram o processo da geração da árvore sintática, por conta disso, essas bibliotecas foram de grande importância no desenvolvimento da ferramenta.

### Referências
Gonçalves, R. A. (2017) “Documentação online da Gramática da TPP”, https://docs.google.com/document/d/1oYX-5ipzL_izj_hO8s7axuo2OyA279YEhnAItgXzXAQ.
Louden, K. C. (2004) “Análise Sintática Ascendente”, Em: Compiladores: princípios e práticas., EUA.
Beazley, D. M. (2021) “PLY (Python Lex-Yacc)”, https://www.dabeaz.com/ply/ply.html
Johnson, S. C. (1979) Yacc: Yet Another Compiler-Compiler.