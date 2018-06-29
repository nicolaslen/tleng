from optparse import OptionParser

import sys

import SLSLexerRules

from sys import argv

from ply.lex import lex


def dump_tokens(lexer, output_file):
    token = lexer.token()

    while token is not None:
        output_file.write("type:" + token.type)
        output_file.write(" value:" + str(token.value))
        output_file.write(" line:" + str(token.lineno))
        output_file.write(" position:" + str(token.lexpos))
        output_file.write("\n")

        token = lexer.token()


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
            print("  SLSLexer.py [-o SALIDA] [-c ENTRADA | FUENTE]")
            exit()

    lexer = lex(module=SLSLexerRules)

    lexer.input(text)

    if options.output_filename:
        output_file = open(options.output_filename, "w")
        dump_tokens(lexer, output_file)
        output_file.close()
    else:
        dump_tokens(lexer, sys.stdout)
