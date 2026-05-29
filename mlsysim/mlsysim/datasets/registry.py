from ..core.units import count
from ..core.constants import IMAGE_CHANNELS_RGB
from ..core.registry import Registry
from .types import DatasetProfile

_IMAGENET_IMAGE_DIM = 224  # ImageNet-1k native training resolution (224x224)
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
        image_width=_IMAGENET_IMAGE_DIM,
        image_height=_IMAGENET_IMAGE_DIM,
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
