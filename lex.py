import ply.lex as lex

reserved_words = (
	'BTW',
	'OBTW',
	'TLDR',
	'ITZ',
	'UPPIN',
	'NERFIN',
	'AN',
	'FAIL',
	'WIN',
	'NOT',
	'DIFFRINT',
	'OIC',
	'WILE',
	'GTFO'
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'IDENTIFIER',

	'SL_COMMENT',
	'ML_COMMNENT',
	
	'HAS',
	'AN',
	'ITZ',
	'IDENTIFIER',
	'NUMBER',
	'STRING',
	'ADD_OP',
	'MUL_OP',
	'MOD_OP',
	'MAX_OP',
	'MIN_OP',
	'INC_OP',
	'COMP',
	'IF',
	'IF_TRUE',
	'IF_FALSE',
	'IF_END'	
)

literals = '();={}'

def t_ADD_OP(t):
	r'[+-]'
	return t
	
def t_MUL_OP(t):
	r'[*/]'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t
	
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
