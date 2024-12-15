# import re
# import ply.yacc as yacc
# import ply.lex as lex

# from process import process

# a_tokens = [
#     "FLOAT",
#     "NUMBER",
#     "PLUS",
#     "MINUS",
#     "TIMES",
#     "DIVIDE",
#     "LPAREN",
#     "RPAREN",
#     "LSQPAREN",
#     "RSQPAREN",
#     "VERTICALBAR",
#     "COMMA",
#     "EQ",
#     "EQEQ",
#     "MORE",
#     "LESS",
#     "ID",
#     "STRING",
#     "METHOD",
# ]

# reserved = {
#     "func": "FUNC",
#     "global": "GLOBAL",
#     "do": "DO",
#     "if": "IF",
#     "then": "THEN",
#     "else": "ELSE",
#     "while": "WHILE",
#     "return": "RETURN",
#     "matrix": "MATRIX",
#     "vector": "VECTOR",
#     "call": "CALL",
#     "until": "UNTIL",
#     "for": "FOR",
#     "read": "READ",
#     "write": "WRITE",
#     "const": "CONST",
#     "in": "IN",
#     "INDENT": "INDENT",
#     "DEDENT": "DEDENT",
# }


# tokens = a_tokens + list(reserved.values())

# # Regular expression rules for simple tokens
# t_PLUS = r"\+"
# t_MINUS = r"-"
# t_TIMES = r"\*"
# t_DIVIDE = r"/"
# t_LPAREN = r"\("
# t_RPAREN = r"\)"
# t_LSQPAREN = r"\["
# t_RSQPAREN = r"\]"
# t_VERTICALBAR = r"\|"
# t_COMMA = r","
# t_EQ = r"="
# t_EQEQ = r"=="
# t_MORE = r">"
# t_LESS = r"<"

# table = {}


# def t_ID(t):
#     r"[a-zA-Z_][a-zA-Z_0-9]*"
#     t.type = reserved.get(t.value, "ID")
#     return t


# def t_METHOD(t):
#     r"\.[a-zA-Z_][a-zA-Z_0-9]*"
#     return t


# def t_STRING(t):
#     r"\"(.)*\" "
#     t.value = t.value[1:-1]
#     return t


# def t_COMMENT(t):
#     r"\#(.)*"
#     pass


# def t_FLOAT(t):
#     r"\d+\.\d+"
#     t.value = float(t.value)
#     return t


# def t_NUMBER(t):
#     r"\d+"
#     t.value = int(t.value)
#     return t


# def t_newline(t):
#     r"\n+"


# t_ignore = " \t"


# # Error handling rule
# def t_error(t):
#     print(f"Illegal character '{t.value[0]}'")
#     t.lexer.skip(1)


# #
# # PARESER
# #


# def p_program(p):
#     """program : prog_element_list"""
#     p[0] = p[1]


# def p_prog_element_list(p):
#     """prog_element_list : prog_element_list prog_element
#     | prog_element"""
#     if len(p) == 3:
#         p[0] = p[1] + [p[2]]
#     else:
#         p[0] = [p[1]]


# def p_prog_element(p):
#     """prog_element : function
#     | global_var"""
#     p[0] = p[1]


# def p_function(p):
#     """function : FUNC ID LPAREN argument_list RPAREN DO block
#     | FUNC ID LPAREN RPAREN DO block"""
#     if len(p) == 8:
#         p[0] = ("func", p[2], "(", p[4], ")", "do", p[7])
#     else:
#         p[0] = ("func", p[2], "(", ")", "do", p[6])


# def p_global_var(p):
#     """global_var : ID EQ list
#     | ID EQ multi_dim_list"""
#     p[0] = (p[2], "=", p[3])


# def p_list(p):
#     """list : LSQPAREN enum RSQPAREN
#     | LSQPAREN RSQPAREN"""
#     p[0] = ("[", p[2], ")")


# def p_multi_dim_list(p):
#     """multi_dim_list : LSQPAREN row_list RSQPAREN"""
#     p[0] = ("[", p[2], "]")


# def p_row_list(p):
#     """row_list : row_list COMMA row
#     | row"""
#     if len(p) == 4:
#         p[0] = p[1] + [p[3]]
#     else:
#         p[0] = [p[1]]


# def p_row(p):
#     """row : LSQPAREN enum RSQPAREN"""
#     p[0] = ("[", p[2], "]")


# def p_enum(p):
#     """enum : enum COMMA value
#     | value"""
#     if len(p) == 4:
#         p[0] = p[1] + [p[3]]
#     if len(p) == 2:
#         p[0] = [p[1]]


# def p_value(p):
#     """value : ID
#     | STRING
#     | NUMBER
#     | FLOAT"""
#     p[0] = p[1]


# def p_block(p):
#     """block : INDENT statement_list DEDENT"""
#     p[0] = p[2]


# def p_statement_list(p):
#     """statement_list : statement_list statement
#     | statement"""
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = p[1] + [p[2]]


# def p_statement(p):
#     """statement : if_statement
#     | while_statement
#     | for_statement
#     | until_statement
#     | call_statement
#     | return_statement
#     | assignment_statement
#     | write
#     | read
#     | ID method
#     | GLOBAL ID
#     | const_declaration"""
#     if len(p) == 3:
#         p[0] = (p[1], p[2])
#     else:
#         p[0] = p[1]


# def p_const_declaration(p):
#     """const_declaration : CONST ID"""
#     p[0] = ("const", p[2])


# def p_if_statement(p):
#     """if_statement : IF LPAREN condition RPAREN THEN block
#     | IF LPAREN condition RPAREN THEN block ELSE block"""
#     if len(p) == 6:
#         p[0] = ("if", "(", p[3], ")", "then", p[6])
#     else:
#         p[0] = ("if", "(", p[3], ")", "then", p[6], "else", p[8])


# def p_while_statement(p):
#     """while_statement : WHILE LPAREN condition RPAREN DO block"""
#     p[0] = ("while", "(", p[3], ")", "do", p[6])


# def p_for_statement(p):
#     """for_statement : FOR LPAREN term IN term RPAREN DO block"""
#     # print(f"block p[6] {p[4]}")
#     p[0] = ("for", "(", p[3], "in", p[5], ")", "do", p[8])


# def p_until_statement(p):
#     """until_statement : UNTIL LPAREN condition RPAREN DO block"""
#     # print(f"until {p}")
#     p[0] = ("until", "(", p[3], ")", "do", p[6])


# def p_call_statement(p):
#     """call_statement : CALL ID LPAREN argument_list RPAREN"""
#     p[0] = ("call", p[2], "(", p[4], ")")


# def p_return_statement(p):
#     """return_statement : RETURN return_list"""
#     p[0] = ("return", p[2])


# def p_assignment_statement(p):
#     """assignment_statement : ID EQ ID
#     | ID EQ typed_argument
#     | ID EQ ID method
#     | ID EQ list
#     | ID EQ multi_dim_list
#     | ID EQ term
#     | ID EQ casting_statement"""

#     if str(p[3]).find("matrix") or str(p[3]).count("[") > 1:

#         table[p[1]] = "matrix"
#     else:
#         table[p[1]] = "vector"

#     if len(p[3]) == 1:
#         try:
#             table[p[3]]
#         except:
#             raise Exception(f"non-existent var {p[3]}  {p[1], p[2], p[3]}")

#     if len(p) == 4:
#         p[0] = (p[1], "=", p[3])
#     if len(p) == 5:
#         p[0] = (p[1], "=", p[2], p[3])


# def p_casting_statement(p):
#     """casting_statement : LPAREN type_specifier RPAREN ID"""
#     p[0] = ("cast", p[2], p[4])


# def p_condition(p):
#     """condition : logical_expression
#     | term"""
#     p[0] = p[1]


# def p_logical_expression(p):
#     """logical_expression : logical_expression MORE logical_expression
#     | logical_expression LESS logical_expression
#     | logical_expression EQEQ logical_expression
#     | ID
#     | sqpar_val
#     | LPAREN expression RPAREN"""
#     if len(p) == 4:
#         if p[2] == ">":
#             p[0] = (">", p[1], p[3])
#         elif p[2] == "<":
#             p[0] = ("<", p[1], p[3])
#         elif p[2] == "==":
#             p[0] = ("==", p[1], p[3])
#     elif len(p) == 2:
#         p[0] = p[1]  # ID or NUMBER
#     else:
#         p[0] = p[2]


# def p_return_list(p):
#     """return_list : return_list COMMA expression
#     | expression"""
#     if len(p) == 3:
#         p[0] = p[1] + [p[3]]

#     else:
#         p[0] = [p[1]]


# def p_argument_list(p):
#     """argument_list : argument_list COMMA typed_argument
#     |  typed_argument"""
#     # print(f"argumets {p[1]}")
#     if len(p) == 4:
#         p[0] = p[1] + [p[3]]
#     else:
#         p[0] = [p[1]]


# def p_typed_argument(p):
#     """typed_argument : type_specifier ID"""
#     if p[1] == "matrix":
#         table[p[2]] = "matrix"
#     else:
#         table[p[2]] = "vector"

#     p[0] = (p[1], p[2])


# def p_type_specifier(p):
#     """type_specifier : MATRIX
#     | VECTOR
#     | NUMBER
#     | FLOAT
#     | STRING"""
#     p[0] = p[1]


# def p_expression(p):
#     """expression : expression PLUS term
#     | expression MINUS term
#     | STRING
#     | term"""
#     if len(p) == 4:  # У нас сложение или вычитание
#         p[0] = (p[2], p[1] + p[3])  # Сложение
#     else:  # У нас просто термин
#         p[0] = p[1]


# def p_term(p):
#     """term : term TIMES factor
#     | term DIVIDE factor
#     | term PLUS factor
#     | term MINUS factor
#     | factor"""
#     if len(p) == 4:  # У нас умножение или деление
#         if p[2] == "*":
#             p[0] = (p[1], "*", p[3])  # Умножение
#         elif p[2] == "/":
#             p[0] = (p[1], "/", p[3])  # Деление
#         elif p[2] == "+":
#             p[0] = (p[1], "-", p[3])
#         elif p[2] == "-":
#             p[0] = (p[1], "+", p[3])
#     else:  # У нас просто фактор
#         p[0] = p[1]


# def p_factor(p):
#     """factor : LPAREN expression RPAREN
#     | sqpar_val
#     | verticalbar
#     | ID"""
#     if len(p) == 4:  # Если у нас выражение в скобках
#         p[0] = p[2]  # Вернем результат выражения
#     if len(p) == 3:
#         p[0] = ("const", p[2])
#     if len(p) == 2:
#         p[0] = p[1]


# def p_sqpar_val(p):
#     """sqpar_val : LSQPAREN NUMBER RSQPAREN
#     | LSQPAREN FLOAT RSQPAREN
#     | LSQPAREN STRING RSQPAREN"""
#     if type(p[2]) == float:
#         p[0] = ("[", p[2], "]")
#     if type(p[2]) == int:
#         p[0] = ("[", p[2], "]")
#     if type(p[2]) == str:
#         p[0] = ("[", p[2], "]")


# def p_write(p):
#     """write : WRITE LPAREN return_list RPAREN"""
#     p[0] = ("write", "(", p[3], ")")


# def p_read(p):
#     """read : READ LPAREN RPAREN"""
#     p[0] = ("read", "(", ")")


# def p_verticalbar(p):
#     """verticalbar : VERTICALBAR ID VERTICALBAR"""
#     p[0] = ("|", p[1], "|")


# def p_method(p):
#     """method : METHOD LPAREN argument_list RPAREN
#     | ID METHOD LPAREN RPAREN"""
#     # print(f"method list {p[3]}")
#     if len(p) == 5:
#         p[0] = (p[1], "(", p[3], ")")
#     else:
#         p[0] = (p[2], "(", ")")


# # Error rule for syntax errors
# def p_error(p):
#     print(f"Syntax error in input! at symbol {p.value}")


# # Build the parser
# parser = yacc.yacc(debug=True)
# lexer = lex.lex()

file = "code_test.txt"
# data = process("data_1.txt")

# lexer.input(data)
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)


# result = parser.parse(data)
# print(result)
