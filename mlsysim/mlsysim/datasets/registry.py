import sys as _sys

# Read core submodules from sys.modules to avoid parent-package re-entry
# on Python <=3.12. These modules are guaranteed to be loaded because
# mlsysim.__init__ imports core (and all its submodules) before datasets.
_units = _sys.modules.get("mlsysim.core.units")
_consts = _sys.modules.get("mlsysim.core.constants")
_reg = _sys.modules.get("mlsysim.core.registry")

if _units is not None and _consts is not None and _reg is not None:
    count = _units.count
    IMAGE_CHANNELS_RGB = _consts.IMAGE_CHANNELS_RGB
    IMAGE_DIM_RESNET = _consts.IMAGE_DIM_RESNET
    Registry = _reg.Registry
else:
    from ..core.units import count
    from ..core.constants import IMAGE_CHANNELS_RGB, IMAGE_DIM_RESNET
    from ..core.registry import Registry

del _sys, _units, _consts, _reg
from .types import DatasetProfile

_IMAGENET_TRAINING = 1_281_167 * count
_IMAGENET_TEST = 50_000 * count
_IMAGENET_CLASSES = 1000
_CIFAR10_TRAINING = 50_000 * count
_MNIST_TRAINING = 60_000 * count


class Datasets(Registry):
    """Registry namespace for Datasets."""
    ImageNet = DatasetProfile(
        name="ImageNet-1k",
        training_examples=_IMAGENET_TRAINING,
        test_examples=_IMAGENET_TEST,
        num_classes=_IMAGENET_CLASSES,
        image_width=IMAGE_DIM_RESNET,
        image_height=IMAGE_DIM_RESNET,
        image_channels=IMAGE_CHANNELS_RGB,
    )
    CIFAR10 = DatasetProfile(
        name="CIFAR-10",
        training_examples=_CIFAR10_TRAINING,
        test_examples=10_000 * count,
        num_classes=10,
        image_width=32,
        image_height=32,
        image_channels=IMAGE_CHANNELS_RGB,
    )
    MNIST = DatasetProfile(
        name="MNIST",
        training_examples=_MNIST_TRAINING,
        test_examples=10_000 * count,
        num_classes=10,
        image_width=28,
        image_height=28,
        image_channels=1,
    )
