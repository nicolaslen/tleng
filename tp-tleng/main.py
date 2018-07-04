"""Archivo principal de json2yaml."""
from json2yaml import parse
import sys
from string import join
    
def execute(expression):
	try:
		parsed = parse(expression)
		print "YAML> {0}\n".format(parsed.value([]))
	except Exception as e:
		sys.stderr.write(str(e) + "\n")
		exit(1)


def main():
	if len(sys.argv) < 2:
		while True:
			expression = raw_input('JSON> ')
			if expression == "exit":
				break
			else:
				execute(expression)
	else:
		execute(join(sys.argv[1:]))
		


if  __name__ =='__main__':
	main()