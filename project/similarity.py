import numpy as np
from numpy.typing import NDArray
from project.types import Image


def mean_color_similarity(img_a: Image, img_b: Image) -> float:
    mean_a = img_a.mean(axis=(0, 1))
    mean_b = img_b.mean(axis=(0, 1))

    max_possible_distance = 255 * np.sqrt(3)
    distance: float = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))
    raw_similarity = 1 - distance / max_possible_distance

    return max(min(raw_similarity, 1.0), 0)


def mean_color_similarities(
    images: NDArray, image_to_compare: NDArray
) -> tuple[float, ...]:
    mean_color_of_images = images.mean(axis=1).mean(axis=1)
    mean_to_compare = image_to_compare.mean(axis=(0, 1))

    distances = [
        np.sqrt(((mean - mean_to_compare) ** 2).sum(axis=0))
        for mean in mean_color_of_images
    ]
    return tuple([-distance for distance in distances])
