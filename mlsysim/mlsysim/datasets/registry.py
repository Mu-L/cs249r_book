from ..core.constants import (
    CIFAR10_IMAGES,
    IMAGENET_IMAGES,
    IMAGENET_NUM_CLASSES,
    IMAGENET_TEST_IMAGES,
    IMAGE_CHANNELS_RGB,
    IMAGE_DIM_RESNET,
    MNIST_IMAGE_HEIGHT,
    MNIST_IMAGE_WIDTH,
    MNIST_NUM_CLASSES,
    MNIST_TRAINING_EXAMPLES,
    count,
)
from ..core.registry import Registry
from .types import DatasetProfile


class Datasets(Registry):
    ImageNet = DatasetProfile(
        name="ImageNet-1k",
        training_examples=IMAGENET_IMAGES,
        test_examples=IMAGENET_TEST_IMAGES,
        num_classes=IMAGENET_NUM_CLASSES,
        image_width=IMAGE_DIM_RESNET,
        image_height=IMAGE_DIM_RESNET,
        image_channels=IMAGE_CHANNELS_RGB,
    )
    CIFAR10 = DatasetProfile(
        name="CIFAR-10",
        training_examples=CIFAR10_IMAGES,
        test_examples=10_000 * count,
        num_classes=10,
        image_width=32,
        image_height=32,
        image_channels=IMAGE_CHANNELS_RGB,
    )
    MNIST = DatasetProfile(
        name="MNIST",
        training_examples=MNIST_TRAINING_EXAMPLES,
        test_examples=10_000 * count,
        num_classes=MNIST_NUM_CLASSES,
        image_width=MNIST_IMAGE_WIDTH,
        image_height=MNIST_IMAGE_HEIGHT,
        image_channels=1,
    )
