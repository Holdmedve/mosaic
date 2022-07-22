import itertools
import cv2
import math
import numpy as np


def get_even_samples(to_sample: int, n: int) -> tuple[int, ...]:
    return tuple(map(lambda x: int(x), np.linspace(0, to_sample, n)))


def sqrti(a: int) -> int:
    return int(math.sqrt(a))


def get_num_total_frames(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    return int(capture.get(cv2.CAP_PROP_FRAME_COUNT))


def flatten_nested_list(nested_list: list[list]) -> list:
    return list(itertools.chain.from_iterable(nested_list))


def reshape_flat_list_to_nested(elements: list, num_rows: int) -> list[list]:
    num_elements = len(elements)
    # should only handle lists with square number of elements
    assert math.isqrt(num_elements) == math.sqrt(num_elements)

    return list(zip(*[iter(elements)] * num_rows))  # type: ignore


def get_random_non_negative_integers(
    range_max: int, num_integers: int, duplicates_allowed: bool
) -> tuple[int]:
    return tuple(np.random.choice(range_max, num_integers, replace=duplicates_allowed))  # type: ignore
