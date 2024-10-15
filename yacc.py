import ply.yacc as yacc
from main import data

# Get the token map from the lexer.  This is required.
from lex import My_Lexer

tokens = My_Lexer().tokens

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("right", "EQ"),
)


def p_program(p):
    """program : prog_element_list"""
    p[0] = p[1]


def p_prog_element_list(p):
    """prog_element_list : prog_element_list prog_element
    | prog_element"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_prog_element(p):
    """prog_element : function
    | global_var"""
    p[0] = p[1]

def p_function(p):
    """function : FUNC ID LPAREN argument_list RPAREN DO block"""
    p[0] = ("func", p[2], "(", p[2], ")", "do", p[5])


def p_global_var(p):
    """global_var : ID EQ list
    | ID EQ multi_dim_list"""
    p[0] = (p[2], "=", p[4])


def p_list(p):
    """list : LSQPAREN element_list RSQPAREN"""
    p[0] = p[2]  # возвращаем список элементов


def p_element_list(p):
    """element_list : element_list COMMA expression
    | expression"""
    if len(p) == 2:
        p[0] = [p[1]]  # один элемент в списке
    else:
        p[0] = p[1] + [p[3]]  # несколько элементов


# Для обработки многомерных списков
def p_multi_dim_list(p):
    """multi_dim_list : LSQPAREN list RSQPAREN LSQPAREN list RSQPAREN"""
    p[0] = [p[2], p[5]]


def p_block(p):
    """block : INDENT statement_list DEDENT"""
    p[0] = p[2]


def p_statement_list(p):
    """statement_list : statement_list statement
    | statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : if_statement
    | while_statement
    | for_statement
    | until_statement
    | call_statement
    | return_statement
    | assignment_statement
    | write
    | read
    | ID method
    | GLOBAL ID"""
    if len(p) == 2:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_if_statement(p):
    """if_statement : IF LPAREN condition RPAREN THEN block
    | IF LPAREN condition RPAREN THEN block ELSE block"""
    if len(p) == 6:
        p[0] = ("if", "(", p[3], ")", "then", p[6])
    else:
        p[0] = ("if", "(", p[3], ")", "then", p[6], "else", p[8])


def p_while_statement(p):
    """while_statement : WHILE RPAREN condition LPAREN DO block"""
    p[0] = ("while", "(", p[3], ")", "do", p[6])


def p_for_statement(p):
    """for_statement : FOR LPAREN term IN term RPAREN DO block"""
    p[0] = ("for", "(", p[3], "in", "term", ")", "do", p[6])


def p_until_statement(p):
    """until_statement : UNTIL RPAREN condition LPAREN DO block"""
    p[0] = ("until", "(", p[3], ")", "do", p[6])


def p_call_statement(p):
    """call_statement : CALL ID LPAREN argument_list RPAREN"""
    p[0] = ("call", p[2], "(", p[3], ")")


def p_return_statement(p):
    """return_statement : RETURN return_list"""
    p[0] = ("return", p[2])


def p_assignment_statement(p):
    """assignment_statement : ID EQ ID
    | ID EQ typed_argument
    | ID EQ ID method
    | ID EQ list
    | ID EQ multi_dim_list
    | ID EQ term"""
    if len(p) == 4:
        p[0] = (p[1], "=", p[2])
    if len(p) == 5:
        p[0] = (p[1], "=", p[2], p[3])


def p_condition(p):
    """condition : logical_expression
    | term"""
    p[0] = p[1]


def p_logical_expression(p):
    """logical_expression : logical_expression MORE logical_expression
    | logical_expression LESS logical_expression
    | logical_expression EQEQ logical_expression
    | ID
    | sqpar_val
    | LPAREN expression RPAREN"""
    if len(p) == 4:
        if p[2] == ">":
            p[0] = (">", p[1], p[3])
        elif p[2] == "<":
            p[0] = ("<", p[1], p[3])
        elif p[2] == "==":
            p[0] = ("==", p[1], p[3])
    elif len(p) == 2:
        p[0] = p[1]  # ID or NUMBER
    else:
        p[0] = p[2]


def p_return_list(p):
    """return_list : return_list COMMA expression
    | expression"""
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_argument_list(p):
    """argument_list : argument_list typed_argument COMMA
    | argument_list typed_argument
    |  typed_argument"""
    if len(p) > 1:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]


def p_typed_argument(p):
    """typed_argument : type_specifier ID"""
    p[0] = (p[1], p[2])


def p_type_specifier(p):
    """type_specifier : MATRIX
    | VECTOR
    | NUMBER
    | FLOAT
    | STRING"""
    p[0] = p[1]


def p_expression(p):
    """expression : expression PLUS term
    | expression MINUS term
    | term"""
    if len(p) == 4:  # У нас сложение или вычитание
        if p[2] == "+":
            p[0] = p[1] + p[3]  # Сложение
        elif p[2] == "-":
            p[0] = p[1] - p[3]  # Вычитание
    else:  # У нас просто термин
        p[0] = p[1]


def p_term(p):
    """term : term TIMES factor
    | term DIVIDE factor
    | factor"""
    if len(p) == 4:  # У нас умножение или деление
        if p[2] == "*":
            p[0] = p[1] * p[3]  # Умножение
        elif p[2] == "/":
            p[0] = p[1] / p[3]  # Деление
    else:  # У нас просто фактор
        p[0] = p[1]


def p_factor(p):
    """factor : LPAREN expression RPAREN
    | sqpar_val
    | verticalbar
    | ID
    | CONST ID"""
    if len(p) == 4:  # Если у нас выражение в скобках
        p[0] = p[2]  # Вернем результат выражения
    if len(p) == 2:
        p[0] = ("const", p[1])
    if len(p) == 1:
        p[0] = p[1]


def p_sqpar_val(p):
    """sqpar_val : LSQPAREN NUMBER RSQPAREN
    | LSQPAREN FLOAT RSQPAREN
    | LSQPAREN STRING RSQPAREN"""
    if type(p[2]) == float:
        p[0] = ("[", p[2], "]")
    if type(p[2]) == int:
        p[0] = ("[", p[2], "]")
    if type(p[2]) == str:
        p[0] = ("[", p[2], "]")


def p_write(p):
    """write : WRITE LPAREN return_list RPAREN"""
    p[0] = ("write", "(", p[3], ")")


def p_read(p):
    """read : READ LPAREN RPAREN"""
    p[0] = ("write", "(", ")")


def p_verticalbar(p):
    """verticalbar : VERTICALBAR ID VERTICALBAR"""
    p[0] = ("|", p[1], "|")


def p_method(p):
    """method : METHOD LPAREN argument_list RPAREN
    | ID METHOD LPAREN RPAREN"""
    if len(p) == 5:
        p[0] = (p[1], "(", p[3], ")")
    else:
        p[0] = (p[2], "(", ")")


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input(data)
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
