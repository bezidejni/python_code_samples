import logging

from ply import yacc,lex
from lexer import *
from parser import *
from semantic import *
#from graph import graph




def get_input(file=False):
	if file:
		f = open(file,"r")
		data = f.read()
		f.close()
	else:
		data = ""
		while True:
			try:
				data += raw_input() + "\n"
			except:
				break
	return data
 
def main(filename='test.ch'):
	log = logging.getLogger()
	 
	logging.basicConfig(
	    level = logging.DEBUG,
	    filename = "parselog.txt",
	    filemode = "w",
	    format = "%(filename)10s:%(lineno)4d:%(message)s"
	)
	
	if filename:
		f = open(filename,"r")
		data = f.read()
		f.close()
		
	lexer = lex.lex()
	lexer.input(data)
	
	# Tokenize
	while True:
	    tok = lexer.token()
	    if not tok: break      # No more input
	    #print tok	
			
	yacc.yacc(debug=True, errorlog=log)    
	
	ast =  yacc.parse(data,lexer = lex.lex(nowarn=1), debug=log)
	#graph(ast, 'graf')
	#import code; code.interact(local=locals())
	print ast.ispisi(0)
	try:
		check(ast)
		print "Semanticka analiza uspjesno izvrsena!"
	except Exception, e:
		print "Error: %s" % e
		sys.exit()
 
if __name__ == '__main__':
	main()