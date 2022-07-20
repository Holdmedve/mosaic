import numpy as np

from project.types import Image, Image


def mean_color_euclidian_distance(img_a: Image, img_b: Image) -> float:
    mean_a = img_a.mean(axis=(0, 1))
    mean_b = img_b.mean(axis=(0, 1))

    dst: float = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))

    return dst
