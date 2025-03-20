from typing import List, Tuple, NamedTuple

import torch

from .split import Layer


class MergingContext(NamedTuple):
    codebook: torch.Tensor  # [K,] int tensor
    cluster_centers: torch.Tensor  # [K, C] float tensor, with the same order as codebook
    n_leaf: int  # the number of leaf codes for this layer, codebook[:n_leaf] are leaf codes

    reversed_codebook: torch.Tensor


def construct_context(codebook: torch.Tensor, cluster_centers: torch.Tensor, n_leaf: int) -> MergingContext:
    reversed_codebook = torch.zeros(codebook.max() + 1, dtype=codebook.dtype, device=codebook.device) + len(codebook)
    reversed_codebook[codebook] = torch.arange(len(codebook), dtype=codebook.dtype, device=codebook.device)
    return MergingContext(codebook, cluster_centers, n_leaf, reversed_codebook)


def init_codebook(layer: Layer) -> MergingContext:
    return construct_context(layer.codebook, layer.cluster_centers, layer.n_leaf)


def append_codebook(layer: Layer, context: MergingContext) -> MergingContext:
    codebook = torch.cat([context.codebook[:context.n_leaf], layer.codebook])
    cluster_centers = torch.cat([context.cluster_centers[:context.n_leaf], layer.cluster_centers])
    n_leaf = context.n_leaf + layer.n_leaf
    return construct_context(codebook, cluster_centers, n_leaf)


def merge_init(layer: Layer) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Init the merging by the lowest layer.
    :param layer: the lowest layer.
    :return: the codes and the context.
    '''
    codes = layer.codes + (1 << layer.n_bit)
    context = init_codebook(layer)
    return codes, context


def merge_next_layer(layer: Layer, codes: torch.Tensor, context: MergingContext) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Merging the next layer.
    :param layer: the next layer.
    :param codes: the current codes.
    :param context: the current context.
    :return: the new codes and the new context.
    '''
    is_leaf = context.reversed_codebook[codes] < context.n_leaf
    codes[~is_leaf] = (codes[~is_leaf] << layer.n_bit) + layer.codes
    context = append_codebook(layer, context)
    return codes, context


def merge_layers(layers: List[Layer]) -> Tuple[torch.Tensor, MergingContext]:
    '''
    Merge multiple layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the codes and the context.
    '''
    codes, context = merge_init(layers[0])
    for layer in layers[1:]:
        codes, context = merge_next_layer(layer, codes, context)
    return codes, context
