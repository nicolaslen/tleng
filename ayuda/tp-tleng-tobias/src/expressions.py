SALTO_DE_LINEA = '\n'
TABULADO = '\t'
ESPACIO = ' '
TIPOS = {
    'bool': 'BOOL',
    'cadena': 'CADENA',
    'numerico': 'NUMERICO',
    'registro': 'REGISTRO',
    'vector_bool': 'B-VECTOR',
    'vector_cadena': 'C-VECTOR',
    'vector_numerico': 'N-VECTOR',
    'vector_registro': 'R-VECTOR',
    'vector_vectores': 'V-VECTOR',
}

TIPOS_VECTOR = {
    TIPOS['bool']: TIPOS['vector_bool'],
    TIPOS['cadena']: TIPOS['vector_cadena'],
    TIPOS['numerico']: TIPOS['vector_numerico'],
    TIPOS['registro']: TIPOS['vector_registro'],
    TIPOS['vector_bool']: TIPOS['vector_vectores'],
    TIPOS['vector_cadena']: TIPOS['vector_vectores'],
    TIPOS['vector_numerico']: TIPOS['vector_vectores'],
    TIPOS['vector_registro']: TIPOS['vector_vectores'],
}

TIPOS_ASOCIADOS_A_TIPOS_DE_VECTOR = {
    TIPOS['vector_bool']: TIPOS['bool'],
    TIPOS['vector_cadena']: TIPOS['cadena'],
    TIPOS['vector_numerico']: TIPOS['numerico'],
    TIPOS['vector_registro']: TIPOS['registro'],
}


class DiccionarioDeTipos(object):
    """
        Usamos un patrón Singleton para el diccionario de tipos porque era mucho más sencillo tenerlo
        así que ir pasándolo por el evaluate todo el tiempo, de esta forma nos aseguramos un setting
        global de variables cada vez que se parsea un programa (el new() se usa en Program únicamente)

        Las variables se van guardando en el diccionario variablesDefinidas a medida que se utilice el
        método definir_variable() y se obtiene el tipo para una variable con el método tipo_de_variable().

        Por ejemplo:
            a = 3;
            b = "test";
            ==> variablesDefinidas == {a: 'NUMERICO', b: 'CADENA'}

        Un caso más particular es el de los registros; si se guarda un registro en una variable, guardamos
        el tipo de cada atributo también:

            a = {id: 3, nombre: "test"};
            ==> variablesDefinidas == {a: 'REGISTRO', a.id: 'NUMERICO', a.nombre: 'CADENA'}

        Known bugs:
         - manejar vectores de vectores se nos complicó, por ahora el tipo sería únicamente V-VECTOR
           (vector de vectores) y los checkeos para ver que todos los elementos de una lista son del
           mismo tipo funcionarían hasta un solo vector de vectores. Es decir, si hay un vector de
           vector de vectores (y así...) no funcionaría bien el checkeo de tipos porque el tipo
           siempre sería V-VECTOR y no V-N-VECTOR, etc... no fue fácil de pensar y abandonamos la
           idea por salud.
    """
    diccionario_de_tipos = None

    def __init__(self):
        self.variablesDefinidas = {}

    @classmethod
    def new(cls):
        nuevo_diccionario_de_tipos = cls()
        cls.diccionario_de_tipos = nuevo_diccionario_de_tipos
        return nuevo_diccionario_de_tipos

    @classmethod
    def get_instance(cls):
        if not cls.diccionario_de_tipos:
            raise Exception('Deberías haber creado una instancia antes!')
        return cls.diccionario_de_tipos

    def tipo_de_variable(self, nombre):
        if '[' in nombre:
            # Si piden el tipo de una posicion X de un vector, devuelvo el tipo asociado al tipo del vector
            return TIPOS_ASOCIADOS_A_TIPOS_DE_VECTOR.get(self.variablesDefinidas.get(nombre.split('[', 1)[0]), None)
        else:
            return self.variablesDefinidas.get(nombre, None)

    def definir_variable(self, nombre, valor):
        if nombre in self.variablesDefinidas.keys():
            self._eliminar_definiciones_de_variables_obsoletas(nombre)

        self.variablesDefinidas[nombre] = valor

    def _eliminar_definiciones_de_variables_obsoletas(self, nombre):
        claves_a_eliminar = []
        for nombre_variable in self.variablesDefinidas.keys():
            if nombre_variable.startswith(nombre + '.'):
                claves_a_eliminar.append(nombre_variable)

        for clave_a_eliminar in claves_a_eliminar:
            self.variablesDefinidas.pop(clave_a_eliminar, None)


class Program(object):
    def __init__(self, statement_ls):
        self.diccionario_de_tipos = DiccionarioDeTipos.new()
        self.statement_ls = statement_ls

    def evaluate(self):
        return self.statement_ls.evaluate(0)


class NombreVariable(object):
    def __init__(self, value):
        self.value = str(value)

    @property
    def tipo(self):
        return DiccionarioDeTipos.get_instance().tipo_de_variable(self.value)

    def evaluate(self, tabulado=0):
        return self.value


class Numerico(object):
    def __init__(self, value):
        self.value = str(value)
        self.tipo = TIPOS['numerico']

    def evaluate(self, tabulado=0):
        return self.value


class Cadena(object):
    def __init__(self, value):
        self.value = str(value)
        self.tipo = TIPOS['cadena']

    def evaluate(self, tabulado=0):
        return self.value


class TrueFalse(object):
    def __init__(self, value):
        self.value = str(value)
        self.tipo = TIPOS['bool']

    def evaluate(self, tabulado=0):
        return self.value


class Token(object):
    def __init__(self, token):
        self.token = str(token)

    def evaluate(self, tabulado=0):
        return self.token


class FuncionMultiplicacionEscalar(object):
    def __init__(self, multiplicacion_escalar):
        self.multiplicacion_escalar = str(multiplicacion_escalar)
        self.tipo_parametros = [(TIPOS['vector_numerico']), (TIPOS['numerico']), (TIPOS['bool'])]
        self.cantidad_de_parametros_opcionales = 1
        self.tipo = TIPOS['vector_numerico']

    def evaluate(self):
        return self.multiplicacion_escalar


class FuncionCapitalizar(object):
    def __init__(self, capitalizar):
        self.capitalizar = str(capitalizar)
        self.tipo_parametros = [(TIPOS['cadena'])]
        self.cantidad_de_parametros_opcionales = 0
        self.tipo = TIPOS['cadena']

    def evaluate(self):
        return self.capitalizar


class FuncionColineales(object):
    def __init__(self, capitalizar):
        self.capitalizar = str(capitalizar)
        self.tipo_parametros = [(TIPOS['vector_numerico']), (TIPOS['vector_numerico'])]
        self.cantidad_de_parametros_opcionales = 0
        self.tipo = TIPOS['bool']

    def evaluate(self):
        return self.capitalizar


class FuncionPrint(object):
    def __init__(self, print_fn):
        self.print_fn = str(print_fn)
        self.tipo_parametros = [list(TIPOS.values()) + [None]]
        self.cantidad_de_parametros_opcionales = 0
        self.tipo = None

    def evaluate(self):
        return self.print_fn


class FuncionLength(object):
    def __init__(self, length_fn):
        self.length_fn = str(length_fn)
        self.tipo_parametros = [(TIPOS['cadena'], TIPOS['vector_numerico'], TIPOS['vector_registro'],
                                 TIPOS['vector_cadena'], TIPOS['vector_bool'])]
        self.cantidad_de_parametros_opcionales = 0
        self.tipo = TIPOS['numerico']

    def evaluate(self):
        return self.length_fn


class Comentario(object):
    def __init__(self, comment, is_inline):
        self.comment = str(comment)
        self.is_inline = is_inline

    def evaluate(self, tabulado=0):
        return TABULADO * tabulado + self.comment + SALTO_DE_LINEA


class StatementListComentario(object):
    def __init__(self, st_list, comment):
        self.st_list = st_list
        self.comment = comment

    def evaluate(self, tabulado=0):
        if self.comment.is_inline:
            return self.st_list.evaluate(tabulado)[:-1] + ESPACIO + self.comment.evaluate(tabulado)
        else:
            return self.st_list.evaluate(tabulado) + self.comment.evaluate(tabulado)


class BinaryNonTerminalStatement(object):
    def __init__(self, ls, statement):
        self.ls = ls
        self.statement = statement

    def evaluate(self, tabulado=0):
        return self.ls.evaluate(tabulado) + self.statement.evaluate(tabulado)


class Statement(object):
    def __init__(self, statement):
        self.diccionario_de_tipos = DiccionarioDeTipos()
        self.statement = statement

    def evaluate(self, tabulado=0):
        return TABULADO * tabulado + self.statement.evaluate(tabulado) + SALTO_DE_LINEA


class BinaryNonTerminalUnaryOperatorExpression(object):
    def __init__(self, unary_op, unary_exp):
        self.unary_op = unary_op
        self.unary_exp = unary_exp
        self.tipo = None

    def evaluate(self, tabulado=0):
        evaluation = self.unary_op.evaluate(tabulado) + self.unary_exp.evaluate(tabulado)
        self.tipo = self.unary_exp.tipo
        return evaluation


class TokenNot(object):
    def __init__(self, token_not):
        self.token_not = token_not

    def evaluate(self, tabulado=0):
        return self.token_not + ESPACIO


class ComentarioCommentList(object):
    def __init__(self, comment, comment_ls):
        self.comment = comment
        self.comment_ls = comment_ls

    def evaluate(self, tabulado=0):
        return self.comment.evaluate(tabulado) + self.comment_ls.evaluate(tabulado)


class Block(object):
    def __init__(self, block):
        self.block = block

    def evaluate(self, tabulado=0):
        return self.block.evaluate(tabulado)

    def is_single_statement(self):
        return isinstance(self.block, SingleStatement)


class SingleStatement(object):
    def __init__(self, single_statement):
        self.single_statement = single_statement

    def evaluate(self, tabulado=0):
        tabulado += 1
        # se toma solo lo primero porque tiene el salto de linea del statement que lo contiene
        evaluacion = SALTO_DE_LINEA + self.single_statement.evaluate(tabulado)[:-1]
        return evaluacion


class BracketedStatementList(object):
    def __init__(self, bracketed_statement_list):
        self.bracketed_statement_list = bracketed_statement_list

    def evaluate(self, tabulado=0):
        tabulado += 1
        evaluacion = self.bracketed_statement_list.evaluate(tabulado)
        return evaluacion


class LlaveLlave(object):
    def __init__(self, open, close):
        self.open = open
        self.close = close

    def evaluate(self, tabulado=0):
        return self.open + self.close


class LlaveStatementListLlave(object):
    def __init__(self, open, st_list, close):
        self.open = open
        self.st_list = st_list
        self.close = close

    def evaluate(self, tabulado=0):
        return self.open + SALTO_DE_LINEA + self.st_list.evaluate(tabulado) + TABULADO * (tabulado - 1) + self.close


class ExpressionPuntoYComa(object):
    def __init__(self, exp, punto_y_coma):
        self.exp = exp
        self.punto_y_coma = punto_y_coma
        self.tipo = None

    def evaluate(self, tabulado=0):
        evaluation = self.exp.evaluate(tabulado) + self.punto_y_coma
        self.tipo = self.exp.tipo
        return evaluation


class ExpressionAssignmentExp(object):
    def __init__(self, assignment_exp):
        self.assignment_exp = assignment_exp
        self.tipo = None

    def evaluate(self, tabulado=0):
        evaluation = self.assignment_exp.evaluate(tabulado)
        self.tipo = self.assignment_exp.tipo
        return evaluation


class ExpressionComaAssignmentExp(object):
    def __init__(self, exp, coma, assignment_exp):
        self.exp = exp
        self.coma = coma
        self.assignment_exp = assignment_exp
        self.tipo = None

    def evaluate(self, tabulado=0):
        evaluation = self.exp.evaluate(tabulado) + self.coma + ESPACIO + \
                     self.assignment_exp.evaluate(tabulado)
        self.tipo = self.assignment_exp.tipo
        return evaluation


class FuncExpEncerrada(object):
    def __init__(self, open, exp, close):
        self.open = open
        self.exp = exp
        self.close = close
        self.tipo = None

    def evaluate(self, tabulado=0):
        evaluation = self.open + self.exp.evaluate(tabulado) + self.close
        self.tipo = self.exp.tipo
        return evaluation


class VectorExpEncerrada(object):
    def __init__(self, open, vector_exp, close):
        self.open = open
        self.vector_exp = vector_exp
        self.close = close
        self.tipo = None
        self.tipos_internos = {}

    def evaluate(self, tabulado=0):
        evaluation = self.open + self.vector_exp.evaluate(tabulado) + self.close
        self.tipo = self.vector_exp.tipo
        self.tipos_internos = self.vector_exp.tipos_internos
        return evaluation


class RegistroExpEncerrada(object):
    def __init__(self, open, reg_exp, close):
        self.open = open
        self.reg_exp = reg_exp
        self.close = close
        self.tipo = TIPOS['registro']
        self.tipos_internos = {}

    def evaluate(self, tabulado=0, nombre_variable=None):
        evaluation = self.open + self.reg_exp.evaluate(tabulado, nombre_variable) + self.close
        self.tipos_internos = self.reg_exp.tipos_y_variables
        return evaluation


class VectorConditionalExpComaVectorExp(object):
    def __init__(self, conditional_exp, coma, vector_exp, linea_error):
        self.conditional_exp = conditional_exp
        self.coma = coma
        self.vector_exp = vector_exp
        self.tipo = None
        self.tipos_internos = []
        self.linea_error = linea_error

    def _assert_tipo_de_operandos(self):
        if self.conditional_exp.tipo != self.vector_exp.conditional_exp.tipo:
            raise TypeError('Todos los valores de una lista deben ser del mismo tipo (línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.conditional_exp.evaluate(tabulado) + self.coma + ESPACIO + self.vector_exp.evaluate(tabulado)
        self._assert_tipo_de_operandos()
        self.tipo = TIPOS_VECTOR[self.conditional_exp.tipo]
        self.tipos_internos = self.vector_exp.tipos_internos
        self.tipos_internos.append(self.conditional_exp.tipo)
        return evaluation


class VectorConditionalExp(object):
    def __init__(self, conditional_exp):
        self.conditional_exp = conditional_exp
        self.tipo = None
        self.tipos_internos = []

    def evaluate(self, tabulado=0):
        evaluation = self.conditional_exp.evaluate(tabulado)
        self.tipo = TIPOS_VECTOR[self.conditional_exp.tipo]
        self.tipos_internos.append(self.conditional_exp.tipo)
        return evaluation


class NombreVarDosPuntosExp(object):
    def __init__(self, var, dos_puntos, exp):
        self.var = var
        self.dos_puntos = dos_puntos
        self.exp = exp
        self.tipos_y_variables = {}

    def evaluate(self, tabulado=0, nombre_variable=None):
        evaluation = self.var.evaluate() + self.dos_puntos + self.exp.evaluate(tabulado)
        if nombre_variable is not None:
            DiccionarioDeTipos.get_instance().definir_variable(nombre_variable + '.' + self.var.value, self.exp.tipo)

        self.tipos_y_variables[self.var.value] = self.exp.tipo
        return evaluation


class NombreVarDosPuntosExpComaRegExp(object):
    def __init__(self, var, dos_puntos, exp, coma, reg_exp):
        self.var = var
        self.dos_puntos = dos_puntos
        self.exp = exp
        self.coma = coma
        self.reg_exp = reg_exp
        self.tipos_y_variables = {}

    def evaluate(self, tabulado=0, nombre_variable=None):
        evaluation = self.var.evaluate() + self.dos_puntos + self.exp.evaluate(tabulado) + self.coma + ESPACIO + \
                     self.reg_exp.evaluate(tabulado, nombre_variable)
        if nombre_variable is not None:
            DiccionarioDeTipos.get_instance().definir_variable(nombre_variable + '.' + self.var.value, self.exp.tipo)

        self.tipos_y_variables.update(self.reg_exp.tipos_y_variables)
        self.tipos_y_variables[self.var.value] = self.exp.tipo
        return evaluation


class PostFixExpCorcheteExpCorchete(object):
    def __init__(self, post_exp, open, exp, close, linea_error):
        self.post_exp = post_exp
        self.open = open
        self.exp = exp
        self.close = close
        self.tipo = None
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        # TODO - deberian ser solo ints ?
        if self.exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un tipo numérico como índice del vector, no un tipo "%s" (línea %s)' %
                            (self.exp.tipo, self.linea_error))

    def evaluate(self, tabulado=0):
        evaluation = self.post_exp.evaluate(tabulado) + self.open + self.exp.evaluate(tabulado) + self.close
        self._assert_tipos_de_operandos()
        if isinstance(self.post_exp, VectorExpEncerrada):
            self.tipo = self.post_exp.tipos_internos[0]
        else:
            self.tipo = DiccionarioDeTipos.get_instance().tipo_de_variable(evaluation)
        return evaluation


class FunctionExpParenParen(object):
    def __init__(self, function_exp, open, close, linea_error):
        self.function_exp = function_exp
        self.open = open
        self.close = close
        self.tipo = None
        self.linea_error = linea_error

    def _assert_cantidad_de_parametros_de_funcion_es_0(self):
        function_exp = self.function_exp
        cantidad_de_parametros = len(function_exp.tipo_parametros) - function_exp.cantidad_de_parametros_opcionales
        if cantidad_de_parametros is not 0:
            raise TypeError('%s() lleva al menos %s parámetros (0 dados) (línea %s)' % (function_exp.evaluate(),
                                                                                        cantidad_de_parametros,
                                                                                        self.linea_error))

    def evaluate(self, tabulado=0):
        evaluation = self.function_exp.evaluate() + self.open + self.close
        self._assert_cantidad_de_parametros_de_funcion_es_0()
        self.tipo = self.function_exp.tipo
        return evaluation


class FunctionExpParenArgumentExpListParen(object):
    def __init__(self, function_exp, open, arg_exp_ls, close, linea_error):
        self.function_exp = function_exp
        self.open = open
        self.arg_exp_ls = arg_exp_ls
        self.close = close
        self.tipo = None
        self.linea_error = linea_error

    def _assert_cantidad_de_parametros_pasada_es_correcta(self):
        function_exp = self.function_exp
        arg_exp_ls = self.arg_exp_ls
        cantidad_de_parametros = len(function_exp.tipo_parametros)
        cantidad_de_parametros_pasados = arg_exp_ls.cantidad
        cantidad_de_parametros_opcionales = function_exp.cantidad_de_parametros_opcionales
        minima_cantidad_de_parametros = cantidad_de_parametros - cantidad_de_parametros_opcionales

        no_pase_todos_los_parametros = cantidad_de_parametros_pasados != cantidad_de_parametros
        hay_parametros_opcionales = function_exp.cantidad_de_parametros_opcionales > 0

        if hay_parametros_opcionales:
            no_pase_la_minima_cantidad_de_parametros = cantidad_de_parametros_pasados != minima_cantidad_de_parametros
            if no_pase_todos_los_parametros and no_pase_la_minima_cantidad_de_parametros:
                raise TypeError('%s() lleva al menos %s parámetros (%s dados) (línea %s)' %
                                (function_exp.evaluate(), minima_cantidad_de_parametros, cantidad_de_parametros_pasados,
                                 self.linea_error))
        else:
            if no_pase_todos_los_parametros:
                raise TypeError('%s() lleva exactamente %s parámetros (%s dados) (línea %s)' %
                                (function_exp.evaluate(), cantidad_de_parametros, cantidad_de_parametros_pasados,
                                 self.linea_error))

    def _assert_el_tipo_de_los_parametros_pasados_es_correcto(self):
        function_exp = self.function_exp
        arg_exp_ls = self.arg_exp_ls
        tipos_de_parametros_permitidos = function_exp.tipo_parametros
        tipos_de_parametros_pasados = arg_exp_ls.tipos
        tipos_correctos = list(map(lambda x, y: y in x, tipos_de_parametros_permitidos, tipos_de_parametros_pasados))
        if not all(tipos_correctos):
            primer_indice_tipo_incorrecto = tipos_correctos.index(False)
            raise TypeError('Se esperaban tipos "%s" como parámetro nº%s para %s() (línea %s)' %
                            (tipos_de_parametros_permitidos[primer_indice_tipo_incorrecto],
                             primer_indice_tipo_incorrecto + 1, function_exp.evaluate(), self.linea_error))

    def evaluate(self, tabulado=0):
        evaluation = self.function_exp.evaluate() + self.open + self.arg_exp_ls.evaluate(tabulado) + self.close
        self._assert_cantidad_de_parametros_pasada_es_correcta()
        self._assert_el_tipo_de_los_parametros_pasados_es_correcto()
        self.tipo = self.function_exp.tipo
        return evaluation


class ArgumentExpLs(object):
    def __init__(self, argument_expression_ls):
        self.argument_expression_ls = argument_expression_ls
        self.cantidad = self.argument_expression_ls.cantidad
        self.tipos = []

    def evaluate(self, tabulado=0):
        evaluation = self.argument_expression_ls.evaluate(tabulado)
        self.tipos = self.argument_expression_ls.tipos
        return evaluation


class PostFixExpPuntoNombreVar(object):
    def __init__(self, post_exp, punto, var, linea_error):
        self.post_exp = post_exp
        self.punto = punto
        self.var = var
        self.tipo = None
        self.linea_error = linea_error

    def evaluate(self, tabulado=0):
        evaluation = self.post_exp.evaluate(tabulado) + self.punto + self.var
        if isinstance(self.post_exp, RegistroExpEncerrada):
            if self.var not in self.post_exp.tipos_internos.keys():
                raise AttributeError('No existe el atributo %s en el registro (línea %s)' %
                                     (self.var, self.linea_error))
            else:
                self.tipo = self.post_exp.tipos_internos[self.var]
        else:
            self.tipo = DiccionarioDeTipos.get_instance().tipo_de_variable(evaluation)
        return evaluation


class PostFixExpAuto(object):
    def __init__(self, post_exp, auto, linea_error):
        self.post_exp = post_exp
        self.auto = auto
        self.tipo = TIPOS['numerico']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        post_exp = self.post_exp
        if post_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico para una operación de autoincremento o '
                            'autodecremento (línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.post_exp.evaluate(tabulado) + self.auto
        self._assert_tipos_de_operandos()
        return evaluation


class ArgumentExpLsAssigmentExp(object):
    def __init__(self, assignment_exp):
        self.assignment_exp = assignment_exp
        self.cantidad = 1
        self.tipos = []

    def evaluate(self, tabulado=0):
        evaluation = self.assignment_exp.evaluate(tabulado)
        self.tipos.append(self.assignment_exp.tipo)
        return evaluation


class ArgumentExpLsComaAssigmentExp(object):
    def __init__(self, argument_exp, coma, assigment_exp):
        self.argument_exp = argument_exp
        self.coma = coma
        self.assigment_exp = assigment_exp
        self.cantidad = argument_exp.cantidad + 1
        self.tipos = []

    def evaluate(self, tabulado=0):
        evaluation = self.argument_exp.evaluate(tabulado) + self.coma + ESPACIO + self.assigment_exp.evaluate(tabulado)
        self.tipos = self.argument_exp.tipos + [self.assigment_exp.tipo]
        return evaluation


class AutoUnaryExp(object):
    def __init__(self, auto, unary_exp):
        self.auto = auto
        self.unary_exp = unary_exp
        self.tipo = TIPOS['numerico']

    def _assert_tipos_de_operandos(self):
        unary_exp = self.unary_exp
        if unary_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico para una operación de '
                            'autoincremento/autodecremento')

    def evaluate(self, tabulado=0):
        evaluation = self.auto + self.unary_exp.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class MultiplicativeExpOpUnaryExp(object):
    def __init__(self, multiplicative_exp, op, unary_exp, linea_error):
        self.multiplicative_exp = multiplicative_exp
        self.op = op
        self.unary_exp = unary_exp
        self.tipo = TIPOS['numerico']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        multiplicative_exp = self.multiplicative_exp
        unary_exp = self.unary_exp
        if multiplicative_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como primer operando en una operación '
                            'multiplicativa (línea %s)' % self.linea_error)
        if unary_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como segundo operando en una operación '
                            'multiplicativa (línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.multiplicative_exp.evaluate(tabulado) + ESPACIO + self.op + ESPACIO + self.unary_exp.evaluate(
            tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class CongruenceExpModuloMultiplicativeExpression(object):
    def __init__(self, congruence_exp, modulo_op, multiplicative_exp, linea_error):
        self.congruence_exp = congruence_exp
        self.modulo_op = modulo_op
        self.multiplicative_exp = multiplicative_exp
        self.tipo = TIPOS['numerico']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        # TODO - deberiamos preguntar si son int ambos para este caso? si no, no hacia falta separarlo de los multiplicative
        congruence_exp = self.congruence_exp
        multiplicative_exp = self.multiplicative_exp
        if congruence_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como primer operando en una operación de '
                            'congruencia (línea %s)' % self.linea_error)
        if multiplicative_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como segundo operando en una operación de '
                            'congruencia (línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.congruence_exp.evaluate(
            tabulado) + ESPACIO + self.modulo_op + ESPACIO + self.multiplicative_exp.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class AdditiveExpOpCongruenceExp(object):
    def __init__(self, additive_exp, op, congruence_exp, linea_error):
        self.additive_exp = additive_exp
        self.op = op
        self.congruence_exp = congruence_exp
        self.tipo = None
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        additive_exp = self.additive_exp
        congruence_exp = self.congruence_exp

        if self.op == '+':
            if congruence_exp.tipo == TIPOS['cadena'] and additive_exp.tipo != TIPOS['cadena']:
                raise TypeError('Se espera un operando de tipo cadena como primer operando en una operación aditiva '
                                '(línea %s)' % self.linea_error)
            if additive_exp.tipo == TIPOS['cadena'] and congruence_exp.tipo != TIPOS['cadena']:
                raise TypeError('Se espera un operando de tipo cadena como segundo operando en una operación aditiva'
                                ' (línea %s)' % self.linea_error)
            if additive_exp.tipo == congruence_exp.tipo == TIPOS['cadena']:
                return

        if additive_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como primer operando en una operación aditiva '
                            '(línea %s)' % self.linea_error)
        if congruence_exp.tipo != TIPOS['numerico']:
            raise TypeError('Se espera un operando de tipo numérico como segundo operando en una operación aditiva '
                            '(línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.additive_exp.evaluate(tabulado) + ESPACIO + self.op + ESPACIO + \
                     self.congruence_exp.evaluate(tabulado)
        self.tipo = self.additive_exp.tipo
        self._assert_tipos_de_operandos()
        return evaluation


class RelationalExpRelAdditiveExp(object):
    def __init__(self, relational_exp, rel, additive_exp, linea_error):
        self.relational_exp = relational_exp
        self.rel = rel
        self.additive_exp = additive_exp
        self.tipo = TIPOS['bool']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        relational_exp = self.relational_exp
        additive_exp = self.additive_exp
        if relational_exp.tipo != additive_exp.tipo:
            raise TypeError('Se espera que los operandos sean del mismo tipo en una operación relacional (línea %s)' %
                            self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.relational_exp.evaluate(tabulado) + ESPACIO + self.rel + ESPACIO + self.additive_exp.evaluate(
            tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class EqualityExpEqRelationalExp(object):
    def __init__(self, equality_exp, eq, relational_exp, linea_error):
        self.equality_exp = equality_exp
        self.eq = eq
        self.relational_exp = relational_exp
        self.tipo = TIPOS['bool']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        equality_exp = self.equality_exp
        relational_exp = self.relational_exp
        if equality_exp.tipo != relational_exp.tipo:
            raise TypeError('Se espera que los operandos sean del mismo tipo en una operación de igualdad (línea %s)'
                            % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.equality_exp.evaluate(tabulado) + ESPACIO + self.eq + ESPACIO + self.relational_exp.evaluate(
            tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class LogicalAndExpAndEqualityExp(object):
    def __init__(self, logical_and_exp, op, equality_exp, linea_error):
        self.logical_or_exp = logical_and_exp
        self.op = op
        self.equality_exp = equality_exp
        self.tipo = TIPOS['bool']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        logical_and_exp = self.logical_or_exp
        equality_exp = self.equality_exp
        if logical_and_exp.tipo != TIPOS['bool']:
            raise TypeError('Se espera un operando de tipo booleano como primer operando en una operación lógica '
                            '(línea %s)' % self.linea_error)
        if equality_exp.tipo != TIPOS['bool']:
            raise TypeError('Se espera un operando de tipo booleano como segundo operando en una operación lógica '
                            '(línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.logical_or_exp.evaluate(tabulado) + ESPACIO + self.op + ESPACIO + self.equality_exp.evaluate(
            tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class LogicalOrExpOrLogicalAndExp(object):
    def __init__(self, logical_or_exp, op, logical_and_exp, linea_error):
        self.logical_or_exp = logical_or_exp
        self.op = op
        self.logical_and_exp = logical_and_exp
        self.tipo = TIPOS['bool']
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        logical_or_exp = self.logical_or_exp
        logical_and_exp = self.logical_and_exp
        if logical_or_exp.tipo != TIPOS['bool']:
            raise TypeError('Se espera un operando de tipo booleano como primer operando en una operación lógica '
                            '(línea %s)' % self.linea_error)
        if logical_and_exp.tipo != TIPOS['bool']:
            raise TypeError('Se espera un operando de tipo booleano como segundo operando en una operación lógica '
                            '(línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        evaluation = self.logical_or_exp.evaluate(
            tabulado) + ESPACIO + self.op + ESPACIO + self.logical_and_exp.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class LogicalOrExpSignoExpDosPuntosConditionalExp(object):
    def __init__(self, logical_or_exp, signo_preg, exp, dos_puntos, conditional_exp, linea_error_condicion,
                 linea_error_resultado):
        self.logical_or_exp = logical_or_exp
        self.signo_preg = signo_preg
        self.exp = exp
        self.dos_puntos = dos_puntos
        self.conditional_exp = conditional_exp
        self.tipo = None
        self.linea_error_condicion = linea_error_condicion
        self.linea_error_resultado = linea_error_resultado

    def _assert_tipos_de_operandos(self):
        logical_or_exp = self.logical_or_exp
        exp = self.exp
        conditional_exp = self.conditional_exp
        if logical_or_exp.tipo != TIPOS['bool']:
            raise TypeError('Se espera un operando de tipo booleano como condición de la operación ternaria (línea %s)'
                            % self.linea_error_condicion)
        if exp.tipo != conditional_exp.tipo:
            raise TypeError('Se espera que ambos resultados alternativos sean del mismo tipo en la operación ternaria '
                            '(línea %s)' % self.linea_error_resultado)

    def evaluate(self, tabulado=0):
        evaluation = self.logical_or_exp.evaluate(tabulado) + ESPACIO + self.signo_preg + ESPACIO + self.exp.evaluate(
            tabulado) + ESPACIO + self.dos_puntos + ESPACIO + self.conditional_exp.evaluate(tabulado)
        self.tipo = self.exp.tipo
        self._assert_tipos_de_operandos()
        return evaluation


class UnaryExpOpAssigmentExp(object):
    def __init__(self, unary_exp, op, assigment_exp, linea_error):
        self.unary_exp = unary_exp
        self.op = op
        self.assigment_exp = assigment_exp
        self.tipo = None
        self.linea_error = linea_error
        self._assert_la_unary_expression_debe_ser_una_variable()

    def _assert_la_unary_expression_debe_ser_una_variable(self):
        if not isinstance(self.unary_exp, (NombreVariable, PostFixExpPuntoNombreVar, PostFixExpCorcheteExpCorchete)):
            raise TypeError('Solo se puede definir una variable (línea %s)' % self.linea_error)

    def evaluate(self, tabulado=0):
        if isinstance(self.assigment_exp, RegistroExpEncerrada):
            eval_unary_exp = self.unary_exp.evaluate(tabulado)
            evaluation = eval_unary_exp + ESPACIO + self.op.evaluate(
                tabulado) + ESPACIO + self.assigment_exp.evaluate(tabulado, eval_unary_exp)
        else:
            evaluation = self.unary_exp.evaluate(tabulado) + ESPACIO + self.op.evaluate(tabulado) + ESPACIO + \
                         self.assigment_exp.evaluate(tabulado)
        DiccionarioDeTipos.get_instance().definir_variable(self.unary_exp.evaluate(), self.assigment_exp.tipo)
        self.tipo = self.assigment_exp.tipo
        return evaluation


class IfParenExpParenBlock(object):
    def __init__(self, iff, open, exp, close, block, linea_error):
        self.iff = iff
        self.open = open
        self.exp = exp
        self.close = close
        self.block = block
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del IF sea de tipo booleana (línea %s)" % self.linea_error)

    def evaluate(self, tabulado=0):
        espacio_condicional = ESPACIO if not self.block.is_single_statement() else ''
        evaluation = self.iff + ESPACIO + self.open + self.exp.evaluate(
            tabulado) + self.close + espacio_condicional + self.block.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class IfParenExpParenBlockElseBlock(object):
    def __init__(self, iff, open, exp, close, block, eelse, block1, linea_error):
        self.iff = iff
        self.open = open
        self.exp = exp
        self.close = close
        self.block = block
        self.eelse = eelse
        self.block1 = block1
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del IF sea de tipo booleana (línea %s)" % self.linea_error)

    def evaluate(self, tabulado=0):
        block_is_single_statement = self.block.is_single_statement()
        espacio_condicional_1 = ESPACIO if not block_is_single_statement else ''
        salto_de_linea_condicional = SALTO_DE_LINEA if block_is_single_statement else ''
        tabulado_condicional = TABULADO * tabulado if block_is_single_statement else ''
        espacio_condicional_2 = ESPACIO if not self.block1.is_single_statement() else ''
        evaluation = self.iff + ESPACIO + self.open + self.exp.evaluate(
            tabulado) + self.close + espacio_condicional_1 + self.block.evaluate(tabulado) + salto_de_linea_condicional\
                     + espacio_condicional_1 + tabulado_condicional + self.eelse + espacio_condicional_2 +\
                     self.block1.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class WhileParenExpParenBlock(object):
    def __init__(self, whhile, open, exp, close, block, linea_error):
        self.whhile = whhile
        self.open = open
        self.exp = exp
        self.close = close
        self.block = block
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del WHILE sea de tipo booleana (línea %s)" % self.linea_error)

    def evaluate(self, tabulado=0):
        espacio_condicional = ESPACIO if not self.block.is_single_statement() else ''
        evaluation = self.whhile + ESPACIO + self.open + self.exp.evaluate(
            tabulado) + self.close + espacio_condicional + self.block.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class DoBlockWhileParenExpParenPuntoYComa(object):
    def __init__(self, doo, block, whhile, open, exp, close, punto_y_coma, linea_error):
        self.doo = doo
        self.block = block
        self.whhile = whhile
        self.open = open
        self.exp = exp
        self.close = close
        self.punto_y_coma = punto_y_coma
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del DO-WHILE sea de tipo booleana (línea %s)"
                            % self.linea_error)

    def evaluate(self, tabulado=0):
        espacio_condicional = ESPACIO if not self.block.is_single_statement() else ''
        salto_de_linea_condicional = SALTO_DE_LINEA if self.block.is_single_statement() else ''
        tabulado_condicional = TABULADO * tabulado if self.block.is_single_statement() else ''
        evaluation = self.doo + espacio_condicional
        evaluation += self.block.evaluate(tabulado) + salto_de_linea_condicional + espacio_condicional + \
                  tabulado_condicional
        evaluation += self.whhile + ESPACIO + self.open + self.exp.evaluate(tabulado) + self.close + self.punto_y_coma
        self._assert_tipos_de_operandos()
        return evaluation


class ForParenExpStatementExpStatementParenBlock(object):
    def __init__(self, ffor, open, exp_statement, exp_statement1, close, block, linea_error):
        self.ffor = ffor
        self.open = open
        self.exp_statement = exp_statement
        self.exp_statement1 = exp_statement1
        self.close = close
        self.block = block
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp_statement1.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del FOR sea de tipo booleana (línea %s)" % self.linea_error)

    def evaluate(self, tabulado=0):
        espacio_condicional = ESPACIO if not self.block.is_single_statement() else ''
        evaluation = self.ffor + ESPACIO + self.open + self.exp_statement.evaluate(
            tabulado) + ESPACIO + self.exp_statement1.evaluate(
            tabulado) + ESPACIO + self.close + espacio_condicional + self.block.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class ForParenExpStatementExpStatementExpParenBlock(object):
    def __init__(self, ffor, open, exp_statement, exp_statement1, exp, close, block, linea_error):
        self.ffor = ffor
        self.open = open
        self.exp_statement = exp_statement
        self.exp_statement1 = exp_statement1
        self.exp = exp
        self.close = close
        self.block = block
        self.linea_error = linea_error

    def _assert_tipos_de_operandos(self):
        if self.exp_statement1.tipo != TIPOS['bool']:
            raise TypeError("Se espera que la condición del FOR sea de tipo booleana (línea %s)" % self.linea_error)

    def evaluate(self, tabulado=0):
        espacio_condicional = ESPACIO if not self.block.is_single_statement() else ''
        evaluation = self.ffor + ESPACIO + self.open + self.exp_statement.evaluate(
            tabulado) + ESPACIO + self.exp_statement1.evaluate(tabulado) + ESPACIO + self.exp.evaluate(
            tabulado) + self.close + espacio_condicional + self.block.evaluate(tabulado)
        self._assert_tipos_de_operandos()
        return evaluation


class ReturnPuntoYComa(object):
    def __init__(self, ret, punto_y_coma):
        self.ret = ret
        self.punto_y_coma = punto_y_coma

    def evaluate(self, tabulado=0):
        return self.ret + self.punto_y_coma


class ReturnExpPuntoYComa(object):
    def __init__(self, ret, exp, punto_y_coma):
        self.ret = ret
        self.exp = exp
        self.punto_y_coma = punto_y_coma

    def evaluate(self, tabulado=0):
        return self.ret + ESPACIO + self.exp.evaluate(tabulado) + self.punto_y_coma
