gramatica_file = open('gramatica')
parser_rules_file = open('parser_rules_file.py', 'w')

contador = 1
for line in gramatica_file:
    if line[0] != '\t':
        no_terminal = line.strip()
        contador = 1
    else:
        if line[1] != ";":
            derecha_produccion = line[2:].strip()
            parser_rules_file.write(
'''
def p_%(no_terminal)s_%(contador)d(subexpressions):
    """%(no_terminal)s : %(derecha_produccion)s"""
    pass

''' % {'no_terminal': no_terminal, 'derecha_produccion': derecha_produccion, 'contador': contador})
            contador += 1

gramatica_file.close()
parser_rules_file.close()
