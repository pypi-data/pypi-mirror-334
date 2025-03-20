from typing import List, NamedTuple, Tuple

import torch

from .split import Layer
from .merge import MergingContext, merge_layers, merge_init, merge_next_layer


def decode_layers(layers: List[Layer]) -> torch.Tensor:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: [N, C] float tensor
    '''
    codes, context = merge_layers(layers)
    return context.cluster_centers[context.reversed_codebook[codes], ...]


class DecodingContext(NamedTuple):
    codes: torch.Tensor
    merging: MergingContext


def decode_layer(layer: Layer, context: DecodingContext = None) -> Tuple[torch.Tensor, DecodingContext]:
    '''
    Decode the layers.
    :param: layers: [layer0, layer1, ...] splitted layers
    :return: the decode result and the new context
    '''
    if context is None:
        codes, merging = merge_init(layer)
    else:
        codes, merging = merge_next_layer(layer, context.codes, context.merging)
    return merging.cluster_centers[merging.reversed_codebook[codes], ...], DecodingContext(codes, merging)
