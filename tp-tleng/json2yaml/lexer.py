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
  'STRING',
  'BACKSLASH',
  'UNICODE_HEX'
]

  # 2 estados del lexer:
  #
  #   default:
  #     Por defecto, lee objetos, arrays, numeros, etc.
  #   string:
  #     Delimitado por comillas dobles.
  
states = (
  ('string', 'exclusive'),
)

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


t_ignore = ' \s\t\n\r'

# No ignorar ningun caracter dentro del estado string
t_string_ignore = ''


# Ingresa el estado string en una comilla de apertura
def t_QUOTATION_MARK(t):
  r'\"'
  t.lexer.push_state('string') 
  return t

def t_string_STRING(t):
  r'[\x20-\x21,\x23-\x5B,\x5D-\xFFFF]+'
  t.value = unicode(t.value, encoding='utf8')
  return t

# Sale del estado string en una comilla de cierre
def t_string_QUOTATION_MARK(t):
  r'\x22'  # '"'
  t.lexer.pop_state()
  return t

def t_string_BACKSLASH(t):
  r'[\",\\,\/,\b,\f,\n,\r,\t]'
  t.value = unicode(t.value, encoding='utf8')
  return t

def t_string_UNICODE_HEX(t):
  r'\u[\x30-\x39,\x41-\x46,\x61-\x66]{4}' # 'uXXXX'
  t.value = unicode(t.value, encoding='utf8')
  return t

def t_error(t):
    raise Exception("Expresión inválida '%s'" % t.value)

def t_string_error(t):
    raise Exception("Expresión inválida '%s'" % t.value)

# Build the lexer
lexer = lex.lex()

def apply_lexer(string):
    """Aplica el lexer al string dado."""
    print string
    lexer.input(string)
    
    return list(lexer)

#print apply_lexer(exp)

