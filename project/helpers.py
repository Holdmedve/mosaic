import cv2
import math
import numpy as np


def get_even_samples(to_sample: int, n: int) -> tuple[int, ...]:
    return tuple(map(lambda x: int(x), np.linspace(0, to_sample, n)))


def _sqrti(a: int) -> int:
    return int(math.sqrt(a))


def _get_total_num_frames(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    return capture.get(cv2.CAP_PROP_FRAME_COUNT)  # type: ignore
