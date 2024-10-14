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
    "COMMENT",
    "STRING",
    "METHOD"
]

reserved = {
    "func": "FUNC",
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
}


class My_Lexer(object):
    tokens = a_tokens + list(reserved.values())

    states = (("indentation", "inclusive"),)

    def __init__(self):
        self.indent_stack = [0] 
    


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
            print(tok) 


data = """
proc myProcedure(vector a) do
	write(a)

func multiplexMatrix(matrix a, matrix b) do
	return a * b

func main()
    const t = [1, 2, 3, 4]
    a = [1, 2, 3, 4]
    b = (matrix) a
    c = [[1, 2, 3] [4, 5, 6]]
    d = (vector) b  // [1, 2, 3, 4, 5, 6]

    a = d
	
	call myProcedure( a )

	res = []
	for ( i in a ) do
        res.add( call multiplex )
	
    i = [20]
	while (i  > [0] ) do
		i = i - [1]	
	
	i = [0]
	until (i  < [20] ) do
        i = i + [1]
	
	expectedLength = read()
	
    if ( res.length > expectedLength[0]) then
        write( "More" )
    else
        write( "Less" )
    return  [0]
"""

my_lexer = My_Lexer()
my_lexer.build()
my_lexer.input(data)