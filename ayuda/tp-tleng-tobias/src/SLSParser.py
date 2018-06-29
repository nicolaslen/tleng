import sys
from optparse import OptionParser
from sys import exit

from ply.lex import lex
from ply.yacc import yacc, NullLogger

import SLSLexerRules
import SLSParserRules


if __name__ == "__main__":
    option_parser = OptionParser()
    option_parser.add_option("-o", "--output", dest="output_filename", help="archivo de output", metavar="FILE")
    option_parser.add_option("-c", "--input", dest="input_filename", help="archivo de entrada", metavar="FILE")

    (options, args) = option_parser.parse_args()

    text = ""
    if options.input_filename:
        input_file = open(options.input_filename, "r")
        text = input_file.read()
        input_file.close()
    else:
        if len(args) > 0:
            text = args[0]
        else:
            print("Parámetros inválidos.")
            print("Uso:")
            print("  SLSParser.py [-o SALIDA] [-c ENTRADA | FUENTE]")
            exit()

    lexer = lex(module=SLSLexerRules)

    # NullLogger para que no muestre warnings y "manche" el stderr. Se puede sacar para ver que no hay conflictos
    parser = yacc(module=SLSParserRules, errorlog=NullLogger())

    ast = parser.parse(text, lexer)

    result = ast.evaluate()

    if options.output_filename:
        output_file = open(options.output_filename, "w")
        output_file.write(result)
        output_file.close()
        print('Se ha guardado satisfactoriamente el resultado del parseo en el archivo %s.' % options.output_filename)
    else:
        sys.stdout.write(result)
