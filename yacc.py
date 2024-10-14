import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex import tokens


def p_block(p):
    "block : INDENT statement_list DEDENT"
    p[0] = p[2]


def p_statement_list(p):
    """statement_list : statement_list statement
    | statement"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    """statement : assignment
    | expression
    | if_statement
    | loop"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : ID EQ expression"""
    p[0] = ("assign", p[1], p[3])


def p_expression(p):
    """expression : expression PLUS term
    | expression MINUS term
    | term"""
    if len(p) == 4:
        if p[2] == "+":
            p[0] = ("+", p[1], p[3])
        if p[2] == "-":
            p[0] = ("-", p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    """term : term TIMES factor
    | term DIVIDE factor
    | factor"""
    if len(p) == 4:
        if p[2] == "*":
            p[0] = ("*", p[1], p[2])
        if p[2] == "/":
            p[0] = ("/", p[1], p[2])
    else:
        p[0] = p[1]


def p_factor(p):
    """factor : LSQPAREN NUMBER RSQPAREN
    | LSQPAREN FLOAT RSQPAREN
    | ID
    | LPAREN expresion RPAREN"""
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 4:
        if p[1] == '[':
            p[0] = p[2]
        if p[1] == '(':
            p[0] =  

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input("calc > ")
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
