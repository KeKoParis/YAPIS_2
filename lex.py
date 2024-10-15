import re
import ply.lex as lex

# List of token names. This is always required
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


class My_Lexer(object):
    tokens = a_tokens + list(reserved.values())

    states = (("indentation", "inclusive"),)  # Exclusive 'indentation' state

    def __init__(self):
        self.indent_stack = [0]  # Track indentation levels with a stack

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

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = reserved.get(t.value, "ID")
        return t

    def t_METHOD(self, t):
        r"\.[a-zA-Z_][a-zA-Z_0-9]*"
        return t

    def t_STRING(self, t):
        r"\"(.)*\" "
        t.value = t.value[1:-1]
        return t

    def t_COMMENT(self, t):
        r"\#(.)*"
        pass

    def t_FLOAT(self, t):
        r"\d+\.\d+"
        t.value = float(t.value)
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

        # Handle indentation (in 'indentation' state)

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        t.lexer.begin("indentation")  # Switch to indentation state

    t_indentation_ignore = " "

    def t_indentation_count(self, t):
        r"end"
        self.indent_stack = [0]

        t.type = "DEDENT"
        return t

    def t_indentation_indentation(self, t):
        r"\t{1,8}"  # Match one or more spaces or tabs
        curr_val = t.value
        current_indent = len(curr_val)  # Count spaces or tabs at the start of the line
        # print(f"indends: {current_indent}  {self.indent_stack[-1]}")
        # Compare the current indentation with the top of the indent stack
        if current_indent > self.indent_stack[-1]:
            self.indent_stack.append(current_indent)
            t.type = "INDENT"
            return t
        elif current_indent < self.indent_stack[-1]:
            dedent_count = 0
            while self.indent_stack and current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                dedent_count += 1
            t.type = "DEDENT"
            t.value = dedent_count
            return t

        # If we reach here, we have a case of the same level of indentation
        t.lexer.begin("INITIAL")

    # Ignore all characters in the indentation state
    def t_indentation_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)  # Skip illegal character without printing

    # Ignore spaces and tabs in other parts of the code
    t_ignore = " \t"

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            print(tok)  # Print the token
