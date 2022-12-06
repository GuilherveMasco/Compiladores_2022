
import sys

from tabulate import tabulate
from anytree.exporter import UniqueDotExporter

import tppparser


def encontrar_nos(root, label, list_node):
    for node in root.children:
        list_node = encontrar_nos(node, label, list_node)
        if node.label == label:
            list_node.append(node)

    return list_node


def encontrar_nos_pais(sun, label, list_node):
    for index in range(len(sun.anchestors)-1, -1, -1):
        if sun.anchestors[index].label == label:
            list_node.append(sun.anchestors[index])

    return list_node


def encontrar_parametros(root, escope, list_node):

    for node in root.children:
        if node.label == 'chamada_funcao':
            func_name = node.descendants[1].label
            type_func = func_list[func_name][0][1]
            list_node.append((func_name, type_func))
            return list_node
        elif node.label == 'ID':
            var_name = node.children[0].label
            type_var = ''
            if var_name in var_list:
                for var in var_list[var_name]:
                    if var[6] == escope:
                        type_var = var[2]
                        break

                if type_var == '':
                    for var in var_list[var_name]:
                        if var[6] == 'global':
                            type_var = var[2]
                            break

                list_node.append((var_name, type_var))
                return list_node
        elif node.label == 'numero':
            type_num = node.children[0].label

            if type_num == 'NUM_INTEIRO':
                num = int(node.descendants[1].label)
                type_num = 'inteiro'
            else:
                type_num = 'flutuante'
                num = float(node.descendants[1].label)

            list_node.append((num, type_num))
            return list_node

        list_node = encontrar_parametros(node, escope, list_node)

    return list_node


def chamada_funcao(line, func_list):
    for funcao in func_list:
        for func in func_list[funcao]:
            if func[5] <= line < func[6]:
                return func[0]


def linha_limpa(lst):
    return [t for t in (set(tuple(i) for i in lst))]


def variavel_escopo(i, escopo='global'):
    for var in var_list[i]:
        if var[6] == escopo:
            return var


def gerar_tabela_funcao(list, header, list_index):
    table = [header]

    for i in list:
        for func in list[i]:
            aux_array = []
            for index in list_index:
                aux_array.append(func[index])
            table.append(aux_array)

    return table


def gerar_tabela_variaveis(list, header, list_index):
    table = [header]

    for i in list:
        for func in list[i]:
            aux_array = []
            for index in list_index:
                if index == 4:
                    dim_tam = []
                    for j in range(len(func[index])):
                        if func[index][j][1] == 'NUM_PONTO_FLUTUANTE':
                            value = float(func[index][j][0])
                        else:
                            value = int(func[index][j][0])
                        dim_tam.append(value)
                    if func[3] == 0:
                        aux_array.append(len(dim_tam)+1)
                    else:
                        aux_array.append(len(dim_tam))
                elif index == 5:
                    dim_tam = 0
                    aux_array.append(dim_tam)
                else:
                    aux_array.append(func[index])
            table.append(aux_array)

    return table


def check_principal(func_list, message_list):
    if 'principal' not in func_list or not func_list['principal'][0][7]:
        message = (
            'ERROR', f'Erro: Função principal não declarada.')
        message_list.append(message)
    else:
        line_start = func_list['principal'][0][5]
        line_end = func_list['principal'][0][6]

        for call in func_list['principal'][0][-1]:
            if not line_start <= call[0] < line_end:
                message = (
                    'ERROR', f'Erro: Chamada para a função principal não permitida.')
                message_list.append(message)


def check_retorno_funcoes(func_list, message_list):
    message = ''
    for funcao in func_list:
        for func in func_list[funcao]:
            type_func = func[1]

            return_types = list()
            for type_return in func[4]:
                return_types.append(type_return[0])

            return_types = list(set(return_types))

            if type_func == 'vazio':
                if len(return_types) > 0:
                    if len(return_types) > 1:
                        message = ('ERROR',
                                   f'Erro: Função {funcao} deveria retornar vazio, mas retorna {return_types[0]} e {return_types[1]}.')
                    else:
                        message = ('ERROR',
                                   f'Erro: Função {funcao} deveria retornar vazio, mas retorna {return_types[0]}.')
            elif type_func == 'inteiro':
                if len(return_types) == 0:
                    message = ('ERROR',
                               f'Erro: Função {funcao} deveria retornar inteiro, mas retorna vazio.')
                else:
                    for type_return in return_types:
                        if type_return != 'inteiro' and type_return != 'ERROR':
                            message = ('ERROR',
                                       f'Erro: Função {funcao} deveria retornar inteiro, mas retorna flutuante.')
                            break
            elif type_func == 'flutuante':
                if len(return_types) == 0:
                    message = ('ERROR',
                               f'Erro: Função {funcao} deveria retornar flutuante, mas retorna vazio.')
                else:
                    for type_return in return_types:
                        if type_return != 'flutuante' and type_return != 'ERROR':
                            message = ('ERROR',
                                       f'Erro: Função {funcao} deveria retornar flutuante, mas retorna inteiro.')
                            break

            if message != '':
                message_list.append(message)


def check_chamada_funcoes(func_list, message_list):
    message = ''
    for funcao in func_list:
        for func in func_list[funcao]:
            if not func[-2]:
                message = ('ERROR',
                           f'Erro: Chamada a função {funcao} que não foi declarada.')
                message_list.append(message)

            else:
                if len(func[-1]) == 0 and funcao != 'principal':
                    message = ('WARNING',
                               f'Aviso: Função {funcao} declarada, mas não utilizada.')
                    message_list.append(message)
                else:
                    calls = 0
                    recursion = 0
                    for call_func in func[-1]:
                        func_called = chamada_funcao(call_func[0], func_list)
                        if func_called != funcao:
                            calls += 1
                        else:
                            recursion += 1

                    if funcao == 'principal':
                        calls += 1

                    if calls == 0:
                        message = ('WARNING',
                                   f'Aviso: Função {funcao} declarada, mas não utilizada.')
                        message_list.append(message)

                    elif recursion > 0:
                        message = ('WARNING',
                                   f'Aviso: Chamada recursiva para {funcao}.')
                        message_list.append(message)

                for call in func[-1]:
                    list_parameters = encontrar_parametros(call[1].children[2], func[0], list())

                    if len(list_parameters) > func[2]:
                        message = ('ERROR',
                                   f'Erro: Chamada à função {func[0]} com número de parâmetros maior que o declarado.')
                        message_list.append(message)
                    elif len(list_parameters) < func[2]:
                        message = ('ERROR',
                                   f'Erro: Chamada à função {func[0]} com número de parâmetros menor que o declarado.')
                        message_list.append(message)
                    else:
                        parameters = []
                        for func in func_list[call[1].descendants[1].label]:
                            for var_func in func[3]:
                                for index in range(len(var_list[var_func])):
                                    if var_list[var_func][index][6] == call[1].descendants[1].label:
                                        parameters.append((var_list[var_func][index][1], var_list[var_func][index][2]))
                                        break

                        for index in range(len(parameters)):
                            type_index = list_parameters[index][1]
                            if type_index == 'NUM_PONTO_FLUTUANTE':
                                type_index = 'flutuante'
                            else:
                                type_index = 'inteiro'
                            if parameters[index][1] != type_index:
                                message = ('WARNING',
                                           f'Aviso: Coerção implícita do valor passado para váriavel ' +
                                           f'‘{parameters[index][1]}‘ da função ‘{call[1].descendants[1].label}’.')
                                message_list.append(message)


def check_chamada_variaveis(var_list, message_list, root):
    all_leia_node = encontrar_nos(root, 'LEIA', list())

    for index in range(len(all_leia_node)):
        all_leia_node[index] = all_leia_node[index].anchestors[-1]
        escope_read = encontrar_nos_pais(all_leia_node[index], 'cabecalho', list())[0].descendants[1].label
        id_read = encontrar_nos(all_leia_node[index], 'ID', list())[0].children[0].label

        for var in var_list[id_read]:
            found = False
            if var[6] == escope_read:
                found = True
                if len(var[-1]) == 0:
                    message = ('WARNING',
                               f'Aviso: Variável ‘{id_read}’ declarada e não utilizada. ')
                    message_list.append(message)

            if not found:
                for var in var_list[id_read]:
                    if var[6] == 'global':
                        if len(var[-1]) == 0:
                            message = ('WARNING',
                                       f'Aviso: Variável ‘{id_read}’ declarada e não utilizada. ')
                            message_list.append(message)

    for variavel in var_list:
        for var in var_list[variavel]:
            if len(var[-1]) == 0: 
                var[7] = 'N'
                message = ('WARNING',
                           f'Aviso: Variável ‘{var[1]}’ declarada e não utilizada. ')
                message_list.append(message)

            if len(var_list[variavel]) > 1:
                for var2 in var_list[variavel]:
                    if var2 != var and var2[6] == var[6]:
                        message = ('WARNING', f'Aviso: Variável ‘{var2[1]}‘ já declarada anteriormente.')
                        message_list.append(message)


def check_atribucao_tipo(var_list, message_list, root):
    all_atribuicao_node = encontrar_nos(root, 'atribuicao', list())

    for index in range(len(all_atribuicao_node)):
        try:
            escope_read = encontrar_nos_pais(all_atribuicao_node[index], 'cabecalho', list())[0].descendants[1].label
        except:
            escope_read = 'global'

        right_side = encontrar_parametros(all_atribuicao_node[index], escope_read, list())
        left_side = right_side.pop(0)

        diferent_expression_type = False
        for unique_right in right_side:
            if unique_right[1] != left_side[1] and unique_right[1] != '':

                diferent_expression_type = unique_right[1]
                message = ('WARNING',
                           f'Aviso: Coerção implícita do valor de ‘{left_side[0]}’.')
                message_list.append(message)

        if diferent_expression_type and diferent_expression_type != left_side[1]:
            message = ('WARNING',
                       f'Aviso: Atribuição de tipos distintos ‘{left_side[0]}’ {left_side[1]} e ’{unique_right[0]}’ {diferent_expression_type}')
            message_list.append(message)


def check_variaveis_array(var_list, message_list):
    for variavel in var_list:
        for var in var_list[variavel]:
            if var[3] != 0:
                for dimension in var[4]:
                    dimension_number = 0
                    if dimension[1] != 'NUM_INTEIRO':
                        dimension_number = float(dimension[0])
                        message = ('ERROR',
                                   f'Erro: Índice de array ‘{var[1]}’ não inteiro.')
                        message_list.append(message)
                    else:
                        dimension_number = int(dimension[0])
                for call in var[-1]:
                    numero = encontrar_nos(call[1].descendants[3], 'numero', list())
                    if len(numero) > 0:
                        if len(encontrar_nos(numero[0], 'NUM_PONTO_FLUTUANTE', list())) > 0:
                            message = ('ERROR',
                                       f'Erro: Índice de array ‘{var[1]}’ não inteiro.')
                            message_list.append(message)
                        else:
                            numero = int(numero[0].descendants[-1].label)
                            if numero > dimension_number - 1:
                                message = ('ERROR',
                                           f'Erro: Índice de array ‘{var[1]}’ fora do intervalo (out of range).')
                                message_list.append(message)


def check_semantica(func_list, var_list, message_list, root):
    check_principal(func_list, message_list)
    check_retorno_funcoes(func_list, message_list)
    check_chamada_funcoes(func_list, message_list)
    check_chamada_variaveis(var_list, message_list, root)
    check_atribucao_tipo(var_list, message_list, root)
    check_variaveis_array(var_list, message_list)


def poda(root, labels):
    for node in root.children:
        poda(node, labels)

    if root.label in labels:
        dad = root.parent
        aux = []
        for children in dad.children:
            if children != root:
                aux.append(children)
        for children in root.children:
            aux.append(children)
        root.children = aux
        dad.children = aux

    if root.label == 'declaracao_funcao':
        corpo = root.children[1]
        aux = []
        for children in root.children:
            if children.label == 'fim':
                aux.append(corpo)
            if children != corpo:
                aux.append(children)
        root.children = aux

    if root.label == 'corpo' and len(root.children) == 0:
        dad = root.parent
        aux = []
        for children in dad.children:
            if children != root:
                aux.append(children)
        for children in root.children:
            aux.append(children)
        root.children = aux
        dad.children = aux

def ajustar_arvore(root, labels_ajuste):
    for node in root.children:
        ajustar_arvore(node, labels_ajuste)

    dad = root.parent
    aux = []

    if root.label == 'repita' and len(root.children) > 0:
        for children in root.children:
            if children.label != 'repita':
                aux.append(children)
        root.children = aux
        aux = []

    if root.label == 'e' and root.children[0].label == '&&':
        root.children = []
        root.label = '&&'
        root.name = '&&'

    if root.label == 'ou' and root.children[0].label == '||':
        root.children = []
        root.label = '||'
        root.name = '||'


    if root.label == 'se' and len(root.children) > 0:
        for children in root.children:
            if children.label != 'se':
                aux.append(children)

        root.children = aux
        aux = []

    if root.label == 'ATE':
        root.children = []
        root.label = 'até'
        root.name = 'até'

    if root.label == 'leia' or root.label == 'escreva' or root.label == 'retorna':
        if len(root.children) == 0:
            for children in dad.children:
                if children != root:
                    aux.append(children)

            dad.children = aux

def main():
    global root, func_list, var_list, message_list

    root, func_list, var_list, message_list = tppparser.main()

    for variavel in var_list:
        for index_var in range(len(var_list[variavel])):
            escopo_atual = var_list[variavel][index_var][6]
            if escopo_atual != 'global':
                len_call_list = len(var_list[variavel][index_var][-1])
                tuple_call_index = 0

                while tuple_call_index < len_call_list:
                    tuple_call = var_list[variavel][index_var][-1][tuple_call_index]
                    if func_list[escopo_atual][0][5] <= tuple_call[0] < func_list[escopo_atual][0][6]:
                        pass
                    else:
                        new_var_escopo = variavel_escopo(variavel, 'global')
                        new_var_escopo[-1].append(tuple_call)
                        var_list[variavel][index_var][-1].pop(tuple_call_index)
                        len_call_list -= 1
                        tuple_call_index -= 1

                    tuple_call_index += 1

    check_semantica(func_list, var_list, message_list, root)

    erros = 0
    message_list = linha_limpa(message_list)
    for message in message_list:
        print(message[-1])
        if message[0] == 'ERROR':
            erros += 1

    print('\n')

    sym_table = gerar_tabela_variaveis(var_list, ['Token', 'Lexema', 'Tipo', 'Dim', 'Tam_dim_1', 'Tam_dim_2', 'Escopo', 'Init', 'Linha'],[0, 1, 2, 3, 4, 5, 6, 7, 8])

    print(f'\x1B[3mTABELA DE SÍMBOLOS\x1B[0m\n{tabulate(sym_table, headers="firstrow", tablefmt="rounded_outline")}')
    
    print('\n')

    nos_remocao = ['inteiro', 'flutuante', 'acao', 'ID', 'var', 'lista_variaveis',
                        'INTEIRO', 'FLUTUANTE', 'NUM_INTEIRO', 'NUM_PONTO_FLUTUANTE',
                        'NUM_NOTACAO_CIENTIFICA', 'LEIA', 'RETORNA', 'ESCREVA', 'SE', 'ENTAO',
                        'SENAO', 'VIRGULA', 'ATRIBUICAO', 'FIM', 'REPITA', 'dois_pontos',
                        'tipo', 'abre_parentese', 'fecha_parentese', 'lista_declaracoes',
                        'declaracao', 'indice', 'numero', 'fator', 'virgula', 'abre_colchete',
                        'fecha_colchete', '(', ')', ':', ',', 'maior', 'menor','vezes',
                        'igual', 'menos', 'menor_igual', 'maior_igual', 'operador_logico',
                        'operador_multiplicacao', 'expressao', 'expressao_logica','vazio',
                        'expressao_simples', 'expressao_aditiva', 'expressao_multiplicativa',
                        'expressao_unaria', 'inicializacao_variaveis', 'atribuicao',
                        'operador_soma', 'mais', 'chamada_funcao', 'lista_argumentos',
                        'cabecalho', 'lista_parametros', 'func', 'ABRE_PARENTESE',
                        'FECHA_PARENTESE', 'ABRE_COLCHETE', 'FECHA_COLCHETE', 'DOIS_PONTOS',
                        'declaracao_variaveis', 'MAIS', 'MENOS', 'VEZES', 'DIVIDISAO',
                        'parametro']

    nos_ajuste = [':=', '+', '*', '-', '/']
    poda(root, nos_remocao)
    ajustar_arvore(root, nos_ajuste)
    UniqueDotExporter(root).to_picture(f"{sys.argv[1]}.prunned.unique.ast.png")
    print(f"Poda da árvore gerada\nArquivo de destino: {sys.argv[1]}.prunned.unique.ast.png")

    return root, message_list, func_list, var_list


if __name__ == '__main__':
    main()