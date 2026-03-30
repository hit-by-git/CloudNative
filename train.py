import torch
import torch.nn.functional as F
from torch_geometric.utils import negative_sampling
from dataset_builder import build_pyg_data
from model import ClassDiagramGNN # From our previous step

def train():
    # 1. Load Data & Initialize Model
    data, mapping = build_pyg_data("graph_data.json")
    
    # We have 2 node features: [method_count, is_cloud]
    model = ClassDiagramGNN(num_node_features=2, hidden_channels=16)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    model.train()
    for epoch in range(1, 201):
        optimizer.zero_grad()

        # 2. Forward Pass: Get Node Embeddings
        z = model(data.x, data.edge_index)

        # 3. Generate Negative Samples (Edges that DO NOT exist in code)
        neg_edge_index = negative_sampling(
            edge_index=data.edge_index, num_nodes=data.num_nodes,
            num_neg_samples=data.edge_index.size(1), method='sparse')

        # 4. Calculate Link Probabilities (Dot product of embeddings)
        # Real edges should score high, negative edges should score low
        edge_label_index = torch.cat([data.edge_index, neg_edge_index], dim=-1)
        edge_label = torch.cat([
            torch.ones(data.edge_index.size(1)),
            torch.zeros(neg_edge_index.size(1))
        ], dim=0)

        out = (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)
        
        # 5. Loss and Backpropagation
        loss = F.binary_cross_entropy_with_logits(out, edge_label)
        loss.backward()
        optimizer.step()

        if epoch % 20 == 0:
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')

if __name__ == "__main__":
    train()