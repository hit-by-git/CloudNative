import ast

class CloudNativeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        # Check for modern "Cloud-Native" decorators (e.g., FastAPI, AWS Lambda)
        is_cloud_native = any(
            isinstance(d, ast.Call) and getattr(d.func, 'id', '') in ['api_route', 'handler']
            or getattr(d, 'id', '') in ['app', 'task']
            for d in node.decorator_list
        )
        
        self.classes[node.name] = {
            "bases": [b.id for b in node.bases if isinstance(b, ast.Name)],
            "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
            "is_cloud_native": is_cloud_native
        }
        self.generic_visit(node)

# Usage check
# visitor = CloudNativeVisitor()
# visitor.visit(ast.parse(open("your_code.py").read()))