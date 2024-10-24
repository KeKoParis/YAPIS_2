import ply.yacc as yacc
import ply.lex as lex


a_tokens = [
    "FLOAT",
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "LSQPAREN",
    "RSQPAREN",
    "VERTICALBAR",
    "COMMA",
    "EQ",
    "EQEQ",
    "MORE",
    "LESS",
    "ID",
    "INDENT",
    "DEDENT",
    "STRING",
    "METHOD",
]

reserved = {
    "func": "FUNC",
    "global": "GLOBAL",
    "do": "DO",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "return": "RETURN",
    "matrix": "MATRIX",
    "vector": "VECTOR",
    "call": "CALL",
    "until": "UNTIL",
    "for": "FOR",
    "read": "READ",
    "write": "WRITE",
    "const": "CONST",
    "in": "IN",
}


tokens = a_tokens + list(reserved.values())

states = (("indentation", "inclusive"),)  # Exclusive 'indentation' state

indent_stack = [0]  # Track indentation levels with a stack

# Regular expression rules for simple tokens
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LSQPAREN = r"\["
t_RSQPAREN = r"\]"
t_VERTICALBAR = r"\|"
t_COMMA = r","
t_EQ = r"="
t_EQEQ = r"=="
t_MORE = r">"
t_LESS = r"<"


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_METHOD(t):
    r"\.[a-zA-Z_][a-zA-Z_0-9]*"
    return t


def t_STRING(t):
    r"\"(.)*\" "
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r"\#(.)*"
    pass


def t_FLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

    # Handle indentation (in 'indentation' state)


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    t.lexer.begin("indentation")  # Switch to indentation state


t_indentation_ignore = " "


def t_indentation_count(t):
    r"end"
    global indent_stack
    indent_stack = [0]

    t.type = "DEDENT"
    return t


def t_indentation_indentation(t):
    r"\t{1,8}"  # Match one or more spaces or tabs
    global indent_stack

    curr_val = t.value
    current_indent = len(curr_val)  # Count spaces or tabs at the start of the line
    # print(f"indends: {current_indent}  {indent_stack[-1]}")
    # Compare the current indentation with the top of the indent stack
    if current_indent > indent_stack[-1]:
        indent_stack.append(current_indent)
        t.type = "INDENT"
        return t
    elif current_indent < indent_stack[-1]:
        dedent_count = 0
        while indent_stack and current_indent < indent_stack[-1]:
            indent_stack.pop()
            dedent_count += 1
        t.type = "DEDENT"
        t.value = dedent_count
        return t

    # If we reach here, we have a case of the same level of indentation
    t.lexer.begin("INITIAL")


# Ignore all characters in the indentation state
def t_indentation_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)  # Skip illegal character without printing


# Ignore spaces and tabs in other parts of the code
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


#
# PARESER
#

tree = []

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


with open("data_1.txt", "r") as f:
    data = f.read()

    lexer = lex.lex()

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    while True:
        try:
            s = input(data)
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print("Hello")
