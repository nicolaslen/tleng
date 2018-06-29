#! coding: utf-8
import unittest
from context import *

class BasicTests(unittest.TestCase):

	def testSuccExpressionValue(self):
		self.assertEqual(parse("succ(if true then succ(0) else 0)").value({}), SuccExpression(SuccExpression(ZERO)))

	def testPredExpressionValue(self):
		self.assertEqual(parse("pred((\\x:Nat.succ(x)) succ(0))").value({}), SuccExpression(ZERO))

	def testIsZeroExpressionValue(self):
		self.assertEqual(parse("isZero(if false then 0 else succ(0))").value({}), FALSE)

	def testIfConditionExpressionValue(self):
		self.assertEqual(parse("if isZero(pred(if true then 0 else succ(0))) then 0 else succ(0)").value({}), ZERO)

	def testIfTrueExpressionValue(self):
		self.assertEqual(parse("if isZero(0) then (\\x:Nat.succ(x)) 0 else succ(succ(0))").value({}), SuccExpression(ZERO))

	def testIfFalseExpressionValue(self):
		self.assertEqual(parse("if isZero((\\b:Bool.b)) then (\\x:Nat.succ(x)) succ(0) else pred((\\x:Nat.succ(x)) succ(0))").value({}), SuccExpression(ZERO))

	def testLambdaRigthAssociation(self):
		self.assertEqual(parse("\\f:Nat->Nat.f 0").value({}), AbstractionExpression(VarExpression("f"),FunctionType(NAT_TYPE,NAT_TYPE),ApplicationExpression(VarExpression("f"),ZERO)))

	def testLambdaPrecedence(self):
		self.assertEqual(parse("\\f:Nat->Nat.f (if true then 0 else succ(0))").value({}), \
			AbstractionExpression(VarExpression("f"),FunctionType(NAT_TYPE,NAT_TYPE), \
				ApplicationExpression(VarExpression("f"), \
					IfExpression(TRUE, ZERO, SuccExpression(ZERO)))))

	def testIfRigthAssociation(self):
		self.assertEqual(parse("if true then 0 else (\\x:Nat.succ(x)) 0").value({}), ZERO)

	def testIfPrecedence(self):
		self.assertEqual(parse("if false then 0 else (\\x:Nat.succ(x)) 0").value({}), SuccExpression(ZERO))

	def testApplicationLeftExpressionLambdaWithoutBrackets(self):
		with self.assertRaisesRegexp(Exception, r".*Expresión '\\' incorrecta en la posición.*"):
			self.assertEqual(parse("(\\f:Nat->Nat.f 0) \\y:Nat.y").value({}), ZERO)

	def testApplicationLeftExpressionLambdaWithBrackets(self):
		self.assertEqual(parse("(\\f:Nat->Nat.f 0) (\\y:Nat.y)").value({}), ZERO)

	def testApplicationLeftExpressionIfWithoutBrackets(self):
		with self.assertRaisesRegexp(Exception, "Expresión 'if' incorrecta en la posición"):
			parse("(\\f:Nat->Nat.f 0) if true then \\y:Nat.y else \\x:Nat.succ(x)").value({})

	def testApplicationLeftExpressionIfWithBrackets(self):
		self.assertEqual(parse("(\\f:Nat->Nat.f 0) (if true then \\y:Nat.y else \\x:Nat.succ(x))").value({}), ZERO)

	def testComplexExpressionWithMultiplePrecedencesAndAssociations(self):
		self.assertEqual(parse("(\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)) (\\j:Nat.succ(j)) succ(succ(0)) true").value({}), \
			SuccExpression(SuccExpression(SuccExpression(ZERO))))

def main():
	unittest.main()

if __name__ == '__main__':
    main()
