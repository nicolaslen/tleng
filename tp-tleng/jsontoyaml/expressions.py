#! coding: utf-8
from types import *

class Expression(object):

  def value(self, prefixs):
    raise NotImplementedError("Este método lo deben implementar las clases que hereden de Expression")

  def indent(self, prefixs, exp):
    spaces = ""
    prefix = ""
    
    if prefixs:
      spaces = ("  " * (len(prefixs) - 1))
      prefix = prefixs[len(prefixs) - 1]

    return "{0}{1}{2}".format(spaces, prefix, exp)

class ValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return self.expression.value(prefixs)

class ValuePopExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    exp = self.expression.value(prefixs)
    prefixs.pop()
    return exp
    
# O -> { M }
class ObjectExpression(Expression):
  def __init__(self, members):
    self.members = members

  def value(self, prefixs):
    prefixs.append("")
    return "\n{0}".format(self.members.value(prefixs)) 

# O -> { }
class ObjectEmptyExpression(Expression):
  def value(self, prefixs):
    prefixs.append("")
    return "{}"

# A -> [ ]
class ArrayEmptyExpression(Expression):
  def value(self, prefixs):
    prefixs.append("- ")
    return "[]"

# A -> [ E ]
class ArrayExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    prefixs.append("- ")
    return "\n{0}".format(self.expression.value(prefixs))

# E -> V , E
# M -> P , M
class ElementListExpression(Expression):
  def __init__(self, valueExpression, elementsExpression):
    self.valueExpression = valueExpression
    self.elementsExpression = elementsExpression

  def value(self, prefixs):
    exp = "{0}\n{1}".format(self.valueExpression.value(prefixs), self.elementsExpression.value(prefixs))
    return Expression.indent(self, prefixs, exp)

# M -> P
# E -> V
class ElementValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return Expression.indent(self, prefixs, self.expression.value(prefixs))

# M -> S : V
class PairExpression(Expression):
  def __init__(self, stringExpression, valueExpression):
    self.stringExpression = stringExpression
    self.valueExpression = valueExpression

  def value(self, prefixs):
    return "{0}: {1}".format(self.stringExpression.value(prefixs), self.valueExpression.value(prefixs))

# S -> " string "
class StringExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return self.expression

# V -> num
class NumberExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return str(self.expression)

# V -> true
class TrueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return "true"

# V -> false
class FalseExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return "false"

# V -> null
class NullExpression(Expression):
  def __init__(self, expression):
    self.expression = expression

  def value(self, prefixs):
    return ""