sentencias = [
    'PUNTO_Y_COMA'
]

comentarios = [
    'COMENTARIO'
]

bloques = [
    'LLLAVE',
    'RLLAVE'
]

operadores = [
    # asignacion
    'IGUAL',
    'MAS_IGUAL',
    'MENOS_IGUAL',
    'POR_IGUAL',
    'DIVIDO_IGUAL',

    # matemáticos
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'EXPONENTE',
    'MODULO',
    'AUTOINCREMENTO',
    'AUTODECREMENTO',

    # relacionales
    'IGUALDAD',
    'DESIGUALDAD',
    'MAYOR',
    'MENOR',

    # ternario
    'SIGNO_DE_PREGUNTA',
    'DOS_PUNTOS'
]

variables_y_valores = [
    'NUMERO',
    'NOMBRE_VARIABLE',
    'CADENA',
    'LPAREN',
    'RPAREN',
    'LCORCHETE',
    'RCORCHETE',
    'PUNTO',
    'COMA'
]

funciones = {
    'multiplicacionEscalar': 'MULTIPLICACION_ESCALAR',
    'capitalizar': 'CAPITALIZAR',
    'colineales': 'COLINEALES',
    'print': 'PRINT',
    'length': 'LENGTH',
}

reservado = {
    'begin': 'BEGIN',
    'end': 'END',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'do': 'DO',
    'res': 'RES',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'AND': 'AND',
    'OR': 'OR',
    'NOT': 'NOT',
}

all_palabras_reservadas = {}
all_palabras_reservadas.update(reservado)
# asumimos funciones palabras reservadas, porque podria haber conflictos con print = algo por ejemplo.
all_palabras_reservadas.update(funciones)

tokens = sentencias + comentarios + bloques + operadores + variables_y_valores + list(all_palabras_reservadas.values())


def t_newline(token):
    r"""\n+"""
    token.lexer.lineno += len(token.value)


# sentencias
def t_PUNTO_Y_COMA(token):
    r""";"""
    token.lexer.lastline = token.lexer.lineno
    return token


# comentarios
def t_COMENTARIO(token):
    r"""\#.*"""
    if hasattr(token.lexer, 'lastline'):
        token.is_inline = token.lexer.lastline == token.lexer.lineno
    else:
        token.is_inline = 1 == token.lexer.lineno
    return token


# bloques
t_LLLAVE = r"\{"
t_RLLAVE = r"\}"

# funciones
t_MULTIPLICACION_ESCALAR = r"multiplicacionEscalar"
t_CAPITALIZAR = r"capitalizar"
t_COLINEALES = r"colineales"
t_PRINT = r"print"
t_LENGTH = r"length"

# operadores
# --- asignación
t_IGUAL = r"="
t_MAS_IGUAL = r"\+="
t_MENOS_IGUAL = r"-\="
t_POR_IGUAL = r"\*="
t_DIVIDO_IGUAL = r"\/="

# --- matemáticos
t_MAS = r"\+"
t_MENOS = r"-"
t_POR = r"\*"
t_DIVIDIDO = r"\/"
t_EXPONENTE = r"\^"
t_MODULO = r"%"
t_AUTOINCREMENTO = r"\+\+"
t_AUTODECREMENTO = r"--"

# --- relacionales
t_IGUALDAD = r"=="
t_DESIGUALDAD = r"!="
t_MAYOR = r">"
t_MENOR = r"<"

# --- ternario
t_SIGNO_DE_PREGUNTA = r"\?"
t_DOS_PUNTOS = r":"


# variables y valores

def t_NUMERO(token):
    r"""(([0-9]+\.[0-9]+)|([0-9]+\.)|(\.[0-9]+)|([1-9][0-9]+|[0-9]))"""
    # TODO - no hace falta ni castear aca me parece, total no hacemos nada con el valor concretamente
    # (salvo si checkeamos por int para algunas operaciones)
    if "." in token.value:
        token.value = float(token.value)
    else:
        token.value = int(token.value)
    return token


def t_NOMBRE_VARIABLE(token):
    r"""([a-z]|[A-Z])(([a-z]|[A-Z])|\_|[0-9])*"""
    value = token.value
    tipo_token_upper = reservado.get(value.upper(), 'NOMBRE_VARIABLE')
    tipo_token_lower = reservado.get(value.lower(), tipo_token_upper)
    tipo_token_funcion = funciones.get(value, tipo_token_lower)
    token.type = tipo_token_funcion  # Check for reserved words
    return token


def t_CADENA(token):
    r"""(")(?:(?=(\\?))(\\?).)*?(")"""
    return token

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LCORCHETE = r"\["
t_RCORCHETE = r"\]"
t_PUNTO = r"\."
t_COMA = r","

# palabras reservadas (?i) para case insensitive flag

t_AND = r"(?i)AND"
t_OR = r"(?i)OR"
t_NOT = r"(?i)NOT"
t_IF = r"(?i)if"
t_ELSE = r"(?i)else"
t_BEGIN = r"(?i)begin"   # Unused, no entendemos como se usa
t_END = r"(?i)end"   # Unused, no entendemos como se usa
t_RES = r"(?i)res"   # Unused, no entendemos como se usa
t_RETURN = r"(?i)return"
t_TRUE = r"(?i)true"
t_FALSE = r"(?i)false"
t_FOR = r"(?i)for"
t_WHILE = r"(?i)while"
t_DO = r"(?i)do"

t_ignore = " \t\r"


def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
