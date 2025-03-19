import torch

from torch_affine_utils.transforms_2d import R, T, S


def test_rotation():
    """Rotating x-axis by 90 degrees should become y-axis."""
    # Standard coordinate system (xyw)
    rotation = R(90)
    v = torch.tensor([1, 0, 1]).view((3, 1)).float()
    expected = torch.tensor([0, 1, 1]).view((3, 1)).float()
    assert torch.allclose(rotation @ v, expected, atol=1e-6)

    # Test with yx coordinate system
    rotation = R(90, yx=True)
    v = torch.tensor([0, 1, 1]).view((3, 1)).float()
    expected = torch.tensor([1, 0, 1]).view((3, 1)).float()
    assert torch.allclose(rotation @ v, expected, atol=1e-6)


def test_translation():
    """Translation should add the offset to the position."""
    translation = T([2, 3])
    v = torch.tensor([1, 1, 1]).view((3, 1)).float()
    expected = torch.tensor([3, 4, 1]).view((3, 1)).float()
    assert torch.allclose(translation @ v, expected, atol=1e-6)


def test_scaling():
    """Scaling should multiply each coordinate by the scale factor."""
    scaling = S([2, 3])
    v = torch.tensor([1, 1, 1]).view((3, 1)).float()
    expected = torch.tensor([2, 3, 1]).view((3, 1)).float()
    assert torch.allclose(scaling @ v, expected, atol=1e-6)
