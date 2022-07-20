import cv2
import numpy as np
from numpy.typing import NDArray


def get_frames_at_indeces(
    video_path: str, indeces: tuple[int, ...]
) -> list[NDArray[np.uint8]]:
    capture = cv2.VideoCapture(video_path)
    frames: list[NDArray[np.uint8]] = []

    for idx in indeces:
        capture.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, frame = capture.read()
        if not success:
            continue

        desired_width, desired_height = _get_desired_dimensions_keep_ratio(
            original_height=frame.shape[0],
            original_width=frame.shape[1],
            desired_height=100,
        )
        resized_frame = cv2.resize(src=frame, dsize=(desired_width, desired_height))
        frames.append(resized_frame)

    capture.release()

    return frames


def _get_desired_dimensions_keep_ratio(
    original_height: int, original_width: int, desired_height: int
) -> tuple[int, int]:
    dimension_multiplier = desired_height / original_height
    desired_width = int(original_width * dimension_multiplier)
    return desired_width, desired_height
