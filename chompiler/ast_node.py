class Node(object):
	def __init__(self, t, *args):
		self.type = t
		self.args = args
 
	def __str__(self):
		s = "type: " + str(self.type) + "\n"
		s += "".join( ["i: " + str(i) + "\n" for i in self.args])
		return s
		
	def __add__(self, other):
		argumenti = self.args + (other,)
		return Node(self.type, *argumenti)
		
	def ispisi(self, offset):
		s = "type: " + str(self.type) + "\n"
		#s += "".join( [" " * offset + "i: " + str(i) + "\n" for i in self.args])
		for i in self.args:
			if i.__class__ != Node:
				s += " " * offset + "i: " + str(i) + "\n"
			else:
				s += " " * offset + "i: " + i.ispisi(offset+2) + "\n"
		return s		