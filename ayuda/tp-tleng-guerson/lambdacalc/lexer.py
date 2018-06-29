#! coding: utf-8
import ply.lex as lex


""" Lista de tokens """
tokens = [
    
    'BACKSLASH',
    'VAR',
    'COLON',
    'TYPE',
    'DOT',

    'ZERO',

    'R_PAREN',
    'L_PAREN',
    'ARROW'
]


# https://stackoverflow.com/questions/5022129/ply-lex-parsing-problem 
reserved_tokens = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'succ' : 'SUCC',
    'pred' : 'PRED',
    'isZero' : 'IS_ZERO',
    'true' : 'TRUE',
    'false' : 'FALSE'
}

tokens += reserved_tokens.values()


t_BACKSLASH = r'\\'

def t_VAR(t):
    r'[a-z][a-zA-Z0-9]*'
    if t.value in reserved_tokens:
        t.type = reserved_tokens[t.value]
    return t

t_COLON = r':'
t_TYPE = r'(Bool|Nat)'
t_DOT = r'\.'

t_ZERO = r'0'

t_L_PAREN =r'\('
t_R_PAREN =r'\)'
t_ARROW = r'->'


t_ignore = ' \t'


def t_error(t):
    raise Exception("Expresión invalida '%s'" % t.value)


# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)
