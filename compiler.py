# coding=utf-8
import AST
from AST import addToClass

# opcodes de la SVM
#    PUSHC <val>     pushes the constant <val> on the stack
#    PUSHV <id>      pushes the value of identifier <id> on the stack
#    SET <id>        pops a value from the top of stack and sets <id>
#    PRINT           pops a value from the top of stack and print it
#    ADD,SUB,DIV,MUL pops 2 values from the top of stack and compute them
#    USUB            changes the sign of the number on the top of stack
#    JMP <tag>       jump to :<tag>
#    JIZ,JINZ <tag>  pops a value from the top of stack and jump to :<tag> if (not) zero

# chaque opération correspond à son instruction d'exécution de la machine SVM
operations = {
	'+' : 'ADD',
	'-' : 'SUB',
	'*' : 'MUL',
	'/' : 'DIV'
}

def whilecounter():
	whilecounter.current += 1
	return whilecounter.current
whilecounter.current = 0

# noeud de programme
# retourne la suite d'opcodes de tous les enfants
@addToClass(AST.ProgramNode)
def compile(self):
	resultPython = ""
	for c in self.children:
		resultPython += c.compile()
	return resultPython

# Commentaire
@addToClass(AST.CommentNode)
def compile(self):
	resultPython = ""
	comment = None
	if(len(self.children) == 2) :
		resultPython += self.children[0].compile()
		comment = self.children[1].compile()
	else :
		comment = self.children[0].compile()

	# Multiple line comment
	if(comment[0] == "O") :
		resultPython += "#" + comment[4:-4].replace("\n", "\n#")[:-1]
	# Single line comment
	else:
		resultPython += "#" + comment[3:] + "\n"
	
	return resultPython


# noeud terminal
@addToClass(AST.TokenNode)
def compile(self):
	return str(self.tok)

@addToClass(AST.StringNode)
def compile(self):
	return self.tok

# Opération arithmétique binaire
@addToClass(AST.OpNode)
def compile(self):
	resultPython = ""
	# modulo, min, max
	if(len(self.op) > 1) :
		if(self.op == "MOD OF") :
			resultPython += self.children[0].compile() + " % " + self.children[1].compile()
		elif(self.op == "BIGGR OF") :
			resultPython += "max(" + self.children[0].compile() + "," + self.children[1].compile() + ")"
		elif(self.op == "SMALLR OF") :	
			resultPython += "min(" + self.children[0].compile() + "," + self.children[1].compile() + ")"
	# +, -, *, /
	else:
		resultPython += self.children[0].compile()
		resultPython += self.op
		resultPython += self.children[1].compile()
	
	return resultPython + "\n"

# Opération incrémentale (unaire)
@addToClass(AST.IncOpNode)
def compile(self):
	return self.children[0].tok + " " + self.op + "= 1\n"

# Opération de comparaison
@addToClass(AST.CompNode)
def compile(self):
	resultPython = ""
	resultPython += self.children[0].compile()
	resultPython += " " + self.op + " "
	resultPython += self.children[1].compile()
	
	return resultPython + "\n"

# Opération booleen
@addToClass(AST.BoolOpNode)
def compile(self):
	resultPython = ""
	# not
	if(len(self.children) == 1) :
		resultPython += "not "
		resultPython += "True" if self.children[0].tok == '0' else "False"
	# and, or
	else:
		resultPython += "True" if self.children[0].tok == '0' else "False"
		resultPython += " " + self.op + " "
		resultPython += "True" if self.children[1].tok == '0' else "False"
	return resultPython + "\n"

# noeud d'assignation de variable
# exécute le noeud à droite du signe =
# dépile un élément et le met dans ID
@addToClass(AST.AssignNode)
def compile(self):
	resultPython = ""
	resultPython += self.children[0].tok + " = "
	resultPython += self.children[1].compile() + "\n"
	return resultPython

# noeud d'assignation de variable
# exécute le noeud à droite du signe =
# dépile un élément et le met dans ID
@addToClass(AST.DeclarationNode)
def compile(self):
	resultPython = ""
	resultPython += self.children[0].tok + " = "
	resultPython += self.children[1].compile() + "\n"
	return resultPython

# noeud de boucle while
@addToClass(AST.WhileNode)
def compile(self):
	resultPython = "while "
	resultPython += self.children[0].compile()[:-1] + " :\n"
	block = self.children[1].compile()
	resultPython += "\t" + block.replace("\n", "\n\t")[:-1]
	return resultPython

# noeud de boucle if
@addToClass(AST.IfNode)
def compile(self):
	resultPython = "if "
	resultPython += self.children[0].compile()[:-1] + " :\n"
	blockIf= self.children[1].compile()
	resultPython += "\t" + blockIf.replace("\n", "\n\t")[:-1]
	# test if "else" exist
	if(len(self.children) == 3):
		blockElse = self.children[2].compile()
		resultPython += "else :\n\t" + blockElse.replace("\n", "\n\t")[:-1]
	return resultPython

# noeud de boucle for
@addToClass(AST.ForNode)
def compile(self):
	resultPython = "for " + self.value + " in range(" + self.value + ", "
	resultPython += self.until.compile() + ", "
	resultPython += "1" if self.inc == "+" else "-1"
	resultPython += ") :\n"
	block = self.children[0].compile()
	resultPython += "\t" + block.replace("\n", "\n\t")[:-1]
	return resultPython

@addToClass(AST.BreakNode)
def compile(self):
	return "break\n"

if __name__ == "__main__":
	from parserLOL import parse
	import sys, os
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	print(ast)
	compiled = ast.compile()
	name = "result.py"   
	outfile = open(name, 'w')
	outfile.write(compiled)
	outfile.close()
	print ("Wrote output to", name)