import math
import os
import cv2


import numpy as np

from project.exceptions import InvalidSplitLevel
from project.mosaic_data import MosaicData
from project.types import Image


def get_even_samples(to_sample: int, n: int) -> tuple[int, ...]:
    return tuple(map(lambda x: int(x), np.linspace(0, to_sample, n)))


def split_image_into_tiles(data: MosaicData) -> list[list[Image]]:
    img = cv2.imread(data.target_image_path)
    tile_count_along_1_dimension_plus_1 = int(math.sqrt(data.requested_tile_count)) + 1
    x_tile_borders = get_even_samples(img.shape[0], tile_count_along_1_dimension_plus_1)
    y_tile_borders = get_even_samples(img.shape[1], tile_count_along_1_dimension_plus_1)

    tiles: list[list[Image]] = []

    for x in range(len(y_tile_borders) - 1):
        row = []
        for y in range(len(x_tile_borders) - 1):
            s = (
                slice(x_tile_borders[x], x_tile_borders[x + 1]),
                slice(y_tile_borders[y], y_tile_borders[y + 1]),
            )
            tile = img[s]
            row.append(tile)
        tiles.append(row)

    return tiles


def get_n_frames_from_kth_frame(vid_path: str, n: int, k: int) -> list[Image]:
    capture = cv2.VideoCapture(vid_path)
    capture.set(cv2.CAP_PROP_POS_FRAMES, k)
    frames: list[Image] = []

    while True:
        success, frame = capture.read()
        if len(frames) < n and success:
            desired_width, desired_height = _get_desired_dimensions_keep_ratio(
                original_height=frame.shape[0],
                original_width=frame.shape[1],
                desired_height=100,
            )
            frame = cv2.resize(src=frame, dsize=(desired_width, desired_height))
            frames.append(frame)
        else:
            break

    capture.release()

    return frames


def _get_desired_dimensions_keep_ratio(
    original_height: int, original_width: int, desired_height: int
) -> tuple[int, int]:
    dimension_multiplier = desired_height / original_height
    desired_width = int(original_width * dimension_multiplier)
    return desired_width, desired_height


def is_data_valid(data: MosaicData) -> bool:
    if data.requested_tile_count < 1:
        raise InvalidSplitLevel("split level must be at least 1")

    if not os.path.exists(data.source_video_path):
        raise FileNotFoundError

    if not os.path.exists(data.target_image_path):
        raise FileNotFoundError

    return True
