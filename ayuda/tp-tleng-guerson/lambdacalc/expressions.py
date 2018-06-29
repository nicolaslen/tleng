#! coding: utf-8
from types import *

class Expression(object):
	"""
	La clase Expression tiene como objetivo representar una abstracción de las expresiones del calculo lambda.
	Cualquier expresión válida de este lenguaje deberá extender esta clase y sobreescribir los métodos de la misma.
	"""

	def value(self, context):
		"""
		El método value debe evaluar la expresión y retornar el valor que se obtiene al realizar dicha evaluación.

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


class BoolExpression(Expression):
	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return "BoolExpression({0})".format(self.expression)

	def __str__(self):
		return self.expression

	def type(self, context):
		return BOOL_TYPE

	def value(self, context):
		return self

TRUE = BoolExpression("true")
FALSE = BoolExpression("false")


class ZeroExpression(Expression):
		def __repr__(self):
			return "ZeroExpression"
		
		def __str__(self):
			return "0"

		def type(self, context):
			return NAT_TYPE

		def value(self, context):
			return self

ZERO = ZeroExpression()


class ApplicationExpression(Expression):
	def __init__(self, firstExpression, secondExpression):
		self.firstExpression = firstExpression
		self.secondExpression = secondExpression
		
	def __repr__(self):
		return "ApplicationExpression(Expression1: {0} | Expression2: {1})".format(self.firstExpression, self.secondExpression)

	def __str__(self):
		return "{0} {1}".format(self.firstExpression, self.secondExpression)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.firstExpression == other.firstExpression and self.secondExpression == other.secondExpression

	def value(self, context):
		# Se evalúa la expresión de la derecha hasta obtener un valor
		parameterValue = self.secondExpression.value(context)
		# Se evalúa la expresión de la izquierda hasta obtener un valor (es necesario porque antes de evaluar no necesariamente es una abstracción), 
		# el cual se asume que una vez evaluado es una abstracción.
		# Luego se le indica a la abstracción que se aplique, es decir, que realice el reemplazo de variables por sus valores y
		# retorne el valor final
		return self.firstExpression.value(context).apply(parameterValue, context)

	def type(self, context):
		abstractionType = self.firstExpression.type(context)
		if not abstractionType.isFunction():
			raise Exception("La expresión de la izquierda no es una abstracción")
		else:
			parameterType = self.secondExpression.type(context)
			if not abstractionType.domain() == parameterType:
				raise Exception("El parámetro pasado no se corresponde con el dominio de la abstracción")
			else:
				return abstractionType.range()


class AbstractionExpression(Expression):
	def __init__(self, variable, variableType, expression):
		self.variable = variable
		self.variableType = variableType
		self.expression = expression

	def __repr__(self):
		return "AbstractionExpression(VarName: {0} | VarType: {1} | Expression: {2})".format(self.variable, self.variableType, self.expression)

	def __str__(self):
		return "\{0}:{1}.{2}".format(self.variable, str(self.variableType), self.expression)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.variable == other.variable and self.variableType == other.variableType \
			and self.expression == other.expression

	def value(self, context):
		return self

	def apply(self, parameterValue, context):
		"""
		El método apply debe introducir el el valor de la variable en el contexto y retornar el valor obtenido 
		al evaluar su expresión.

		Parameters:
		-----------
		parameterValue: Expression
			Expresión que será el valor de la variable

		context: dict<VarExpression, Expression>
			Contexto en donde se deberá definir la expresión para la variable de la abstracción
		-----------

		Returns:
		--------
		Expression
			Valor obtenido luego de realizar la evaluación de la expresión reemplazando variables por su valor.
		"""
		context[self.variable] = parameterValue
		return self.expression.value(context)

	def type(self, context):
		context[self.variable] = self.variableType
		return FunctionType(self.variableType, self.expression.type(context))


class IfExpression(Expression):
	def __init__(self, condition, ifTrue, ifFalse):
		self.condition = condition
		self.ifTrue = ifTrue
		self.ifFalse = ifFalse

	def __repr__(self):
		return "IfExpression(condition: {0} | ifTrue: {1} | ifFalse: {2}".format(self.condition, self.ifTrue, self.ifFalse)

	def __str__(self):
		return "if {0} then {1} else {2}".format(self.condition, self.ifTrue, self.ifFalse)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.condition == other.condition and self.ifTrue == other.ifTrue \
			and self.ifFalse == other.ifFalse

	def value(self, context):
		return self.ifTrue.value(context) if(self.condition.value(context) == TRUE) else self.ifFalse.value(context)

	def type(self, context):
		if(self.condition.type(context) != BOOL_TYPE):
			raise Exception("La condición debe ser de tipo Bool")
		elif(self.ifTrue.type(context) != self.ifFalse.type(context)):
			raise Exception("Las expresiones resultantes del if deben tener el mismo tipo")	
		return self.ifTrue.type(context)


class VarExpression(Expression):
	def __init__(self, varName):
		self.varName = varName

	def __repr__(self):
		return "VarExpression({0})".format(self.varName)

	def __str__(self):
		return self.varName

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.varName == other.varName

	def __hash__(self):
		return hash(self.varName)

	def type(self, context):
		if(context.has_key(self)):
			return context[self]
		else:
			raise Exception("La variable {0} esta libre".format(self.varName))

	def value(self, context):
		if(context.has_key(self)):
			return context[self].value(context)
		else:
			raise Exception("La variable {0} esta libre".format(self.varName))


class NatExpression(Expression):
	def __init__(self, expression):
		self.expression = expression

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.expression == other.expression

	def type(self, context):
		if(self.expression.type(context) == NAT_TYPE):
			return NAT_TYPE
		else:
			raise Exception("La subexpresión no es de tipo Nat")


class SuccExpression(NatExpression):
		def __repr__(self):
			return "SuccExpression(Expression: {0})".format(self.expression)
		
		def __str__(self):
			return "succ({0})".format(self.expression)

		def value(self, context):
			return SuccExpression(self.expression.value(context))


class PredExpression(NatExpression):
		def __repr__(self):
			return "PredExpression(Expression: {0})".format(self.expression)
		
		def __str__(self):
			return "pred({0})".format(self.expression)

		def value(self, context):
			if(self.expression == ZERO):
				return ZERO
			else:
				expressionValue = self.expression.value(context)
				return ZERO if(expressionValue == ZERO) else expressionValue.expression.value(context)


class IsZeroExpression(Expression):
	def __init__(self, expression):
		self.expression = expression

	def __repr__(self):
		return "IsZeroExpression({0})".format(self.expression)

	def __str__(self):
		return "isZero({0})".format(self.expression)

	def type(self, context):
		if(self.expression.type(context) == NAT_TYPE):
			return BOOL_TYPE
		else:
			raise Exception("La subexpresión no es de tipo Nat")

	def value(self, context):
		return TRUE if(self.expression.value(context) == ZERO) else FALSE

