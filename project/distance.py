import numpy as np

from numpy.typing import NDArray
from numpy import ndarray


def mean_color_euclidian_distance(
    img_a: NDArray[np.int32], img_b: NDArray[np.int32]
) -> float:
    mean_a = img_a.mean(axis=(0, 1))
    mean_b = img_b.mean(axis=(0, 1))

    dst: float = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))

    return dst
