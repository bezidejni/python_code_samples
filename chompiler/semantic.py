types = ['cijeli','plutajuci','znak','praznina']

class Any(object):
	def __eq__(self,o):
		return True
	def __ne__(self,o):
		return False

class Context(object):
	def __init__(self,name=None):
		self.variables = {}
		self.var_count = {}
		self.var_assigned = {}
		self.name = name
	
	def has_var(self,name):
		return name in self.variables
	
	def get_var(self,name):
		return self.variables[name]
	
	def set_var(self,name,typ):
		self.variables[name] = typ
		self.var_assigned[name] = 0
		self.var_count[name] = 0
		
	def set_assigned(self, name):
		self.var_assigned[name] = 1
		
	def is_assigned(self, name):
		return self.var_assigned[name]

contexts = []
functions = {
	'ispisio':('void',[
			("a",Any())
		]),
}

def pop():
	count = contexts[-1].var_count
	for v in count:
		if count[v] == 0:
			print "Upozorenje: varijabla %s je deklarirana, ali se ne koristi." % v
	contexts.pop()

def check_if_function(var):
	if var.lower() in functions and not is_function_name(var.lower()):
		raise Exception, "Funkcija imena %s vec postoji" % var
		
def is_function_name(var):
	for i in contexts[::-1]:
		if i.name == var:
			return True
	return False
		
		
def has_var(varn):
	var = varn.lower()
	check_if_function(var)
	for c in contexts[::-1]:
		if c.has_var(var):
			return True
	return False

def get_var(varn):
	var = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(var):
			c.var_count[var] += 1
			return c.get_var(var)
	raise Exception, "Varijabla %s se koristi prije definiranja" % var
	
def set_var(varn,typ):
	var = varn.lower()
	check_if_function(var)
	now = contexts[-1]
	if now.has_var(var):
		raise Exception, "Varijabla %s je vec definirana" % var
	else:
		now.set_var(var,typ.lower())

def set_assigned(varn):
	varn = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(varn):
			c.set_assigned(varn)
			return True
	return False	
	
def is_assigned(varn):
	varn = varn.lower()
	for c in contexts[::-1]:
		if c.has_var(varn):
			if c.is_assigned(varn):
				return True
	return False		
	
def get_params(node):
	if node.type == "parameter":
		return [check(node.args[0])]
	else:
		l = []
		for i in node.args:
			l.extend(get_params(i))
		return l
		
def flatten(n):
	if not is_node(n): return [n]
	if not n.type.endswith("_list"):
		return [n]
	else:
		l = []
		for i in n.args:
			l.extend(flatten(i))
		return l
		

def is_node(n):
	return hasattr(n,"type")

def check(node):
	if not is_node(node):
		if hasattr(node,"__iter__") and type(node) != type(""):
			for i in node:
				check(i)
		else:
			return node
	else:
		if node.type in ['identifier']:
			varn = node.args[0]
			if not has_var(varn):
				raise Exception, "Varijabla %s nije deklarirana" % varn
			#if not is_assigned(varn):
			#	print "Upozorenje: varijabla %s nije inicijalizirana" % varn
			return get_var(varn)
			
		elif node.type in types:
			return node.type	
			
		elif node.type in ['func_def']:
			ime = node.args[1].args[0].lower()
			tip = node.args[0].lower()
			check_if_function(ime)
  
			args = []
			functions[ime] = (tip,args)
 
 
			contexts.append(Context(ime))
			for i in args:
				set_var(i[0],i[1])
			check(node.args[2])
			pop()
		
		elif node.type in ['declaration_list', 'statement_list']:
			return check(node.args)
		
		elif node.type in ['var_decl']:
			ime = node.args[1].args[0].args[0]
			tip = node.args[0]
			set_var(ime, tip)
			check(node.args[1])
	
		elif node.type in ['assignment', 'var_init']:
			if node.type == 'assignment':
				c = 1
			else:
				c = 0
			varn = node.args[c].args[0].lower()
			if is_function_name(varn):
				vartype = functions[varn][0]
			else:
				if not has_var(varn):
					raise Exception, "Varijabla %s nije deklarirana" % varn
				vartype = get_var(varn)
			assgntype = check(node.args[c+1])
			if vartype != assgntype:
				raise Exception, "Varijabla %s je tipa %s i nemoguce je pridruziti vrijednost tipa %s" % (varn, vartype, assgntype)
			set_assigned(varn)


		
		elif node.type == "BinOp":
 
			op = node.args[0]
			vt1 = check(node.args[1])
			vt2 = check(node.args[2])
			
			if vt1 != vt2:
				raise Exception, "Argumenti operacije '%s' moraju biti istog tipa. Tipovi su %s i %s." % (op,vt1,vt2)

			return vt1		
					
		elif node.type in ['if','while','dowhile']:
			if node.type == 'dowhile':
				c = 1
			else:
				c = 0
			t = check(node.args[c])
			
 
			# check body
			check(node.args[1-c])
 
			# check else
			if len(node.args) > 2:
				check(node.args[2])		
		
		elif node.type in ['for']:
			check(node.args)
			
		elif node.type in ['prefix', 'postfix']:
			tip = check(node.args[0])
			if tip != 'cijeli':
				raise Exception, "Tip podatka kod operacije %s mora biti cijeli" % node.type
			
		elif node.type in ['program', 'func_body']:
			contexts.append(Context())
			check(node.args)
			pop()
			
		elif node.type in ['var','func_call']:
			pass
			
		else:
			print "semantic missing:", node.type