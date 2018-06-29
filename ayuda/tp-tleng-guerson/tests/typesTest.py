#! coding: utf-8
import unittest
from context import *

class BasicTests(unittest.TestCase):

	def testTrueBool(self):
		self.assertEqual(parse("true").type({}), BOOL_TYPE)

	def testFalseBool(self):
		self.assertEqual(parse("false").type({}), BOOL_TYPE)

	def testZeroNat(self):
		self.assertEqual(parse("0").type({}), NAT_TYPE)

	def testSuccZeroNat(self):
		self.assertEqual(parse("succ(0)").type({}), NAT_TYPE)

	def testPredZeroNat(self):
		self.assertEqual(parse("pred(0)").type({}), NAT_TYPE)

	def testPredSuccZeroNat(self):
		self.assertEqual(parse("pred(succ(0))").type({}), NAT_TYPE)

	def testPredSuccSuccZeroNat(self):
		self.assertEqual(parse("pred(succ(succ(0)))").type({}), NAT_TYPE)

	def testSuccPredSuccZeroNat(self):
		self.assertEqual(parse("succ(pred(succ(0)))").type({}), NAT_TYPE)

	def testIsZeroZeroBool(self):
		self.assertEqual(parse("isZero(0)").type({}), BOOL_TYPE)

	def testIsZeroPredZeroBool(self):
		self.assertEqual(parse("isZero(pred(0))").type({}), BOOL_TYPE)

	def testIsZeroSuccZeroBool(self):
		self.assertEqual(parse("isZero(succ(0))").type({}), BOOL_TYPE)

	def testSuccSubExpressionNotNat(self):
		with self.assertRaisesRegexp(Exception, 'La subexpresión no es de tipo Nat'):
			parse("succ(true)").type({})

	def testPredSubExpressionNotNat(self):
		with self.assertRaisesRegexp(Exception, 'La subexpresión no es de tipo Nat'):
			parse("pred(true)").type({})

	def testIsZeroSubExpressionNotNat(self):
		with self.assertRaisesRegexp(Exception, 'La subexpresión no es de tipo Nat'):
			parse("isZero(false)").type({})

	def testIfConditionNotBool(self):
		with self.assertRaisesRegexp(Exception, 'La condición debe ser de tipo Bool'):
			parse("if 0 then 0 else succ(0)").type({})

	def testIfDifferentExpressionsType(self):
		with self.assertRaisesRegexp(Exception, 'Las expresiones resultantes del if deben tener el mismo tipo'):
			parse("if true then false else succ(0)").type({})

	def testIfTrueType(self):
		self.assertEqual(parse("if true then 0 else succ(0)").type({}), NAT_TYPE)

	def testIfFalseType(self):
		self.assertEqual(parse("if false then true else false").type({}), BOOL_TYPE)

	def testLambdaType1(self):
		self.assertEqual(parse("\\x:Nat.succ(x)").type({}), FunctionType(NAT_TYPE, NAT_TYPE))

	def testLambdaType2(self):
		self.assertEqual(parse("\\x:Bool.x").type({}), FunctionType(BOOL_TYPE, BOOL_TYPE))

	def testLambdaType3(self):
		self.assertEqual(parse("\\x:Nat.isZero(x)").type({}), FunctionType(NAT_TYPE, BOOL_TYPE))

	def testLambdaType4(self):
		self.assertEqual(parse("\\x:Nat->Bool.x").type({}), FunctionType(FunctionType(NAT_TYPE, BOOL_TYPE),FunctionType(NAT_TYPE, BOOL_TYPE)))

	def testApplicationSimpleType(self):
		self.assertEqual(parse("(\\x:Nat.x) 0").type({}), NAT_TYPE)

	def testApplicationFunctionType(self):
		self.assertEqual(parse("(\\x:Nat.succ(x)) 0").type({}), NAT_TYPE)

	def testApplicationLambdaType(self):
		self.assertEqual(parse("(\\f:Nat->Bool.f 0) (\\x:Nat.isZero(x))").type({}), BOOL_TYPE)

	def testApplicationLambdaParameterTypeDifferentFromVariableType(self):
		with self.assertRaisesRegexp(Exception, 'El parámetro pasado no se corresponde con el dominio de la abstracción'):
			self.assertEqual(parse("(\\x:Nat.x) true").type({}), NAT_TYPE)

	def testApplicationWithoutLambdaType(self):
		with self.assertRaisesRegexp(Exception, 'La expresión de la izquierda no es una abstracción'):
			self.assertEqual(parse("(true) true").type({}), NAT_TYPE)

	def testVariableFree(self):
		with self.assertRaisesRegexp(Exception, 'La variable x esta libre'):
			self.assertEqual(parse("x").type({}), NAT_TYPE)

	def testVariableNotFree(self):
			self.assertEqual(parse("x").type({VarExpression("x"): NAT_TYPE}), NAT_TYPE)

	
def main():
    unittest.main()

if __name__ == '__main__':
    main()
