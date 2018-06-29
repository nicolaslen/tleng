"""Archivo principal de lambdacalc."""
from lambdacalc import parse
import sys
from string import join
    
def execute(expression):
	try:
		parsed = parse(expression)
		expressionType = str(parsed.type({}))
		print(str(parsed.value({})) + ":" + expressionType)
	except Exception as e:
		sys.stderr.write(str(e) + "\n")
		exit(1)


def main():
	if len(sys.argv) < 2:
		while True:
			expression = raw_input('expression> ')
			if expression == "exit":
				break
			else:
				execute(expression)
	else:
		execute(join(sys.argv[1:]))
		


if  __name__ =='__main__':
	main()