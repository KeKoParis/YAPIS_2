from lex import My_Lexer


data = """
a = [0, 2.2]
    b =  (vector)
"""

my_lexer = My_Lexer()
my_lexer.build()
lexer = my_lexer.get_lexer(data)
# Tokenize

