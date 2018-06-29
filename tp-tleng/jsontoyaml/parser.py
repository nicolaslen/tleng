#! coding: utf-8
"""Parser lambda calculo."""
import ply.yacc as yacc
from .lexer import tokens
from types import *
from expressions import *


# def p_expression(subexpression):
#     'expression : absExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_abstraction_expression(subexpression):
#     'absExpression : BACKSLASH varExpression COLON typeExpression DOT expression'
#     subexpression[0] = AbstractionExpression(subexpression[2], subexpression[4], subexpression[6])
# 
# def p_abstraction_if_expression(subexpression):
#     'absExpression : ifExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_if_expression(subexpression):
#     'ifExpression : IF expression THEN expression ELSE expression'
#     subexpression[0] = IfExpression(subexpression[2], subexpression[4], subexpression[6])
# 
# def p_if_application_expression(subexpression):
#     'ifExpression : appExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_application_expression(subexpression):
#     'appExpression : appExpression termExpression'
#     subexpression[0] = ApplicationExpression(subexpression[1], subexpression[2])
# 
# def p_application_term_expression(subexpression):
#     'appExpression : termExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_term_var_expression(subexpression):
#     'termExpression : varExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_term_function_expression(subexpression):
#     'termExpression : functionExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_var_expression(subexpression):
#     'varExpression : VAR'
#     subexpression[0] = VarExpression(subexpression[1])
# 
# def p_function_succ_expression(subexpression):
#     'functionExpression : SUCC L_PAREN expression R_PAREN'
#     subexpression[0] = SuccExpression(subexpression[3])
# 
# def p_function_pred_expression(subexpression):
#     'functionExpression : PRED L_PAREN expression R_PAREN'
#     subexpression[0] = PredExpression(subexpression[3])
# 
# def p_function_is_zero_expression(subexpression):
#     'functionExpression : IS_ZERO L_PAREN expression R_PAREN'
#     subexpression[0] = IsZeroExpression(subexpression[3])
# 
# def p_function_val_expression(subexpression):
#     'functionExpression : valExpression'
#     subexpression[0] = subexpression[1]
# 
# def p_val_true_expression(subexpression):
#     'valExpression : TRUE'
#     subexpression[0] = TRUE
# 
# def p_val_false_expression(subexpression):
#     'valExpression : FALSE'
#     subexpression[0] = FALSE
# 
# def p_val_zero_expression(subexpression):
#     'valExpression : ZERO'
#     subexpression[0] = ZERO
# 
# def p_val_expression_expression(subexpression):
#     'valExpression : L_PAREN expression R_PAREN'
#     subexpression[0] = subexpression[2]
# 
# def p_type_function_expression(subexpression):
#     'typeExpression : TYPE ARROW typeExpression'
#     subexpression[0] = FunctionType(Type(subexpression[1]), subexpression[3])
# 
# def p_type_basic_expression(subexpression):
#     'typeExpression : TYPE'
#     subexpression[0] = Type(subexpression[1])
# 
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