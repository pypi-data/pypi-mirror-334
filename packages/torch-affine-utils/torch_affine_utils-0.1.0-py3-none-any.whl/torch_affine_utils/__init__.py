"""Utilities for affine transformations of 2d/3d coordinates in PyTorch"""

__version__ = '0.1.0'
__author__ = "Alister Burt"
__email__ = "alisterburt@gmail.com"

from torch_affine_utils.utils import homogenise_coordinates

__all__ = [
    "homogenise_coordinates",
]