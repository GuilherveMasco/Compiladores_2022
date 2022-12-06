import sys 
import subprocess

from llvmlite import ir
from llvmlite import binding as llvm

import tppsemantica

escopo = 'global'
var_list = {'global': []}
list_func = dict()
func_exit = False


def get_tipo(type):
    if type == "inteiro":
        default_type = ir.IntType(32)
    elif type == "flutuante":
        default_type = ir.FloatType()
    else:
        default_type = ir.VoidType()

    return default_type


def get_variavel_lista(var1):
    global escopo

    not_found = True
    if escopo in var_list:
        if any(var1 in var for var in var_list[escopo]):
            for var in var_list[escopo]:
                if var1 in var:
                    not_found = False
                    var1 = var[var1]
                    break
        else:
            for var in var_list['global']:
                if var1 in var:
                    not_found = False
                    var1 = var[var1]
                    break
    else:
        for var in var_list['global']:
            if var1 in var:
                not_found = False
                var1 = var[var1]
                break

    if not_found:
        return None

    return var1


def dec_variavel_global(node):
    flag = False
    var_type = node.children[0].name
    var_name = node.children[1].name
    var_dim = 0
    list_dim = list()

    for var in var_list[var_name]:
        if var[1] == var_type and var[4] == 'global':
            flag = True
            var_dim = var[2]
            list_dim = var[3]

    if flag:
        temp_var_type = get_tipo(var_type)
        if var_dim > 0:
            temp_var_type = get_tipo('inteiro')
            for dim in list_dim:
                temp_var_type = ir.ArrayType(temp_var_type, int(dim[0]))

        temp_var = ir.GlobalVariable(module, temp_var_type, var_name)

        if var_dim == 0:
            if var_type == 'inteiro':
                temp_var.initializer = ir.Constant(temp_var_type, 0)
            else:
                temp_var.initializer = ir.Constant(temp_var_type, 0.0)
        else:
            temp_var.initializer = ir.Constant(temp_var_type, None)

        temp_var.linkage = "common"
        temp_var.align = 4
        var_list['global'].append({var_name: temp_var})

    return flag


def dec_variavel_local(var, builder):
    temp_var_type = get_tipo(var[1])
    if var[2] > 0:
        temp_var_type = get_tipo('inteiro')
        for dim in var[3]:
            temp_var_type = ir.ArrayType(temp_var_type, int(dim[0]))

    temp_var = builder.alloca(temp_var_type, name=var[0])

    if var[2] == 0:
        if var[1] == 'inteiro':
            temp_var.initializer = ir.Constant(temp_var_type, 0)
        else:
            temp_var.initializer = ir.Constant(temp_var_type, 0.0)
    else:
        temp_var.initializer = ir.Constant(temp_var_type, None)

    temp_var.align = 4

    if var[4] not in var_list:
        var_list[var[4]] = []
    var_list[var[4]].append({var[0]: temp_var})


def retorno_codigo(node, builder, type_func, func):

    end_basic_block = func.append_basic_block('exit')

    builder.branch(end_basic_block)

    builder.position_at_end(end_basic_block)

    if len(node.children) > 1:
        var1 = node.children[0].name
        operation = node.children[1].name
        var2 = node.children[2].name

        var1 = get_variavel_lista(var1)
        var2 = get_variavel_lista(var2)

        if operation == '+':
            builder.ret(builder.add(var1, var2))
    else:
        flag_num = False
        if node.children[0].name.isnumeric():
            flag_num = True
            if type_func == 'inteiro':
                return_element = int(node.children[0].name)
            else:
                return_element = float(node.children[0].name)
        else:
            return_element = node.children[0].name

        if flag_num:
            value = ir.Constant(get_tipo(type_func), return_element)

            builder.ret(value)
        else:
            try:
                var = builder.load(get_variavel_lista(return_element))
            except:
                var = get_variavel_lista(return_element)
            builder.ret(var)


def leia_codigo(node, builder):
    var1 = node.children[0].name

    var1 = get_variavel_lista(var1)
    var_type = var1.type.pointee.intrinsic_name
    if var_type == 'i32':
        result_read = builder.call(leiaInteiro, args=[])
    else:
        result_read = builder.call(leiaFlutuante, args=[])

    builder.store(result_read, var1, align=4)


def escreva_codigo(node, builder):
    if len(node.children) == 1:
        var1 = node.children[0].name

        var1 = get_variavel_lista(var1)
        try:
            var_type = var1.type.pointee.intrinsic_name
        except:
            var_type = var1.type.intrinsic_name

        if var_type == 'i32':
            try:
                builder.call(escrevaInteiro, args=[var1])
            except:
                builder.call(escrevaInteiro, args=[builder.load(var1)])
        else:
            try:
                builder.call(escrevaFlutuante, args=[var1])
            except:
                builder.call(escrevaFlutuante, args=[builder.load(var1)])
    elif len(node.children) == 2:
        name_func = node.children[0].name
        type_func = list_func[name_func].type.pointee.return_type.intrinsic_name

        var1_arg = node.children[1].name
        var1_arg = get_variavel_lista(var1_arg)

        escreva_arg = builder.call(list_func[name_func], args=[builder.load(var1_arg)])
        if type_func == 'i32':
            builder.call(escrevaInteiro, args=[escreva_arg])
        else:
            builder.call(escrevaFlutuante, args=[escreva_arg])

    elif len(node.children) == 4:
        int_ty = ir.IntType(32)

        array_var_name = node.children[0].name
        index_var = node.children[2].name

        array_var = get_variavel_lista(array_var_name)
        index_var_load = builder.load(get_variavel_lista(index_var))
        array_var_pos = builder.gep(array_var, [int_ty(0), index_var_load], name=f'{array_var_name}[{index_var}]')
        temp_expression = builder.load(array_var_pos, align=4)

        type_array = array_var.type.pointee.element.intrinsic_name
        if type_array == 'i32':
            builder.call(escrevaInteiro, args=[temp_expression])
        else:
            builder.call(escrevaFlutuante, args=[temp_expression])


def atribuicao_codigo(node, builder):
    dad = node.parent

    float_ty = ir.FloatType()
    int_ty = ir.IntType(32)

    recive = True
    left = list()
    right = list()
    for children in dad.children:
        if children.name != ':=':
            if recive:
                left.append(children.name)
            else:
                right.append(children.name)
        else:
            recive = False

    var1 = None
    if len(left) == 1:
        var1 = get_variavel_lista(left[0])
    else:
        array_left = get_variavel_lista(left[0])
        if len(left) == 4:
            expression = builder.load(get_variavel_lista(left[2]))
            var1 = builder.gep(array_left, [int_ty(0), expression], name=left[0]+'_'+left[2])
        else:
            expressions = list()
            for indice in [left[2], left[4]]:
                if indice.isnumeric():
                    expressions.append(int_ty(indice))
                else:
                    expressions.append(builder.load(get_variavel_lista(indice)))

            operation = left[3]
            if operation == '+':
                expression = builder.add(expressions[0], expressions[1],
                                         name=left[0]+'_'+left[2]+left[3]+left[4], flags=())
            else:
                expression = builder.sub(expressions[0], expressions[1],
                                         name=left[0] + '_' + left[2] + left[3] + left[4], flags=())

            var1 = builder.gep(array_left, [int_ty(0), expression], name=left[0] + '_' + left[2] + left[3] + left[4])

    try:
        var_type = var1.type.pointee.intrinsic_name
    except:
        var_type = var1.type.intrinsic_name

    next_operation = 'add'
    if var_type == 'i32':
        expression = ir.Constant(ir.IntType(32), 0)
    else:
        expression = ir.Constant(ir.FloatType(), float(0))

    index = 0
    while index < len(right):
        if var_type == 'i32':
            temp_expression = ir.Constant(ir.IntType(32), 0)
        else:
            temp_expression = ir.Constant(ir.FloatType(), float(0))

        if right[index] != '+' and right[index] != '-' and right[index] != '*':

            if var_type != 'i32':
                if right[index] not in list_func and get_variavel_lista(right[index]) is None:
                    value = float(right[index])
                    temp_expression = ir.Constant(ir.FloatType(), value)
            if right[index].isnumeric():
                value = int(right[index])
                temp_expression = ir.Constant(ir.IntType(32), value)

            elif right[index] in list_func:
                num_vars = func_list[right[index]][0][2]
                func = list_func[right[index]]
                args = list()
                aux = 0

                for next_index in range(index + 1, index + num_vars + 1):
                    if right[next_index].isnumeric():
                        param_name = func_list[right[index]][0][3][aux]
                        type_param_name = var_list[param_name][0][1]
                        if type_param_name == 'inteiro':
                            value = int(right[next_index])
                            args.append(ir.Constant(ir.IntType(32), value))
                        else:
                            value = float(right[next_index])
                            args.append(ir.Constant(ir.FloatType(), value))

                    elif get_variavel_lista(right[next_index]) is None:
                        value = float(right[next_index])
                        args.append(ir.Constant(ir.FloatType(), value))

                    else:
                        args.append(builder.load(get_variavel_lista(right[next_index])))

                    aux += 1

                temp_expression = builder.call(func, args=args)
                index = index + num_vars
            elif get_variavel_lista(right[index]) is not None:
                if var_type == 'i32':
                    if len(right) > index + 1 and right[index + 1] == '[':
                        array_var = right[index]
                        index_var = right[index + 2]

                        array_var = get_variavel_lista(array_var)
                        index_var_load = builder.load(get_variavel_lista(index_var))
                        array_var_pos = builder.gep(array_var, [int_ty(0), index_var_load], name=f'{right[index]}[{right[index + 2]}]')
                        temp_expression = builder.load(array_var_pos, align=4)

                        index += 3
                    else:
                        try:
                            temp_expression = builder.load(get_variavel_lista(right[index]))
                        except:
                            temp_expression = get_variavel_lista(right[index])

            if next_operation == 'add':
                if expression.type.intrinsic_name != 'i32' or temp_expression.type.intrinsic_name != 'i32':
                    expression = builder.fadd(expression, temp_expression, name='expression', flags=())
                else:
                    expression = builder.add(expression, temp_expression, name='expression', flags=())
            if next_operation == 'sub':
                expression = builder.sub(expression, temp_expression, name='expression', flags=())
            elif next_operation == 'mul':
                expression = builder.mul(expression, temp_expression, name='expression', flags=())
        else:
            if right[index] == '+':
                next_operation = 'add'
            elif right[index] == '-':
                next_operation = 'sub'
            elif right[index] == '*':
                next_operation = 'mul'

        index += 1

    try:
        builder.store(expression, var1)
    except:
        builder.store(expression, var1)


def se_codigo(node, builder, type_func, func):
    if node.children[1].name == 'corpo':
        corps = 2
    else:
        corps = 1

    iftrue = func.append_basic_block('iftrue')
    iffalse = func.append_basic_block('iffalse')
    ifend = func.append_basic_block('ifend')

    comparation_list = list()
    comparation_list.append(node.children[2].name)
    type_comparation = node.children[3].name
    comparation_list.append(node.children[4].name)

    int_ty = ir.IntType(32)
    var_comper_right = builder.alloca(ir.IntType(32), name='var_comper_right')
    var_comper_left = builder.alloca(ir.IntType(32), name='var_comper_left')

    for index in range(len(comparation_list)):
        if comparation_list[index] in list_func:
            pass
        elif get_variavel_lista(comparation_list[index]) is None:
            value = int(comparation_list[index])
            builder.store(int_ty(value), var_comper_right)
            comparation_list[index] = ir.Constant(int_ty, int_ty(value))
        else:
            comparation_list[index] = get_variavel_lista(comparation_list[index])
            if comparation_list[index].type.intrinsic_name == 'p0i32':
                var_comper_left = comparation_list[index]
            else:
                builder.store(comparation_list[index], var_comper_left)

    if_state = builder.icmp_signed(type_comparation, var_comper_left, var_comper_right, name='if_test')
    builder.cbranch(if_state, iftrue, iffalse)

    builder.position_at_end(iftrue)
    arvore(node.children[0], builder, type_func, func)
    try:
        builder.branch(ifend)
    except:
        pass

    if corps == 2:
        builder.position_at_end(iffalse)
        arvore(node.children[1], builder, type_func, func)
        try:
            builder.branch(ifend)
        except:
            pass

    builder.position_at_end(ifend)


def repita_codigo(node, builder, type_func, func):

    comparation_list = list()
    comparation_list.append(node.children[2].name)
    type_comparation = node.children[3].name
    comparation_list.append(node.children[4].name)

    if type_comparation == '=':
        type_comparation = '=='

    int_ty = ir.IntType(32)
    var_comper = builder.alloca(ir.IntType(32), name='var_comper')
    any_value = True

    for index in range(len(comparation_list)):
        if comparation_list[index] in list_func:
            pass
        elif get_variavel_lista(comparation_list[index]) is None:
            any_value = False
            value = int(comparation_list[index])
            builder.store(int_ty(value), var_comper)
            comparation_list[index] = ir.Constant(ir.IntType(32), int_ty(value))
        else:
            comparation_list[index] = get_variavel_lista(comparation_list[index])

    loop = builder.append_basic_block('loop')
    lopp_val = builder.append_basic_block('loop_val')
    loop_end = builder.append_basic_block('loop_end')

    builder.branch(loop)

    builder.position_at_end(loop)
    arvore(node.children[0], builder, type_func, func)
    builder.branch(lopp_val)

    builder.position_at_end(lopp_val)
    if any_value:
        if comparation_list[0].type.is_pointer and not comparation_list[1].type.is_pointer:
            expression = builder.icmp_signed(type_comparation, builder.load(comparation_list[0]),
                                             comparation_list[1], name='expression')
        elif comparation_list[0].type.is_pointer and comparation_list[1].type.is_pointer:
            expression = builder.icmp_signed(type_comparation, builder.load(comparation_list[0]),
                                             builder.load(comparation_list[1]), name='expression')
        else:
            expression = builder.icmp_signed(type_comparation, comparation_list[0], comparation_list[1], name='expression')
    else:
        if comparation_list[0].type.is_pointer and var_comper.type.is_pointer:
            expression = builder.icmp_signed(type_comparation, builder.load(comparation_list[0]),
                                             builder.load(var_comper), name='expression')
        elif not comparation_list[0].type.is_pointer and var_comper.type.is_pointer:
            expression = builder.icmp_signed(type_comparation, comparation_list[0],
                                             builder.load(var_comper), name='expression')

    if type_comparation == '==':
        builder.cbranch(expression, loop_end, loop)
    else:
        builder.cbranch(expression, loop, loop_end)
    builder.position_at_end(loop_end)


def chamada_funcao_codigo(node, builder):
    int_ty = ir.IntType(32)
    func_name = node.name

    node_params = []
    dad = node.parent
    for children in dad.children:
        if children != node:
            node_params.append(children)

    if len(node_params) == 1:
        param = node_params[0].name

        if param.isnumeric():
            func_aux = list_func[func_name]
            param_type = func_aux.args[0].type.intrinsic_name
            if param_type == 'i32':
                value = int_ty(int(param))
            else:
                value = ir.Constant(ir.FloatType(), float(param))
            builder.call(func_aux, [value])
        else:
            pass
    else:
        pass


def arvore(node, builder, type_func, func):
    global func_exit
    if node.name == 'retorna':
        func_exit = True
        retorno_codigo(node, builder, type_func, func)
        return
    if node.name == 'leia':
        leia_codigo(node, builder)
        return
    if node.name == 'escreva':
        escreva_codigo(node, builder)
        return
    if node.name == ':=':
        atribuicao_codigo(node, builder)
        return
    if node.name == 'se':
        se_codigo(node, builder, type_func, func)
        return
    if node.name == 'repita':
        repita_codigo(node, builder, type_func, func)
        return
    if node.name in list_func:
        chamada_funcao_codigo(node, builder)
        return

    for children in node.children:
        arvore(children, builder, type_func, func)


def dec_funcoes(node):
    global escopo, func_exit
    func_exit = False
    type_func = node.children[0].name
    if type_func != 'inteiro' and type_func != 'flutuante':
        type_func = 'vazio'

    if type_func != 'vazio':
        name_func = node.children[1].name
    else:
        name_func = node.children[-2].name

    escopo = name_func
    func_return_type = get_tipo(type_func)
    list_param_func = list()
    for var_param in func_list[name_func][0][3]:
        for var in var_list[var_param]:
            if var[4] == name_func:
                list_param_func.append(get_tipo(var[1]))

    t_func = ir.FunctionType(func_return_type, list_param_func)

    if name_func == 'principal':
        func = ir.Function(module, t_func, name='main')
    else:
        func = ir.Function(module, t_func, name=name_func)

    for index in range(len(func_list[name_func][0][3])):
        func.args[index].name = func_list[name_func][0][3][index]
        if name_func not in var_list:
            var_list[name_func] = []
        var_list[name_func].append({func_list[name_func][0][3][index]: func.args[index]})

    entry_block = func.append_basic_block('entry')

    builder = ir.IRBuilder(entry_block)

    for element in var_list:
        for var in var_list[element]:
            if var[4] == name_func:
                if var[0] not in func_list[var[4]][0][3]:
                    dec_variavel_local(var, builder)

    arvore(node, builder, type_func, func)

    if not func_exit:
        end_basic_block = func.append_basic_block('exit')

        builder.branch(end_basic_block)

        builder.position_at_end(end_basic_block)

        if type_func != 'vazio':
            Zero64 = ir.Constant(func_return_type, 0)

            returnVal = builder.alloca(func_return_type, name='retorno')
            builder.store(Zero64, returnVal)

            returnVal_temp = builder.load(returnVal, name='ret_temp', align=4)
            builder.ret(returnVal_temp)
        else:
            builder.ret_void()

    list_func[name_func] = func
    escopo = 'global'


def geracao(root):
    for children in root.children:
        if children.name == 'declaracao_variaveis':
            dec_variavel_global(children)
        if children.name == 'declaracao_funcao':
            dec_funcoes(children)


if __name__ == '__main__':
    root, message_list, func_list, var_list = tppsemantica.main()

    for message in message_list:
        if message[0] == 'ERROR':
            print('Não foi possível gerar o código intermediário devido a erros no código!')
            exit()

    file_name = sys.argv[1].split('/')[-1].split('.')[0]

    llvm.initialize()
    llvm.initialize_all_targets()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    module = ir.Module(f'{file_name}.bc')
    module.triple = llvm.get_default_triple()

    target = llvm.Target.from_triple(module.triple)
    target_machine = target.create_target_machine()

    module.data_layout = target_machine.target_data

    escrevaInteiro = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.IntType(32)]), name="escrevaInteiro")
    escrevaFlutuante = ir.Function(module, ir.FunctionType(ir.VoidType(), [ir.FloatType()]), name="escrevaFlutuante")
    leiaInteiro = ir.Function(module, ir.FunctionType(ir.IntType(32), []), name="leiaInteiro")
    leiaFlutuante = ir.Function(module, ir.FunctionType(ir.FloatType(), []), name="leiaFlutuante")

    geracao(root)

    arquivo = open(f'geracao-codigo-testes/{file_name}.ll', 'w')
    print(str(module))
    arquivo.write(str(module))
    arquivo.close()

    bashCommands = ["clang -emit-llvm -S io.c", "llc -march=x86-64 -filetype=obj io.ll -o io.o",
                    f'llvm-link geracao-codigo-testes/{file_name}.ll io.ll -o geracao-codigo-testes/{file_name}.bc',
                    f'clang geracao-codigo-testes/{file_name}.bc -o geracao-codigo-testes/{file_name}.o',
                    f'rm geracao-codigo-testes/{file_name}.bc']
    for bashCommand in bashCommands:
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()