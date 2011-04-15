import sys
from ast_node import Node

precedence = (
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'RSHIFT', 'LSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD')
    )

def p_translation_unit(t):
	"""
    translation_unit : external_declaration
    				 | translation_unit external_declaration
	"""
	if len(t) == 2:
		t[0] = Node('program', t[1])
	else:
		t[0] = Node('program', t[1] + t[2])

def p_external_declaration(t):
    """
    external_declaration : function_definition
    					 | declaration
    """
    t[0] = t[1]

def p_function_definition(t):
    """
    function_definition : type_specifier declarator LPAREN RPAREN compound_statement
    """
    t[0] = Node('func_def', t[1], t[2], t[5])

def p_declaration_list(t):
	"""
	declaration_list : declaration
					 | declaration_list declaration
	"""
	if len(t) == 2:
		t[0] = Node('declaration_list', t[1])
	else:
		t[0] = t[1] + t[2]

def p_compound_statement(t):
	"""
    compound_statement : LBRACE declaration_list statement_list RBRACE
    					| LBRACE statement_list RBRACE
    					| LBRACE declaration_list RBRACE
    					| LBRACE RBRACE
	"""
	if len(t) == 5:
		t[0] = Node('func_body', t[2], t[3])
	elif len(t) == 4:
		t[0] = Node('func_body', t[2])
	else:
		t[0] = Node('func_body', None)

def p_statement_list(t):
	"""statement_list : statement
    				  | statement_list statement
	"""
	if len(t) == 2:
		t[0] = Node('statement_list',t[1])
	else:
		t[0] = t[1] + t[2]


def p_declaration(t):
    'declaration : type_specifier init_declarator_list SEMI'
    t[0] = Node('var_decl', t[1], t[2])

def p_init_declarator_list(t):
    """init_declarator_list : init_declarator
    						| init_declarator_list COMMA init_declarator
    """
    if len(t) == 2:
    	t[0] = t[1]
    else:
    	t[0] = t[1] + t[3]
    
def p_init_declarator(t):
    """
    init_declarator : declarator
    				| declarator EQUALS initializer
    """
    if len(t) == 2:
    	t[0] = Node('var', t[1])
    else:
    	t[0] = Node('var_init', t[1], t[3])

def p_declarator(t):
	"""
	declarator : IDENTIFIER
				| declarator LBRACKET INT_CONST RBRACKET
	"""
	if len(t) == 2:	
		t[0] = Node('identifier', t[1])
	else:
		t[0] = t[1] + t[3]

def p_initializer(t):
    """
    initializer : IDENTIFIER
    			| constant
    """
    t[0] = t[1]

def p_type_specifier(t):
    '''type_specifier : PRAZNINA
                      | ZNAK
                      | CIJELI
                      | PLUTAJUCI
                      '''
    t[0] = t[1]

def p_statement(t):
    """
     statement : labeled_statement
               | expression_statement
               | compound_statement
               | selection_statement
               | iteration_statement    
               | jump_statement
    """
    t[0] = t[1]

def p_labeled_statement(t):
	"""
	labeled_statement : SLUCAJ constant_expression COLON statement
					  | PRETPOSTAVLJENO COLON statement
	"""
	if len(t) == 4:
		t[0] = Node('While', t[2], t[4])
	else:
		t[0] = t[3]

def p_expression_statement(t):
	"""
	expression_statement : expression SEMI
	"""
	t[0] = t[1]
	
def p_expression(t):
	"""expression : conditional_expression
				  | unary_expression assignment_operator expression
    """
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('assignment', t[2], t[1], t[3])


def p_expression_opt(t):
	"""expression_opt : empty
					  | expression
	"""
	t[0] = t[1]

def p_selection_statement_1(t):
	"""
	selection_statement : AKO LPAREN expression RPAREN statement
						| AKO LPAREN expression RPAREN statement INACE statement
	"""
	if len(t) == 6:
		t[0] = Node('if', t[3], t[5])
	else:
		t[0] = Node('if', t[3], t[5], t[7])

def p_selection_statement_2(t):
	"""
	selection_statement : PREBACI LPAREN expression RPAREN statement
	"""
	t[0] = Node('switch', t[3])

def p_iteration_statement_1(t):
	"""
	iteration_statement : DOKGOD LPAREN expression RPAREN statement
	"""
	t[0] = Node('while', t[3], t[5])
	
def p_iteration_statement_2(t):
	"""
	iteration_statement : ZA LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
	"""
	t[0] = Node('for', t[3], t[5], t[7], t[9])

def p_iteration_statement_3(t):
	"""
	iteration_statement : CINI statement DOKGOD LPAREN expression RPAREN SEMI
	"""
	t[0] = Node('dowhile', t[2], t[5])

def p_jump_statement(t):
	"""
    jump_statement : NASTAVI SEMI
    			   | PRELOMI SEMI
    			   | VRATI expression_opt SEMI
    """
	if len(t) == 3:
		t[0] = t[1]
	else:
		t[0] = Node('return', t[2])

def p_constant_expression(t):
    'constant_expression : conditional_expression'
    t[0] = t[1]

def p_assigment_operator(t):
	"""assignment_operator : EQUALS
                            | XOREQUAL   
                            | TIMESEQUAL  
                            | DIVEQUAL    
                            | MODEQUAL    
                            | PLUSEQUAL   
                            | MINUSEQUAL  
                            | LSHIFTEQUAL 
                            | RSHIFTEQUAL 
                            | ANDEQUAL    
                            | OREQUAL  
    """
	t[0] = t[1]
	
def p_conditional_expression(t):
    """ conditional_expression  : binary_expression
                                | binary_expression CONDOP expression COLON conditional_expression
    """
    if len(t) == 2:
		t[0] = t[1]

def p_binary_expression_1(t):
	""" binary_expression   : unary_expression
                            | binary_expression TIMES binary_expression
                            | binary_expression DIVIDE binary_expression
                            | binary_expression MOD binary_expression
                            | binary_expression PLUS binary_expression
                            | binary_expression MINUS binary_expression
                            | binary_expression RSHIFT binary_expression
                            | binary_expression LSHIFT binary_expression
                            | binary_expression LT binary_expression
                            | binary_expression LE binary_expression
                            | binary_expression GE binary_expression
                            | binary_expression GT binary_expression
                            | binary_expression EQ binary_expression
                            | binary_expression NE binary_expression
                            | binary_expression AND binary_expression
                            | binary_expression OR binary_expression
                            | binary_expression XOR binary_expression
                            | binary_expression LAND binary_expression
                            | binary_expression LOR binary_expression
	"""
	if len(t) > 2:
		t[0] = Node('BinOp', t[2], t[1], t[3])
	else:
		t[0] = t[1]

def p_binary_expression_2(t):
	'binary_expression : LPAREN binary_expression RPAREN'
	t[0] = t[2]
    
	
def p_unary_expression(t):
	"""unary_expression : postfix_expression
        	| PLUSPLUS unary_expression 
			| MINUSMINUS unary_expression
	"""
	if len(t) == 2:
		t[0] = t[1]
	else:
		t[0] = Node('prefix', t[1], t[2])

def p_postfix_expression(t):
	"""postfix_expression : primary_expression
						  | postfix_expression LPAREN argument_expression_list RPAREN
						  | postfix_expression LPAREN RPAREN
				          | postfix_expression PLUSPLUS
						  | postfix_expression MINUSMINUS
	"""
	if len(t) == 2:
		t[0] = t[1]
	elif len(t) == 4:
		t[0] = Node('func_call', t[1])
	elif len(t) == 5:
		t[0] = Node('func_call', t[1], t[3])
	else:
		t[0] = Node('postfix', t[1], t[2])


def p_argument_expression_list(t):
    """ argument_expression_list : expression 
                                 | argument_expression_list COMMA expression
    """
    if len(t) == 2: # single expr
        t[0] = t[1]
    else:
        t[0] = t[1] + t[3]
		
def p_primary_expression_1(t):
	"""primary_expression : IDENTIFIER
						  | primary_expression LBRACKET INT_CONST RBRACKET
	"""
	if len(t) == 2:
		t[0] = Node('identifier', t[1])
	else:
		t[0] = t[1] + t[3]
	
def p_primary_expression_2(t):
	"""primary_expression : constant				
	"""
	t[0] = t[1]
	
def p_constant(t):
	"""constant : int_const
				| str_const
				| float_const
	"""
	t[0] = t[1]
	
def p_int_const(t):
	"""int_const : INT_CONST
				 | OCTAL_CONST
				 | HEX_CONST
	"""
	t[0] = Node('cijeli', t[1])
	
def p_str_const(t):
	'str_const : STR_CONST'
	t[0] = Node('znak', t[1])
	
	
def p_float_const(t):
	'float_const : FLOAT_CONST'
	t[0] = Node('plutajuci', t[1])				
	
def p_empty(t):
    'empty :'
    pass

def p_error(t):
	print "Syntax error in input, in line %d!" % t.lineno
	sys.exit()