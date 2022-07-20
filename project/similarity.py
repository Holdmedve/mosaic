import numpy as np
from project.types import Image


def mean_color_similarity(img_a: Image, img_b: Image) -> float:
    mean_a = img_a.mean(axis=(0, 1))
    mean_b = img_b.mean(axis=(0, 1))

    max_possible_distance = 255 * np.sqrt(3)
    distance: float = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))
    raw_similarity = 1 - distance / max_possible_distance

    return max(min(raw_similarity, 1.0), 0)
