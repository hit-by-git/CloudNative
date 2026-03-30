import ast
import os
import json

class RepoParser:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.data = {"nodes": [], "edges": []}

    def parse(self):
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".py"):
                    self._parse_file(os.path.join(root, file))
        return self.data

    def _parse_file(self, file_path):
        with open(file_path, "r", errors="ignore") as f:
            try:
                tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        
                        # --- NEW SMART CLOUD DETECTION ---
                        # 1. Check if the class inherits from FastAPI/Pydantic cloud models
                        base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
                        is_cloud_model = any(base in ['SQLModel', 'BaseModel'] for base in base_names)
                        
                        # 2. Check if any methods inside the class have API route decorators
                        has_api_route = False
                        for n in node.body:
                            if isinstance(n, ast.FunctionDef):
                                for d in n.decorator_list:
                                    # Matches @router.get(), @app.post(), etc.
                                    if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute):
                                        if d.func.attr in ['get', 'post', 'put', 'delete', 'patch']:
                                            has_api_route = True

                        # Flag as true if it matches either cloud pattern
                        is_cloud_final = is_cloud_model or has_api_route
                        # ---------------------------------

                        self.data["nodes"].append({
                            "id": node.name,
                            "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                            "is_cloud": is_cloud_final
                        })
                        
                        # Edge: Inheritance (Generalization)
                        for base in node.bases:
                            if isinstance(base, ast.Name):
                                self.data["edges"].append({"source": node.name, "target": base.id, "type": "inheritance"})
            except SyntaxError:
                pass

# Detailed Instruction: Run this on a small folder of Python scripts to test.
# parser = RepoParser("./path_to_your_scripts")
# print(json.dumps(parser.parse(), indent=2))
if __name__ == "__main__":
    # Point the parser at the backend directory of the cloned repo
    parser = RepoParser("./sample_code/backend/app")

    # Save the output to our JSON file
    with open("graph_data.json", "w") as f:
        json.dump(parser.parse(), f, indent=2)
    print("Data collection complete. graph_data.json created.")