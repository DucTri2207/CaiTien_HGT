import dgl
import dgl.nn.pytorch
import torch
import torch.nn as nn


class ImprovedHGT(nn.Module):
    """Lightweight HGT close to the original AMDGT branch with small upgrades.

    Improvements kept on purpose:
    - works with the updated heterograph that already includes reverse edges
    - caches homogeneous conversion per fold to reduce repeated overhead
    - accepts projected features for all node types
    """

    def __init__(self, hidden_dim, out_dim, num_heads, num_layers, canonical_etypes, node_types, dropout=0.2):
        super().__init__()

        if hidden_dim % num_heads != 0:
            raise ValueError(f'hidden_dim ({hidden_dim}) must be divisible by num_heads ({num_heads})')
        if out_dim % num_heads != 0:
            raise ValueError(f'out_dim ({out_dim}) must be divisible by num_heads ({num_heads})')

        self.node_types = list(node_types)
        self.layers = nn.ModuleList()
        hidden_head_dim = hidden_dim // num_heads
        out_head_dim = out_dim // num_heads
        num_ntypes = len(self.node_types)
        num_etypes = len(canonical_etypes)

        if num_layers <= 1:
            self.layers.append(
                dgl.nn.pytorch.conv.HGTConv(hidden_dim, out_head_dim, num_heads, num_ntypes, num_etypes, dropout)
            )
        else:
            for _ in range(num_layers - 1):
                self.layers.append(
                    dgl.nn.pytorch.conv.HGTConv(hidden_dim, hidden_head_dim, num_heads, num_ntypes, num_etypes, dropout)
                )
            self.layers.append(
                dgl.nn.pytorch.conv.HGTConv(hidden_dim, out_head_dim, num_heads, num_ntypes, num_etypes, dropout)
            )

        self._cache_key = None
        self._homo_graph = None
        self._node_slices = {}
        self._node_order = []

    def _refresh_cache(self, g):
        self._homo_graph = dgl.to_homogeneous(g)
        self._node_order = list(g.ntypes)
        self._node_slices = {}

        start = 0
        for ntype in self._node_order:
            stop = start + g.num_nodes(ntype)
            self._node_slices[ntype] = slice(start, stop)
            start = stop

        self._cache_key = id(g)

    def _get_cached_homogeneous_graph(self, g):
        if self._cache_key != id(g):
            self._refresh_cache(g)
        return self._homo_graph

    def forward(self, g, feature_dict):
        homo_graph = self._get_cached_homogeneous_graph(g)
        features = torch.cat([feature_dict[ntype] for ntype in self._node_order], dim=0)

        if homo_graph.device != features.device:
            homo_graph = homo_graph.to(features.device)
            self._homo_graph = homo_graph

        with homo_graph.local_scope():
            hidden = features
            node_type_ids = homo_graph.ndata['_TYPE']
            edge_type_ids = homo_graph.edata['_TYPE']
            for layer in self.layers:
                hidden = layer(homo_graph, hidden, node_type_ids, edge_type_ids, presorted=True)

        return {ntype: hidden[node_slice] for ntype, node_slice in self._node_slices.items()}
