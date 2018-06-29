class Type(object):
	def __init__(self, typeName):
		self.typeName = typeName

	def __repr__(self):
		return "Type(typeName: {0})".format(self.typeName)

	def __str__(self):
		return self.typeName

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.typeName == other.typeName

	def __ne__(self, other):
		return not (self == other)

	def isFunction(self):
		return False;

BOOL_TYPE = Type("Bool")
NAT_TYPE = Type("Nat")


class FunctionType(Type):
	def __init__(self, domainType, rangeType):
		Type.__init__(self, "Function")
		self.domainType = domainType
		self.rangeType = rangeType

	def __repr__(self):
		return "FunctionType(domainType: {0} | rangeType: {1})".format(self.domainType, self.rangeType)

	def __str__(self):
		domainStr = "(" + str(self.domainType) + ")" if(self.domainType.isFunction()) else self.domainType
		return "{0}->{1}".format(domainStr, self.rangeType)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.domainType == other.domainType and self.rangeType == other.rangeType

	def isFunction(self):
		return True;

	def domain(self):
		return self.domainType

	def range(self):
		return self.rangeType