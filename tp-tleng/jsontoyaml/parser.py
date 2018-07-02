#! coding: utf-8
"""Parser JSON to YAML."""
import ply.yacc as yacc
from lexer import tokens
from types import *
from expressions import *

def p_expression_value_string(subexpr):
  'value : string'
  subexpr[0] = ValueExpression(subexpr[1])
  
def p_expression_value_false(subexpr):
  'value : FALSE'
  subexpr[0] = ValueExpression(subexpr[1])

def p_expression_value_true(subexpr):
  'value : TRUE'
  subexpr[0] = ValueExpression(subexpr[1])

def p_expression_value_null(subexpr):
  'value : NULL'
  subexpr[0] = ValueExpression(subexpr[1])
  
def p_expression_value_number(subexpr):
  'value : number'
  subexpr[0] = ValueExpression(subexpr[1])

def p_expression_value_object(subexpr):
  'value : object'
  subexpr[0] = ValueExpression(subexpr[1])

def p_expression_value_array(subexpr):
  'value : array'
  subexpr[0] = ValueExpression(subexpr[1])
  
def p_expression_elements_value(subexpr):
  'elements : value'

def p_expression_elements_list(subexpr):
  'elements : value VALUE_SEPARATOR elements'

def p_expression_object(subexpr):
  'object : BEGIN_OBJECT members END_OBJECT'
  
  subexpr[2] = ObjectExpression(subexpr[0])

  
def p_expression_object_empty(subexpr):
  'object : BEGIN_OBJECT END_OBJECT'

def p_expression_members(subexpr):
  'members : pair'
  
def p_expression_members_list(subexpr):
  'members : pair VALUE_SEPARATOR members'
  
def p_expression_pair(subexpr):
  'pair : string NAME_SEPARATOR value'
  
def p_expression_array_empty(subexpr):
  'array : BEGIN_ARRAY END_ARRAY'
  
def p_expression_array_list(subexpr):
  'array : BEGIN_ARRAY elements END_ARRAY'

def p_expression_number(subexpr):
  'number : DIGITS'
  
def p_expression_string(subexpr):
  'string : QUOTATION_MARK STRING QUOTATION_MARK'
  
  

# 
# def p_error(p):
#     message = "Hubo un error durante el parseo.\n"
#     if p is not None:
#         message += "Expresión '{0}' incorrecta en la posición {1}.".format(p.value, str(p.lexpos))
#     else:
#         message += "La expresión no puede ser parseada por la producción {0} de {1}:{2}.".format(parser.symstack, __file__.split("/")[-1], parser.state)
# 
#     raise Exception(message)


# Build the parser
parser = yacc.yacc(debug=True)

def apply_parser(str):
    return parser.parse(str)
    
print apply_parser('[{ "hola" : "chau" }]]')