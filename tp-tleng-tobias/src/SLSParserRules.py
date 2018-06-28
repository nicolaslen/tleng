from SLSLexerRules import tokens
from expressions import *

start = 'program'

precedence = (
    ('nonassoc', 'RPAREN'),
    ('nonassoc', 'ELSE'),
)


def p_program_1(subexpressions):
    """program : statement_list"""
    subexpressions[0] = Program(subexpressions[1])


def p_statement_list_1(subexpressions):
    """statement_list : COMENTARIO"""
    token_comment = subexpressions.slice[1]
    is_inline = token_comment.is_inline
    subexpressions[0] = Comentario(subexpressions[1], is_inline)


def p_statement_list_2(subexpressions):
    """statement_list : statement_list COMENTARIO"""
    token_comment = subexpressions.slice[2]
    is_inline = token_comment.is_inline
    subexpressions[0] = StatementListComentario(subexpressions[1], Comentario(subexpressions[2], is_inline))


def p_statement_list_3(subexpressions):
    """statement_list : statement"""
    subexpressions[0] = Statement(subexpressions[1])


def p_statement_list_4(subexpressions):
    """statement_list : statement_list statement"""
    subexpressions[0] = BinaryNonTerminalStatement(subexpressions[1], Statement(subexpressions[2]))


def p_statement_2(subexpressions):
    """statement : expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement"""
    subexpressions[0] = subexpressions[1]


def p_single_statement(subexpressions):
    """single_statement : comment_list statement"""
    subexpressions[0] = BinaryNonTerminalStatement(subexpressions[1], Statement(subexpressions[2]))


def p_single_statement_2(subexpressions):
    """single_statement : statement"""
    subexpressions[0] = Statement(subexpressions[1])


def p_comment_list_1(subexpressions):
    """comment_list : COMENTARIO comment_list"""
    token_comment = subexpressions.slice[1]
    is_inline = token_comment.is_inline
    subexpressions[0] = ComentarioCommentList(Comentario(subexpressions[1], is_inline), subexpressions[2])


def p_comment_list_2(subexpressions):
    """comment_list : COMENTARIO"""
    token_comment = subexpressions.slice[1]
    is_inline = token_comment.is_inline
    subexpressions[0] = Comentario(subexpressions[1], is_inline)


def p_block_1(subexpressions):
    """block : single_statement"""
    subexpressions[0] = SingleStatement(subexpressions[1])


def p_block_2(subexpressions):
    """block : bracketed_statement_list"""
    subexpressions[0] = BracketedStatementList(subexpressions[1])


def p_bracketed_statement_list_2(subexpressions):
    """bracketed_statement_list : LLLAVE statement_list RLLAVE"""
    subexpressions[0] = LlaveStatementListLlave(subexpressions[1], subexpressions[2], subexpressions[3])


def p_expression_statement_1(subexpressions):
    """expression_statement : PUNTO_Y_COMA"""
    subexpressions[0] = Token(subexpressions[1])


def p_expression_statement_2(subexpressions):
    """expression_statement : expression PUNTO_Y_COMA"""
    subexpressions[0] = ExpressionPuntoYComa(subexpressions[1], subexpressions[2])


def p_expression_1(subexpressions):
    """expression : assignment_expression"""
    subexpressions[0] = ExpressionAssignmentExp(subexpressions[1])


def p_expression_2(subexpressions):
    """expression : expression COMA assignment_expression"""
    subexpressions[0] = ExpressionComaAssignmentExp(subexpressions[1], subexpressions[2], subexpressions[3])


def p_primary_expression_1(subexpressions):
    """primary_expression : NOMBRE_VARIABLE"""
    subexpressions[0] = NombreVariable(subexpressions[1])


def p_primary_expression_2(subexpressions):
    """primary_expression : NUMERO"""
    subexpressions[0] = Numerico(subexpressions[1])


def p_primary_expression_3(subexpressions):
    """primary_expression : CADENA"""
    subexpressions[0] = Cadena(subexpressions[1])


def p_primary_expression_4(subexpressions):
    """primary_expression : TRUE
                          | FALSE"""
    subexpressions[0] = TrueFalse(subexpressions[1])


def p_primary_expression_6(subexpressions):
    """primary_expression : LPAREN expression RPAREN"""
    subexpressions[0] = FuncExpEncerrada(subexpressions[1], subexpressions[2], subexpressions[3])


def p_primary_expression_7(subexpressions):
    """primary_expression : LCORCHETE vector_expression RCORCHETE"""
    subexpressions[0] = VectorExpEncerrada(subexpressions[1], subexpressions[2], subexpressions[3])


def p_primary_expression_8(subexpressions):
    """primary_expression : LLLAVE reg_expression RLLAVE"""
    subexpressions[0] = RegistroExpEncerrada(subexpressions[1], subexpressions[2], subexpressions[3])


def p_primary_expression_9(subexpressions):
    """primary_expression : function"""
    subexpressions[0] = subexpressions[1]


def p_vector_expression_1(subexpressions):
    """vector_expression : conditional_expression"""
    subexpressions[0] = VectorConditionalExp(subexpressions[1])


def p_vector_expression_2(subexpressions):
    """vector_expression : conditional_expression COMA vector_expression"""
    subexpressions[0] = VectorConditionalExpComaVectorExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                          subexpressions.lineno(2))


def p_reg_expression_1(subexpressions):
    """reg_expression : NOMBRE_VARIABLE DOS_PUNTOS expression"""
    subexpressions[0] = NombreVarDosPuntosExp(NombreVariable(subexpressions[1]), subexpressions[2], subexpressions[3])


def p_reg_expression_2(subexpressions):
    """reg_expression : NOMBRE_VARIABLE DOS_PUNTOS expression COMA reg_expression"""
    subexpressions[0] = NombreVarDosPuntosExpComaRegExp(NombreVariable(subexpressions[1]), subexpressions[2],
                                                        subexpressions[3], subexpressions[4], subexpressions[5])


def p_function_1(subexpressions):
    """function : MULTIPLICACION_ESCALAR"""
    subexpressions[0] = FuncionMultiplicacionEscalar(subexpressions[1])


def p_function_2(subexpressions):
    """function : CAPITALIZAR"""
    subexpressions[0] = FuncionCapitalizar(subexpressions[1])


def p_function_3(subexpressions):
    """function : COLINEALES"""
    subexpressions[0] = FuncionColineales(subexpressions[1])


def p_function_4(subexpressions):
    """function : PRINT"""
    subexpressions[0] = FuncionPrint(subexpressions[1])


def p_function_5(subexpressions):
    """function : LENGTH"""
    subexpressions[0] = FuncionLength(subexpressions[1])


def p_postfix_expression_1(subexpressions):
    """postfix_expression : primary_expression"""
    subexpressions[0] = subexpressions[1]


def p_postfix_expression_2(subexpressions):
    """postfix_expression : postfix_expression LCORCHETE expression RCORCHETE"""
    subexpressions[0] = PostFixExpCorcheteExpCorchete(subexpressions[1], subexpressions[2], subexpressions[3],
                                                      subexpressions[4], subexpressions.lineno(2))


def p_postfix_expression_3(subexpressions):
    """postfix_expression : function LPAREN RPAREN"""
    subexpressions[0] = FunctionExpParenParen(subexpressions[1], subexpressions[2], subexpressions[3],
                                              subexpressions.lineno(2))


def p_postfix_expression_4(subexpressions):
    """postfix_expression : function LPAREN argument_expression_list RPAREN"""
    subexpressions[0] = FunctionExpParenArgumentExpListParen(subexpressions[1], subexpressions[2],
                                                             ArgumentExpLs(subexpressions[3]), subexpressions[4],
                                                             subexpressions.lineno(2))


def p_postfix_expression_5(subexpressions):
    """postfix_expression : postfix_expression PUNTO NOMBRE_VARIABLE"""
    subexpressions[0] = PostFixExpPuntoNombreVar(subexpressions[1], subexpressions[2], subexpressions[3],
                                                 subexpressions.lineno(2))


def p_postfix_expression_6(subexpressions):
    """postfix_expression : postfix_expression AUTOINCREMENTO
                          | postfix_expression AUTODECREMENTO"""
    subexpressions[0] = PostFixExpAuto(subexpressions[1], subexpressions[2], subexpressions.lineno(2))


def p_argument_expression_list_1(subexpressions):
    """argument_expression_list : assignment_expression"""
    subexpressions[0] = ArgumentExpLsAssigmentExp(subexpressions[1])


def p_argument_expression_list_2(subexpressions):
    """argument_expression_list : argument_expression_list COMA assignment_expression"""
    subexpressions[0] = ArgumentExpLsComaAssigmentExp(subexpressions[1], subexpressions[2], subexpressions[3])


def p_unary_expression_1(subexpressions):
    """unary_expression : postfix_expression"""
    subexpressions[0] = subexpressions[1]


def p_unary_expression_2(subexpressions):
    """unary_expression : AUTOINCREMENTO unary_expression
                        | AUTODECREMENTO unary_expression"""
    subexpressions[0] = AutoUnaryExp(subexpressions[1], subexpressions[2])


def p_unary_expression_4(subexpressions):
    """unary_expression : unary_operator unary_expression"""
    subexpressions[0] = BinaryNonTerminalUnaryOperatorExpression(subexpressions[1], subexpressions[2])


def p_unary_operator_1(subexpressions):
    """unary_operator : MAS
                      | MENOS"""
    subexpressions[0] = Token(subexpressions[1])


def p_unary_operator_2(subexpressions):
    """unary_operator : NOT"""
    subexpressions[0] = TokenNot(subexpressions[1])


def p_multiplicative_expression_1(subexpressions):
    """multiplicative_expression : unary_expression"""
    subexpressions[0] = subexpressions[1]


def p_multiplicative_expression_2(subexpressions):
    """multiplicative_expression : multiplicative_expression POR unary_expression
                                 | multiplicative_expression DIVIDIDO unary_expression
                                 | multiplicative_expression EXPONENTE unary_expression"""
    subexpressions[0] = MultiplicativeExpOpUnaryExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                    subexpressions.lineno(2))


def p_congruence_expression_1(subexpressions):
    """congruence_expression : multiplicative_expression """
    subexpressions[0] = subexpressions[1]


def p_congruence_expression_2(subexpressions):
    """congruence_expression : congruence_expression MODULO multiplicative_expression"""
    subexpressions[0] = CongruenceExpModuloMultiplicativeExpression(subexpressions[1], subexpressions[2],
                                                                    subexpressions[3], subexpressions.lineno(2))


def p_additive_expression_1(subexpressions):
    """additive_expression : congruence_expression"""
    subexpressions[0] = subexpressions[1]


def p_additive_expression_2(subexpressions):
    """additive_expression : additive_expression MAS congruence_expression
                           | additive_expression MENOS congruence_expression"""
    subexpressions[0] = AdditiveExpOpCongruenceExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                   subexpressions.lineno(2))


def p_relational_expression_1(subexpressions):
    """relational_expression : additive_expression"""
    subexpressions[0] = subexpressions[1]


def p_relational_expression_2(subexpressions):
    """relational_expression : relational_expression MENOR additive_expression
                             | relational_expression MAYOR additive_expression"""
    subexpressions[0] = RelationalExpRelAdditiveExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                    subexpressions.lineno(2))


def p_equality_expression_1(subexpressions):
    """equality_expression : relational_expression"""
    subexpressions[0] = subexpressions[1]


def p_equality_expression_2(subexpressions):
    """equality_expression : equality_expression IGUALDAD relational_expression
                           | equality_expression DESIGUALDAD relational_expression"""
    subexpressions[0] = EqualityExpEqRelationalExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                   subexpressions.lineno(2))


def p_logical_and_expression_1(subexpressions):
    """logical_and_expression : equality_expression"""
    subexpressions[0] = subexpressions[1]


def p_logical_and_expression_2(subexpressions):
    """logical_and_expression : logical_and_expression AND equality_expression"""
    subexpressions[0] = LogicalAndExpAndEqualityExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                    subexpressions.lineno(2))


def p_logical_or_expression_1(subexpressions):
    """logical_or_expression : logical_and_expression"""
    subexpressions[0] = subexpressions[1]


def p_logical_or_expression_2(subexpressions):
    """logical_or_expression : logical_or_expression OR logical_and_expression"""
    subexpressions[0] = LogicalOrExpOrLogicalAndExp(subexpressions[1], subexpressions[2], subexpressions[3],
                                                    subexpressions.lineno(2))


def p_conditional_expression_1(subexpressions):
    """conditional_expression : logical_or_expression"""
    subexpressions[0] = subexpressions[1]


def p_conditional_expression_2(subexpressions):
    """conditional_expression : logical_or_expression SIGNO_DE_PREGUNTA expression DOS_PUNTOS conditional_expression"""
    subexpressions[0] = LogicalOrExpSignoExpDosPuntosConditionalExp(subexpressions[1], subexpressions[2],
                                                                    subexpressions[3], subexpressions[4],
                                                                    subexpressions[5], subexpressions.lineno(2),
                                                                    subexpressions.lineno(4))


def p_assignment_expression_1(subexpressions):
    """assignment_expression : conditional_expression"""
    subexpressions[0] = subexpressions[1]


def p_assignment_expression_2(subexpressions):
    """assignment_expression : unary_expression IGUAL assignment_expression
                             | unary_expression POR_IGUAL assignment_expression
                             | unary_expression DIVIDO_IGUAL assignment_expression
                             | unary_expression MAS_IGUAL assignment_expression
                             | unary_expression MENOS_IGUAL assignment_expression"""
    subexpressions[0] = UnaryExpOpAssigmentExp(subexpressions[1], Token(subexpressions[2]), subexpressions[3],
                                               subexpressions.lineno(2))


def p_selection_statement_1(subexpressions):
    """selection_statement : IF LPAREN expression RPAREN block"""
    subexpressions[0] = IfParenExpParenBlock(subexpressions[1], subexpressions[2], subexpressions[3], subexpressions[4],
                                             Block(subexpressions[5]), subexpressions.lineno(2))


def p_selection_statement_2(subexpressions):
    """selection_statement : IF LPAREN expression RPAREN block ELSE block"""
    subexpressions[0] = IfParenExpParenBlockElseBlock(subexpressions[1], subexpressions[2], subexpressions[3],
                                                      subexpressions[4], Block(subexpressions[5]), subexpressions[6],
                                                      Block(subexpressions[7]), subexpressions.lineno(2))


def p_iteration_statement_1(subexpressions):
    """iteration_statement : WHILE LPAREN expression RPAREN block"""
    subexpressions[0] = WhileParenExpParenBlock(subexpressions[1], subexpressions[2], subexpressions[3],
                                                subexpressions[4], Block(subexpressions[5]), subexpressions.lineno(2))


def p_iteration_statement_2(subexpressions):
    """iteration_statement : DO block WHILE LPAREN expression RPAREN PUNTO_Y_COMA"""
    subexpressions[0] = DoBlockWhileParenExpParenPuntoYComa(subexpressions[1], Block(subexpressions[2]),
                                                            subexpressions[3], subexpressions[4], subexpressions[5],
                                                            subexpressions[6], subexpressions[7],
                                                            subexpressions.lineno(4))


def p_iteration_statement_3(subexpressions):
    """iteration_statement : FOR LPAREN expression_statement expression_statement RPAREN block"""
    subexpressions[0] = ForParenExpStatementExpStatementParenBlock(subexpressions[1], subexpressions[2],
                                                                   subexpressions[3], subexpressions[4],
                                                                   subexpressions[5], Block(subexpressions[6]),
                                                                   subexpressions.lineno(2))


def p_iteration_statement_4(subexpressions):
    """iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN block"""
    subexpressions[0] = ForParenExpStatementExpStatementExpParenBlock(subexpressions[1], subexpressions[2],
                                                                      subexpressions[3], subexpressions[4],
                                                                      subexpressions[5], subexpressions[6],
                                                                      Block(subexpressions[7]),
                                                                      subexpressions.lineno(2))


def p_jump_statement_1(subexpressions):
    """jump_statement : RETURN PUNTO_Y_COMA"""
    subexpressions[0] = ReturnPuntoYComa(subexpressions[1], subexpressions[2])


def p_jump_statement_2(subexpressions):
    """jump_statement : RETURN expression PUNTO_Y_COMA"""
    subexpressions[0] = ReturnExpPuntoYComa(subexpressions[1], subexpressions[2], subexpressions[3])


def p_error(subexpressions):
    if subexpressions:
        raise SyntaxError("Error: no se esperaba el token '%s' (línea %s)" %
                          (subexpressions.value, subexpressions.lineno))
    else:
        raise SyntaxError("Final del input inesperado")
