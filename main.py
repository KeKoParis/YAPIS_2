from lex import My_Lexer


data = """func myProcedure(vector a) do
	write(a)
    end

func multiplexMatrix(matrix a, matrix b) do
	write(a)
	return a * b
    end

func main() do
	const t = a * b
    a = [1, 2, 3, 4]
	b = (matrix) a
	c = [[1, 2, 3] [4, 5, 6]]
	d = (vector) b

	a = d

	call myProcedure( a )

	res = []

	for ( i in a ) do
		res.add( call multiplex )

	i = [20]
	while ( i > [0] ) do
		i = i - [1]
		i = i - [1]

	i = [0]
	until ( i < [20] ) do
		i = i + [1]

	expectedLength = read()

	if ( res.length > expectedLength[0] ) then
		write( "More" )
	else
		write( "Less" )
	return [0]
    end"""

#print(repr(data))

my_lexer = My_Lexer()
my_lexer.build()
my_lexer.input(data)
