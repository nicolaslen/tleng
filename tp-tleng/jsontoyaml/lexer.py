#! coding: utf-8
import ply.lex as lex


""" Lista de tokens """
tokens = [
  # Initial state tokens
  'BEGIN_ARRAY',
  'BEGIN_OBJECT',
  'END_ARRAY',
  'END_OBJECT',
  'NAME_SEPARATOR',
  'VALUE_SEPARATOR',
  'QUOTATION_MARK',
  'FALSE',
  'TRUE',
  'NULL',
  'DECIMAL_POINT',
  'DIGITS',
  'E',
  'MINUS',
  'PLUS',
  'ZERO',
  # String state tokens
  'UNESCAPED',
  'ESCAPE',
  # Escaped state tokens
  'REVERSE_SOLIDUS',
  'SOLIDUS',
  'BACKSPACE_CHAR',
  'FORM_FEED_CHAR',
  'LINE_FEED_CHAR',
  'CARRIAGE_RETURN_CHAR',
  'TAB_CHAR',
  'UNICODE_HEX'
]


# https://stackoverflow.com/questions/5022129/ply-lex-parsing-problem 
# reserved_tokens = {
#     'if' : 'IF',
#     'then' : 'THEN',
#     'else' : 'ELSE',
#     'succ' : 'SUCC',
#     'pred' : 'PRED',
#     'isZero' : 'IS_ZERO',
#     'true' : 'TRUE',
#     'false' : 'FALSE'
# }

# tokens += reserved_tokens.values()




# Default state tokens
t_BEGIN_ARRAY          = r'\['
t_BEGIN_OBJECT         = r'\{'
t_END_ARRAY            = r'\]'
t_END_OBJECT           = r'\}'
t_NAME_SEPARATOR       = r'\:'
t_VALUE_SEPARATOR      = r'\,'
t_FALSE                = r'false'
t_TRUE                 = r'true'
t_NULL                 = r'null'
t_DECIMAL_POINT        = r'\.'
t_DIGITS               = r'[0-9]+'
t_E                    = r'[eE]'
t_MINUS                = r'\-'
t_PLUS                 = r'\+'
t_ZERO                 = r'\0'


#t_ignore = '\s\t\n\r'

# Enters the string state on an opening quotation mark 
def t_QUOTATION_MARK(t):
  r'\"'
  t.lexer.push_state('string') 
  return t
	
# Exits the string state on an unescaped closing quotation mark
def t_string_QUOTATION_MARK(t):
  r'\"'
  t.lexer.pop_state()
  return t


def t_error(t):
    raise Exception("Expresión invalida '%s'" % t.value)


# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    lexer.input(string)

    return list(lexer)