#! coding: utf-8
"""Parser JSON to YAML."""
import ply.yacc as yacc
from lexer import tokens
from expressions import *

def p_expression_value_string(subexpr):
  'value : string'
  subexpr[0] = ValueExpression(subexpr[1])
  
def p_expression_value_false(subexpr):
  'value : FALSE'
  subexpr[0] = FalseExpression(subexpr[1])

def p_expression_value_true(subexpr):
  'value : TRUE'
  subexpr[0] = TrueExpression(subexpr[1])

def p_expression_value_null(subexpr):
  'value : NULL'
  subexpr[0] = NullExpression(subexpr[1])
  
def p_expression_value_number(subexpr):
  'value : number'
  subexpr[0] = ValueExpression(subexpr[1])

def p_expression_value_object(subexpr):
  'value : object'
  subexpr[0] = ValuePopExpression(subexpr[1])

def p_expression_value_array(subexpr):
  'value : array'
  subexpr[0] = ValuePopExpression(subexpr[1])
  
def p_expression_elements_value(subexpr):
  'elements : value'
  subexpr[0] = LastElementArrayExpression(subexpr[1])

def p_expression_elements_list(subexpr):
  'elements : value VALUE_SEPARATOR elements'
  subexpr[0] = ElementArrayExpression(subexpr[1], subexpr[3])

def p_expression_object(subexpr):
  'object : BEGIN_OBJECT members END_OBJECT'
  subexpr[0] = ObjectExpression(subexpr[2])

def p_expression_object_empty(subexpr):
  'object : BEGIN_OBJECT END_OBJECT'
  subexpr[0] = ObjectEmptyExpression()

def p_expression_members(subexpr):
  'members : pair'
  subexpr[0] = LastElementObjectExpression(subexpr[1])
  
def p_expression_members_list(subexpr):
  'members : pair VALUE_SEPARATOR members'
  subexpr[0] = ElementObjectExpression(subexpr[1], subexpr[3])
  
def p_expression_pair(subexpr):
  'pair : string NAME_SEPARATOR value'
  subexpr[0] = PairExpression(subexpr[1], subexpr[3])
  
def p_expression_array_empty(subexpr):
  'array : BEGIN_ARRAY END_ARRAY'
  subexpr[0] = ArrayEmptyExpression()
  
def p_expression_array_list(subexpr):
  'array : BEGIN_ARRAY elements END_ARRAY'
  subexpr[0] = ArrayExpression(subexpr[2])

def p_expression_number_plus(subexpr):
  'number : integer
            | float'
  subexpr[0] = subexpr[1]

def p_expression_number_minus(subexpr):
  'number : MINUS integer
            | MINUS float'
  subexpr[0] = - subexpr[2]

def p_expression_integer(subexpr):
  'integer : DIGITS'
  subexpr[0] = - NumberExpression(subexpr[1])

def p_expression_integer_exp(subexpr):
  'integer : DIGITS exp'
  subexpr[0] = NumberExpression(subexpr[1]) * (10 ** subexpr[2])
  
def p_expression_float(subexpr):
  'float : DIGITS frac'
  subexpr[0] = NumberExpression(subexpr[1]) + subexpr[2]

def p_expression_float_exp(subexpr):
  'float : DIGITS frac exp'
  subexpr[0] = (NumberExpression(subexpr[1]) + subexpr[2]) * (10 ** subexpr[3])

def p_expression_exp(subexpr):
  'exp : E DIGITS'
  subexpr[0] = int(subexpr[2])

def p_expression_exp+(subexpr):
  'exp : E PLUS DIGITS'
  subexpr[0] = int(subexpr[3])
  
def p_expression_exp-(subexpr):
  'exp : E MINUS DIGITS'
  subexpr[0] = -int(subexpr[e])
  
def p_expression_frac(subexpr):
  'frac : DECIMAL_POINT DIGITS'
  subexpr[0] = float('.' + subexpr[2])

  
def p_expression_string(subexpr):
  'string : QUOTATION_MARK STRING QUOTATION_MARK'
  subexpr[0] = StringExpression(subexpr[2])  

 
def p_error(p):
  message = "Hubo un error durante el parseo.\n"
  if p is not None:
    message += "Expresión '{0}' incorrecta en la posición {1}.".format(p.value, str(p.lexpos))
  else:
    message += "La expresión no puede ser parseada por la producción {0} de {1}:{2}.".format(parser.symstack, __file__.split("/")[-1], parser.state)

  raise Exception(message)


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
  
#exp = '[1, [2, 3], [1, [2, 3]]]'
#exp = '[1, [3, 4], {"h":"o","l":"a"}]'
#exp = '[ {"clave1": "valor1", "clave 2": [ 125, "Cadena 1" ], "- clave3": true}, "Cadena con salto de linea", [null, 35, {}] ]'
#exp = '{"h":"o", "h":"a"}'

#expression = apply_parser(exp)
#result = expression.value([])
#print result
