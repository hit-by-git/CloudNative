import json
import torch
from torch_geometric.data import Data

def build_pyg_data(json_filepath):
    with open(json_filepath, 'r') as f:
        graph_data = json.load(f)

    # 1. Map String IDs to Integer Indices
    node_mapping = {node['id']: idx for idx, node in enumerate(graph_data['nodes'])}
    
    # 2. Build Node Features Tensor (x)
    # For now, we use [method_count, is_cloud_flag] as features.
    # Note: Later, you can replace this with LLM embeddings of the class source code!
    x_features = []
    for node in graph_data['nodes']:
        method_count = float(node['methods'])
        is_cloud = 1.0 if node.get('is_cloud', False) else 0.0
        x_features.append([method_count, is_cloud])
    
    x = torch.tensor(x_features, dtype=torch.float)

    # 3. Build Edge Index Tensor (Connectivity)
    # PyG expects a [2, num_edges] tensor where row 0 is source, row 1 is target
    source_nodes = []
    target_nodes = []
    
    for edge in graph_data['edges']:
        # Ensure both nodes exist in our mapping (handles missing external imports)
        if edge['source'] in node_mapping and edge['target'] in node_mapping:
            source_nodes.append(node_mapping[edge['source']])
            target_nodes.append(node_mapping[edge['target']])
            
    edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)

    # 4. Create the PyG Data Object
    data = Data(x=x, edge_index=edge_index)
    
    return data, node_mapping

# Test the builder
# pyg_data, mapping = build_pyg_data("graph_data.json")
# print(f"Graph ready: {pyg_data.num_nodes} nodes, {pyg_data.num_edges} edges.")