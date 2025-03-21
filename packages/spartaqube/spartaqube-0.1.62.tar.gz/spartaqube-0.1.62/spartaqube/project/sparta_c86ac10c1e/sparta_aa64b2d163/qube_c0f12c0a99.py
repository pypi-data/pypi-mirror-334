import ast
def sparta_4cc821126f(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_9dbe1c11d3(script_text):return sparta_4cc821126f(script_text)