import numpy as np

from numpy import ndarray


def mean_color_euclidian_distance(img_a: ndarray, img_b: ndarray) -> float:
    mean_a = img_a.mean(axis=(0, 1))
    mean_b = img_b.mean(axis=(0, 1))

    dst = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))

    return dst
