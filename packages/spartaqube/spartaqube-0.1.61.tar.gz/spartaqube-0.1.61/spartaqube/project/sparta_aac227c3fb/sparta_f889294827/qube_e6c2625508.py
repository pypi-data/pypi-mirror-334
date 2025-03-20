import ast
def sparta_3b4c97553d(code):
	B=ast.parse(code);A=set()
	class C(ast.NodeVisitor):
		def visit_Name(B,node):A.add(node.id);B.generic_visit(node)
	D=C();D.visit(B);return list(A)
def sparta_630a90b3dd(script_text):return sparta_3b4c97553d(script_text)