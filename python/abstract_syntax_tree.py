import ast
from pathlib import Path

"""
The ast library is used to load and travers the abstract syntax tree for Python code.

https://docs.python.org/3/library/ast.html
"""

with Path(__file__).open("r") as f:
    this = f.read()

parsed = ast.parse(this)

# We can dump the AST to see its structure
print(ast.dump(parsed, indent=2))

# We can also walk the AST to find specific nodes
for node in ast.walk(parsed):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        print(f"Found import: {ast.dump(node)}")


# A better way to do this is to define a visitor class. We inherit from ast.NodeVisitor
# and define methods named visit_<NodeType> for each node type we want to handle.
# The visitor will automatically call the appropriate method for each node type.
class Visitor(ast.NodeVisitor):
    def visit_Import(self, node: ast.Import) -> None:
        print(f"Found import: {ast.dump(node)}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        print(f"Found import from: {ast.dump(node)}")
        self.generic_visit(node)


# We can then create an instance of the visitor and use it to visit the AST
Visitor().visit(parsed)


# We can convert any part of the AST back to source code
source = ast.unparse(parsed)
# print(source)
