#! coding: utf-8
from types import *

class Expression(object):

  def value(self, prefixs):
    raise NotImplementedError("Este método lo deben implementar las clases que hereden de Expression")

class ValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return self.expression.value(prefixs)

class ValuePopExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    exp = "{0}{1}".format("\n", self.expression.value(prefixs))
    prefixs.pop()
    return exp
    
class ObjectExpression(Expression):
  def __init__(self, members):
    self.members = members

  def value(self, prefixs):
    prefixs.append("")
    return self.members.value(prefixs)

class ObjectEmptyExpression(Expression):
  def value(self, prefixs):
    prefixs.append("")
    return "{}"

class ArrayEmptyExpression(Expression):
  def value(self, prefixs):
    prefixs.append("- ")
    return "[]"

class ArrayExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    prefixs.append("- ")
    return self.expression.value(prefixs)
  
class ElementListExpression(Expression):
  def __init__(self, valueExpression, elementsExpression):
    self.valueExpression = valueExpression
    self.elementsExpression = elementsExpression

  def value(self, prefixs):
    spaces = ""
    prefix = ""
    
    if prefixs:
      spaces = ("  " * (len(prefixs) - 1))
      prefix = prefixs[len(prefixs) - 1]

    return "{0}{1}{2}{3}{4}".format(spaces, prefix, self.valueExpression.value(prefixs), "\n", self.elementsExpression.value(prefixs))

class ElementValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    spaces = ""
    prefix = ""
    
    if prefixs:
      spaces = ("  " * (len(prefixs) - 1))
      prefix = prefixs[len(prefixs) - 1]

    return "{0}{1}{2}".format(spaces, prefix, self.expression.value(prefixs))

class PairExpression(Expression):
  def __init__(self, stringExpression, valueExpression):
    self.stringExpression = stringExpression
    self.valueExpression = valueExpression

  def value(self, prefixs):
    return "{0}{1}{2}".format(self.stringExpression.value(prefixs), ": ", self.valueExpression.value(prefixs))

class StringExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return self.expression

class NumberExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return str(self.expression)

class TrueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return "true"

class FalseExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return "false"

class NullExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return ""