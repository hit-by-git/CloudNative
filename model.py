import torch
from torch_geometric.nn import GATConv
import torch.nn.functional as F

class ClassDiagramGNN(torch.nn.Module):
    def __init__(self, num_node_features, hidden_channels):
        super(ClassDiagramGNN, self).__init__()
        # Layer 1: Learn class embeddings
        self.conv1 = GATConv(num_node_features, hidden_channels, heads=4)
        # Layer 2: Refine embeddings for relationship prediction
        self.conv2 = GATConv(hidden_channels * 4, hidden_channels, heads=1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = self.conv2(x, edge_index)
        return x # These are the "embeddings" used to predict relationships