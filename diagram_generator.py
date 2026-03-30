import json

class MermaidGenerator:
    def __init__(self, json_filepath):
        with open(json_filepath, 'r') as f:
            self.data = json.load(f)

    def generate_markdown(self, output_file="architecture.md"):
        lines = ["```mermaid", "classDiagram"]
        
        # 1. Define custom styles for Cloud-Native components
        lines.append("    %% Custom Cloud Styles")
        lines.append("    classDef cloudClass fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000;")
        lines.append("    classDef standardClass fill:#ffffff,stroke:#333,stroke-width:1px;")

        # 2. Process Nodes (Classes)
        for node in self.data['nodes']:
            class_name = node['id']
            lines.append(f"    class {class_name} {{")
            
            # Add Stereotype if it's a cloud component
            if node.get('is_cloud'):
                lines.append("        <<Serverless / Microservice>>")
            
            # Add a placeholder for methods based on the method count
            method_count = node.get('methods', 0)
            if method_count > 0:
                lines.append(f"        +{method_count} active methods()")
                
            lines.append("    }")

            # Apply the specific style class using Mermaid's cssClass syntax
            if node.get('is_cloud'):
                lines.append(f"    cssClass \"{class_name}\" cloudClass")
            else:
                lines.append(f"    cssClass \"{class_name}\" standardClass")
        # 3. Process Edges (Relationships)
        for edge in self.data['edges']:
            source = edge['source']
            target = edge['target']
            rel_type = edge['type']
            
            if rel_type == "inheritance":
                # Mermaid syntax for inheritance: Base <|-- Derived
                # Note: AST parses target as the base class
                lines.append(f"    {target} <|-- {source}")
            else:
                # Standard dependency/association
                lines.append(f"    {source} --> {target} : depends on")

        lines.append("```")

        # 4. Write to Markdown file
        with open(output_file, 'w') as f:
            f.write("\n".join(lines))
        
        print(f"Diagram successfully generated at: {output_file}")

# Execution
if __name__ == "__main__":
    generator = MermaidGenerator("graph_data.json")
    generator.generate_markdown()