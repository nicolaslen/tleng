import unittest
from context import *

class BasicTests(unittest.TestCase):

	def testTrue(self):
		self.assertEqual(parse("true").value({}), TRUE)

	def testFalse(self):
		self.assertEqual(parse("false").value({}), FALSE)

	def testZero(self):
		self.assertEqual(parse("0").value({}), ZERO)

	def testSuccZero(self):
		self.assertEqual(parse("succ(0)").value({}), SuccExpression(ZERO))

	def testPredZero(self):
		self.assertEqual(parse("pred(0)").value({}), ZERO)

	def testPredSuccZero(self):
		self.assertEqual(parse("pred(succ(0))").value({}), ZERO)

	def testPredSuccSuccZero(self):
		self.assertEqual(parse("pred(succ(succ(0)))").value({}), SuccExpression(ZERO))

	def testSuccPredSuccZero(self):
		self.assertEqual(parse("succ(pred(succ(0)))").value({}), SuccExpression(ZERO))

	def testIsZeroZero(self):
		self.assertEqual(parse("isZero(0)").value({}), TRUE)

	def testIsZeroPredZero(self):
		self.assertEqual(parse("isZero(pred(0))").value({}), TRUE)

	def testIsZeroSuccZero(self):
		self.assertEqual(parse("isZero(succ(0))").value({}), FALSE)

	def testIfTrue(self):
		self.assertEqual(parse("if true then 0 else succ(0)").value({}), ZERO)

	def testIfFalse(self):
		self.assertEqual(parse("if false then 0 else succ(0)").value({}), SuccExpression(ZERO))

	def testLambda(self):
		self.assertEqual(parse("\\x:Nat.x").value({}), AbstractionExpression(VarExpression("x"),NAT_TYPE,VarExpression("x")))

	def testApplicationSimple(self):
		self.assertEqual(parse("(\\x:Nat.x) 0").value({}), ZERO)

	def testApplicationFunction(self):
		self.assertEqual(parse("(\\x:Nat.succ(x)) 0").value({}), SuccExpression(ZERO))

	def testApplicationLambda(self):
		self.assertEqual(parse("(\\f:Nat->Bool.f 0) (\\x:Nat.isZero(x))").value({}), TRUE)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
