# ------------------------------------------------------------
# lexer.py
#
# leksicki analizator za programski jezik C
# ------------------------------------------------------------
import ply.lex as lex
from ply.lex import TOKEN


# Popis rezerviranih rijeci jezika i njihove klase
reserved = (
    'AKO', 'INACE', 'SKOCI', 'ZA', 'PREBACI', 'SLUCAJ', 'PRELOMI', 'NASTAVI',
    'VRATI', 'DOKGOD', 'CINI', 'PRETPOSTAVLJENO', 'CIJELI', 'ZNAK', 'PLUTAJUCI', 'PRAZNINA'
)

# Popis svih tokena tj klasa
tokens = reserved + (
   'IDENTIFIER',
   'INT_CONST',
   'FLOAT_CONST',
   'OCTAL_CONST',
   'HEX_CONST',
   'STR_CONST',
     'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    'PLUSPLUS', 'MINUSMINUS',

    # Structure dereference (->)
    'ARROW',

    # Conditional operator (?)
    'CONDOP',
    
    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Ellipsis (...)
    'ELLIPSIS',
)

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MOD              = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators

t_EQUALS           = r'='
t_TIMESEQUAL       = r'\*='
t_DIVEQUAL         = r'/='
t_MODEQUAL         = r'%='
t_PLUSEQUAL        = r'\+='
t_MINUSEQUAL       = r'-='
t_LSHIFTEQUAL      = r'<<='
t_RSHIFTEQUAL      = r'>>='
t_ANDEQUAL         = r'&='
t_OREQUAL          = r'\|='
t_XOREQUAL         = r'^='

# Increment/decrement
t_PLUSPLUS         = r'\+\+'
t_MINUSMINUS       = r'--'

# ->
t_ARROW            = r'->'

# ?
t_CONDOP           = r'\?'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'
t_ELLIPSIS         = r'\.\.\.'

# Identifiers and reserved words

reserved_map = { }
for r in reserved:
    reserved_map[r.lower()] = r

# Tokeni definirani regularnim izrazima
#t_CONSTANT = r'(0[Xx][0-9A-Za-z]+)|(0[0-7]+)|([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)|([0-9]+)'
t_STR_CONST = r'"(.|\")*" | \'(.|\')*\''
t_INT_CONST = r'[1-9][0-9]*'
t_OCTAL_CONST = r'0[0-7]*'
t_HEX_CONST = r'0[xX][0-9a-fA-F]+'

exponent_part = r"""([eE][-+]?[0-9]+)"""
fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
floating_constant = '(((('+fractional_constant+')'+exponent_part+'?)|([0-9]+'+exponent_part+'))[FfLl]?)'

@TOKEN(floating_constant)
def t_FLOAT_CONST(t):
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]([0-9]|[A-Za-z_])*'
    t.type = reserved_map.get(t.value,'IDENTIFIER')
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'(\r\n)|(\n)'
    t.lexer.lineno += 1


def t_comment(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    t.lexer.lineno += t.value.count('\n')

# Error handling rule
def t_error(t):
    print "Greska! Linija %s: nepoznat znak %s" % (t.lexer.lineno, t.value[0])
    t.lexer.skip(1)




if __name__ == '__main__':
	# Build the lexer
	lexer = lex.lex()
	
	data = '''
// komentar

/*
komentar 2
*/

cijeli glavniaa ()
{
	a = 3;
	b = 3.4;
	c = 012;
	d = 0x1A;
}

a = 2 + 3;
	'''
	
	# Give the lexer some input
	lexer.input(data)
	
	# Tokenize
	while True:
	    tok = lexer.token()
	    if not tok: break      # No more input
	    print tok
