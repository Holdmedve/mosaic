import cv2
import numpy as np
from numpy.typing import NDArray


def get_resized_frames_at_indeces(
    video_path: str, indeces: tuple[int, ...], resized_height: int, resized_width: int
) -> list[NDArray[np.uint8]]:
    capture = cv2.VideoCapture(video_path)
    frames: list[NDArray[np.uint8]] = []

    for idx in indeces:
        capture.set(cv2.CAP_PROP_POS_FRAMES, idx)
        success, frame = capture.read()
        if not success:
            continue

        resized_frame = cv2.resize(src=frame, dsize=(resized_width, resized_height))
        frames.append(resized_frame)

    capture.release()

    return frames
