
# Compilador da Linguagem TPP - Analise Sintática
### Guilherme Vasco da Silva
### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
### Caixa Postal 15.064 – 91.501-970 – Campo Mourão – PR – Brasil

#### guilhermevasco@alunos.utfpr.edu.br

### Resumo
Este trabalho foi realizado como sequência das duas primeiras etapas da compilação de códigos na linguagem TPP. Será abrangida a terceira parte da compilação, a análise semântica, onde espera-se ser realizada uma segunda passada no código, capaz de gerar uma tabela de símbolos e uma árvore podada ao final da execução.

### 1. Introdução
A análise semântica dá continuidade à árvore sintática abstrata (AST) gerada pela análise léxica e análise sintática (duas primeiras etapas da compilação). Nessa etapa, deve ser percorrida a AST, realizando uma segunda passada no código, para a realização da análise sensível ao contexto e a geração de uma tabela de símbolos. O principal motivo da análise semântica é verificar se existem erros de contexto para a linguagem TPP.

### 2. Objetivo
O objetivo da disciplina é o desenvolvimento de um compilador completo para a linguagem de programação TPP. As duas primeiras etapas da compilação já foram realizadas, fornecendo uma AST para ser análisada na etapa de análise semântica.
O objetivo da análise semântica é, então, realizar uma segunda passada no código, a fim de realizar a análise sensível ao contexto, realizando uma anotação de atributos e verificação das regras semânticas estabelecidas para a linguagem.
Para o desenvolvimento da ferramenta de análise semântica foi utilizada a linguagem de programação *Python*, complementada pelas bibliotecas *Anytree* e *Tabulate*, também foi importado o código da análise sintática (*tppparser.py*) com algumas alterações que serão citadas.

### 3. Análise semântica
Para a terceira parte do processo de compilação, a análise semântica deve ser realizada através da AST sendo percorrida para a realização da análise sensível ao contexto, realizando uma anotação de atributos e verificação das regras semânticas estabelecidas para a linguagem. Ao fim da análise devem ser citados erros e avisos em relação às regras semânticas e deve ser gerada uma tabela de símbolos, que será melhor descrita no item **5.**.

### 4. Regras semânticas
Para a análise semântica a AST será percorrida a fim de realizar a identicação de erros semânticos ou de contexto. As definições dos erros serão descritas a seguir.

#### 4.1 Funções e procedimentos
Deve existir o identificador de função (nome e quantidade de parâmetros formais), além de que os parâmetros formais devem ter um apontamento para o identificador de variáveis.

A quantidade de parâmetros reais de uma chamada de função/procedimento func deve ser igual a quantidade de parâmetros formais da sua definição. Caso contrário, gerar uma das mensagens:
- **Erro:** *Chamada à função ‘func’ com número de parâmetros menor que o declarado.*
- **Erro:** *Chamada à função ‘func’ com número de parâmetros maior que o declarado.*

Uma função deve retornar um valor de tipo compatível com o tipo de retorno declarado. Se a função principal que é declarada com retorno inteiro, não apresenta um retorna(0), a mensagem deve ser gerada:
- **Erro:** *Função principal deveria retornar inteiro, mas retorna vazio.*

Funções precisam ser declaradas antes de serem chamadas. Caso contrário a mensagem de erro deve ser emitida:
- **Erro:** *Chamada a função ‘func’ que não foi declarada.*

Uma função qualquer não pode fazer uma chamada à função principal. Devemos verificar se existe alguma chamada para a função principal partindo de qualquer outra função do programa. Caso haja, deve ser gerada a mensagem:
- **Erro:** *Chamada para a função principal não permitida.*

Uma função pode ser declarada e não utilizada. Se isto acontecer um aviso deverá ser emitido:
- **Aviso:** *Função ‘func’ declarada, mas não utilizada.*

Se a função principal fizer uma chamada para ela mesmo, a mensagem de aviso deve ser emitida:
- **Aviso:** *Chamada recursiva para principal.*

#### 4.2 Função principal
Todo programa escrito em TPP deve ter uma função principal declarada. Verificar a existência de uma função principal que inicializa a execução do código. Caso contrário, deve ser apresentada a mensagem:
- **Erro:** *Função principal não declarada.*

A função principal é sempre do tipo inteiro, assim é esperado que seu retorno seja um valor inteiro, do contrário a mensagem deve ser emitida:
- **Erro:** *Função principal deveria retornar inteiro, mas retorna vazio.*

#### 4.3 Variáveis
O identificador de variáveis locais e globais: nome, tipo e escopo devem ser armazenados na Tabela de Símbolos. Variáveis devem ser declaradas e inicializadas antes de serem utilizadas (leitura). Lembrando que uma variável pode ser declarada:
- No escopo do procedimento (como expressão ou como parâmetro formal);
- No escopo global.

Avisos deverão ser mostrados quando uma variável for declarada mas nunca utilizada. Se uma variável ‘a’ for apenas declarada e não for inicializada (escrita) ou não for utilizada (não lida), o analisador deve gerar a mensagem:
- **Aviso:** *Variável ‘a’ declarada e não utilizada.*

Se houver a tentativa de leitura ou escrita de qualquer variável não declarada a seguinte mensagem deve ser apresentada:
- **Erro:** *Variável ‘a’ não declarada.*

Se houver a tentativa de leitura de uma variável ‘a’ declarada, mas não inicializada deve ser apresentada a mensagem:
- **Aviso:** *Variável ‘a’ declarada e não inicializada.*

Se uma variável ‘a’ for declarada duas vezes no mesmo escopo, o aviso deve ser emitido:
- **Aviso:** *Variável ‘a’ já declarada anteriormente.*

#### 4.4 Atribuição
Na atribuição devem ser verificados se os tipos são compatíveis. Por exemplo, uma variável ‘a’ recebe uma expressão ‘b + c’. Os tipos declarados para ‘a’ e o tipo resultado da inferência do tipo da expressão ‘b + c’ deverão ser compatíveis. Se ‘b’ for inteiro e ‘c’ for inteiro, o tipo resultante da expressão será também inteiro. Se assumirmos, por exemplo, que ‘b’ é do tipo inteiro e ‘c’ do tipo flutuante, o resultado pode ser flutuante (se assumirmos isso para nossa linguagem). O que faria a atribuição ‘a := b + c’ apresentar tipos diferentes e a mensagem deve ser apresentada:
- **Aviso:** *Atribuição de tipos distintos ‘a’ inteiro e ‘expressão’ flutuante.*

O mesmo pode acontecer com a atribuição de um retorno de uma função, se os tipos forem incompatíveis o usuário deve ser avisado:
- **Aviso:** *Atribuição de tipos distintos ‘a’ flutuante e ‘func’ retorna inteiro.*

#### 4.5 Coerções implícitas
Avisos deverão ser mostrados quando ocorrer uma coerção implícita de tipos (inteiro<->flutuante). Atribuição de variáveis ou resultados de expressões de tipos distintos devem gerar a mensagem:
- **Aviso:** *Coerção implícita do valor de ‘x’.*
- **Aviso:** *Coerção implícita do valor retornado por ‘func’.*

#### 4.6 Arranjos
Na linguagem TPP é possível declarar arranjos (*array*), pela sintaxe da linguagem o índice de um arranjo é inteiro e isso deve ser verificado. Na tabela de símbolos devemos armazenar se uma variável declarada tem um tipo, se é uma variável escalar, ou um vetor, ou uma matriz. Podemos armazenar um campo ‘dimensões’, que ‘0’: escalar, ‘1’: arranjo unidimensional (vetor) e ‘2’: arranjo bidimensional (matriz) e assim por diante. Encontrado a referência a um arranjo, seu índice, seja um número, variável ou expressão deve ser um inteiro. Do contrário, a mensagem deve ser gerada:
- **Erro:** *Índice de array ‘x’ não inteiro.*

Se o acesso ao elemento do arranjo estiver fora de sua definição, por exemplo um vetor ‘a’ é declarado como tendo 10 elementos (0 a 9) e há um acesso ao ‘a[10]’, a mensagem de erro deve ser apresentada:
- **Erro:** *Índice de array ‘a’ fora do intervalo (out of range).*

### 5. Tabela de símbolos
Para a realização da análise dos erros apontados, a construção de uma tabela de símbolos deve ser realizada adequadamente. Uma Tabela de Símbolos pode começar a ser construída desde as análises anteriores, como é o caso do código gerado nesta tarefa, onde a tabela de símbolos começa a ser gerada na análise sintática e é passada à análise semântica.

A tabela de símbolos deverá conter os campos:
- Token
- Lexema
- Tipo
- Dim (quantidade de dimentsões de arranjo)
- Tam_dim_1 (tamanho da primeira dimensão)
- Tam_dim_2 (tamanho da segunda dimensão)
- Escopo
- Init (S para inicializada e N para não inicializada)
- Linha

Um exemplo de tabela de símbolos esperada pode ser vista na Figura 1.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/relatorio/img/exemplo_tabela_simbolos.png)

**Figura 1. Exemplo de tabela de símbolos esperada.**

### 6. Poda da árvore
Após a análise semântica e geração de dados referentes a esta passagem, é esperado como saída uma árvore sintática abstrata anotada (ASTO).
Após a verificação das regras semânticas, pode-se fazer uma poda dos nós internos da árvore para facilitar a geração de código. 

Um exemplo de árvore podada esperada pode ser visto na Figura 2.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/relatorio/img/exemplo_arvore_poda.png)

**Figura 2. Exemplo de árvore podada esperada.**

### 7. Implementação
A primeira etapa da implementação da análise semântica a ser considerada foi a geração da tabela de símbolos.

Como foi citado no item *5.*, é possível iniciar a geração da tabela de símbolos ainda nas outras fases da compilação, assim, na implementação da ferramenta o código da análise sintática (*tppparser.py*) foi customizado para poder enviar dados dos atributos e funções para serem lidos durante a análise semântica.
Foram feitas alterações no código de análise sintática para obter os valores de token, lexema, tipo, número de dimensões, escopo e linha de cada váriavel e exportar esses valores para serem importados na análise semântica, gerando um vetor de auxílio com esses dados (*var_list*), tanmbém foi gerado um vetor de auxílio similar para as funções (*func_list*), que também é utilizado na análise semântica, apesar de não haver a geração de uma tabela de funções.

Apesar das alterações realizadas, os resultados gerados pela análise sintática permanecem os mesmos e ela pode ser executada normalmente. Porém, pode ser notado que na versão presente na terceira etapa da compilação, o código do tppparser não gera todas as versões da árvore que são geradas na segunda etapa e o resultado da árvore não é impresso no terminal. Isso foi feito, pois foi deixada somente a árvore principal sendo gerada em PNG e DOT e o resultado não é impresso para ocupar menor espaço na impressão da análise semântica no terminal, uma vez que a análise semântica precisa executar o código da análise sintática.

Por conta da tabela de símbolos já ter sido iniciada na análise sintática, a ferramenta desenvolvida não precisa realizar uma passada direta no arquivo DOT gerado para realizar a análise, ela pode realizar a leitura direto nos vetores auxiliares *var_list* e *func_list* enviados pela análise sintática. Assim, é realizada uma passada direto nos vetores de auxílio e realizadas todas as verificações propostas pelas regras semânticas, tendo sido criadas funções para cada regra, como pode ser visto na Figura 3. 

Durante a passada nos vetores de auxílio é enviada a variável *message_list*, que receberá as mensagens de aviso e erro geradas pelas regras. Essa varíavel é impressa no terminal e, em seguida, é impressa a lista de símbolos.
Vale ressaltar que a lista de símbolos ainda recebe algumas alterações na execução das regras, antes de ser impressa na análise semântica, como por exemplo para cálculo do tamanho das dimensões, uma vez que a análise sintática envia o conteúdo das dimensões no vetor de auxílio (necessário para as regras referentes a arranjos).

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/relatorio/img/check_semantica.png)

**Figura 3. Função *check_semantica*, responsável por chamar a execução das regras.**

Após a análise, é gerada uma árvore podada, utilizando uma função de ajuste da árvore (*ajustar_arvore*), que recebe uma lista de nós que podem ser removidos para reduzir a árvore. É gerado o arquivo *arquivo.prunned.unique.ast.png*, contendo a árvore podada.

### 8. Execução
Para a execução da terceira etapa, os arquivos referentes à análise léxica e sintática devem estar presentes na mesma pasta do arquivo de análise semântica. O arquivo *tppsemantica.py* pode, então, ser executado utilizando Python, com o comando:
- python tppsemantica.py arquivo.tpp

#### 8.1 Testes
Foi fornecida, para realização de testes, a pasta *semantica-testes*, contendo 19 códigos em TPP para testes e, nesses códigos, os avisos e erros esperados de serem impressos, em forma de comentários nos códigos.

Para execução de exemplo será mostrado o arquivo *sema-006.tpp*, podendo ser executado pelo comando:
- python tppsemantica.py sema-006.tpp

O resultado obtido no terminal é mostrado na Figura 4.

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/relatorio/img/exemplo_resultado.png)

**Figura 4. Resultado impresso no terminal após a execução do código *sema-006.tpp*.**

Já na Figura 5 são mostrados os resultados esperados (comentário no código).

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/relatorio/img/exemplo_comentario.png)

**Figura 5. Resultado esperado, presente no código *sema-006.tpp*.**

#### 8.2 Resultados esperados e obtidos
Como pode ser visto na Figura 4, em comparação com a Figura 5, alguns resultados impressos foram diferentes dos esperados na execução do código. Esse comportamento foi visto na minoria dos casos, mas, avaliando os códigos, pôde ser notado que esse comportamente se deve pela sequência de análise das regras e, também, por alguns erros e avisos que deveriam estar presentes nos códigos esperados, mas não estavam registrados (como exemplo das coerções implícitas vistas na Figura 4).

Outro resultado obtido diferente do esperado foi a geração da árvore podada. Lembrando que a árvore podada deve se assemelhar com a Figura 2, a árvore gerada pela ferramenta ficou com a seguinte aparência:

![](https://raw.githubusercontent.com/GuilherveMasco/Compiladores_2022/main/BCC__BCC36B__P3__Guilherme_Vasco_1603019/impl/semantica-testes/sema-006.tpp.prunned.unique.ast.png)

**Figura 6. Árvore podada resultante do código *sema-006.tpp*.**

Como pode ser notado na Figura 6, a árvore podada obtida ainda ficou maior e não completamente otimizada. Essa diferença ocorre, principalmente, por conta do método de poda utilizado.

### 9. Conclusões
Apesar das diferenças obtidas nos resultados esperados, a ferramenta de análise semântica desenvolvida possui um funcionamento bom o suficiente para ser utilizada para a próxima, e última, etapa do processo de compilação.

Antes da próxima etapa, porém, será necessário verificar o código um pouco mais e gerar novas atualizações, buscando, principalmente, a otimização da árvore podada e realizando novos testes para verificar se todos os erros e avisos estão de acordo com o esperado.

### Referências
Gonçalves, R. A. (2022) “Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Semântica (Trabalho – 3ª parte)”, https://moodle.utfpr.edu.br/pluginfile.php/2647538/mod_resource/content/19/trabalho-03.md.article.pdf.
Louden, K. C. (2004) “Análise Sintática Ascendente”, Em: Compiladores: princípios e práticas., EUA.
Beazley, D. M. (2021) “PLY (Python Lex-Yacc)”, https://www.dabeaz.com/ply/ply.html
Johnson, S. C. (1979) Yacc: Yet Another Compiler-Compiler.
Astanin, S. (2012) “python-tabulate”, https://pypi.org/project/tabulate/