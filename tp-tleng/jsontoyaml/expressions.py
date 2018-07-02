#! coding: utf-8
from types import *

class ValueExpression(Expression):
  def __init__(self, expression):
    self.expression = expression
    
class ObjectExpression(Expression):
  def __init__(self, expression):
    self.expression = expression
    
  
    