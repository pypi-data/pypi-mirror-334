from typing import List

import torch

from .build import build_layers
from .assign import assign_bits
from .utils import bitcount
from .split import Layer, split_layers


def format_n_bits(n_bits_proposal: List[int], max_n_bits) -> str:
    n_bits = []
    while n_bits_proposal and max_n_bits > 0:
        n_bit = min(n_bits_proposal[0], max_n_bits)
        n_bits_proposal = n_bits_proposal[1:]
        n_bits.append(n_bit)
        max_n_bits -= n_bit
    if max_n_bits > 0:
        n_bits.append(max_n_bits)
    return n_bits


def encode_layers(data: torch.Tensor, quantized_data: torch.Tensor, cluster_centers: torch.Tensor, n_bits_proposal: List[int] = [4, 4, 4]) -> List[Layer]:
    '''
    Encode the layers.
    :param: data: [N, C] float tensor, the origional data
    :param: quantized_data: [N] long tensor, the quantized data
    :param: cluster_centers: [K, C] float tensor, the cluster centers
    :param: n_bits_proposal: list of int, bit width proposal for each layer
    :return: [layer0, layer1, ...] splitted layers
    '''
    n_clusters = cluster_centers.shape[0]
    lod0_bitwidth = n_bits_proposal[0]
    assert 2**lod0_bitwidth < n_clusters

    layerized_cluster_centers, cluster_tree = build_layers(cluster_centers, data, quantized_data, final_clusters=2**lod0_bitwidth)
    assigned_bits = assign_bits(cluster_tree, n_clusters=layerized_cluster_centers.shape[0])
    assigned_bits = torch.tensor(assigned_bits, device=quantized_data.device)
    assigned_bits_data = assigned_bits[quantized_data]

    max_n_bits = bitcount(assigned_bits.max().item()) - 1
    n_bits = format_n_bits(n_bits_proposal, max_n_bits)

    leaf_idx = torch.arange(0, n_clusters, dtype=assigned_bits.dtype, device=assigned_bits_data.device)
    layers = split_layers(assigned_bits_data, assigned_bits, leaf_idx, layerized_cluster_centers, n_bits=n_bits)
    return layers
