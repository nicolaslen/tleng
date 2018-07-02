#! coding: utf-8
from types import *

class Expression(object):

	def value(self, context):
		"""
		Parameters:
		-----------
		context: dict<VarExpression, Expression>
			Diccionario con el contexto de la expresión. La clave debe ser la expresión correspondiente a la variable 
			y su valor debe ser la expresión por la cual debe ser sustituída.
		-----------

		Returns:
		--------
		Expression
			Expresión obtenida al haber realizado la evalución

		"""
		raise NotImplementedError("Este método lo deben implementar las clases que hereden de Expression")

	def type(self, context):
		"""
		El método type debe realizar el chequeo de tipos de la expresión y retornar el tipo que se obtiene al realizar dicho chequeo.

		Parameters:
		-----------
		context: dict<VarExpression, Type>
			Diccionario con el contexto de la expresión. La clave debe ser la expresión correspondiente a la variable 
			y su valor debe ser el tipo que debe tomar la misma.
		-----------

		Returns:
		--------
		Type
			Tipo obtenido al haber realizado el chequeo de tipos

		"""
		raise NotImplementedError("Este método lo deben implementar las clases que hereden de Expression")

class ValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression
    
class ObjectExpression(Expression):
  def __init__(self, expression):
    self.expression = expression
    
  
    