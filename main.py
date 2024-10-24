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
	b = matrix a
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

data_2 = """o = [9]
func main()
	a = [1, 2, 4]
	b = [4, 5, 6]
	
	write( a[0] > b[2] )
	write( a[2] >= b[0] )
	write( a[0] < b[2] )
	write( a[0] == b[2] )
	write( a[2] == b[0] )

	c = a + b
	write( c )
	
	c = a - b
	write( c )

	c = a * [5]
	write( c )

	c = a * b
	write( c )
	global o
	c = |v|
	write( c )
	write(|(([5]+c).add(8)).add(9) + a|)
	write(o)

	return [0]"""

data_3 = """func main()
	d = [[1, 2] [3, 4]]
 	e = [[3,4][5, 6]]
	
	f = d + e 
	write(f)

	f = d - e
	write(f)

	n = [2.5]
	f = d * n
	write(f)

	i = [0]
	p = d[i] 
	write(f)

	d[i] * [5]
	write(d)

	t = |m|
	write(t)
	
	t = [4, 1.1]
	q = d * t
	write(q)

	return [0]
"""

#print(repr(data))

# my_lexer = My_Lexer()
# my_lexer.build()
# my_lexer.input(data_2)
