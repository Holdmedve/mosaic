import os
from dataclasses import dataclass
import cv2  # type: ignore

from typing import List
from numpy import ndarray


import numpy as np

from project.exceptions import InvalidSplitLevel


@dataclass
class Data:
    requested_split_level: int
    target_image_path: str
    source_video_path: str


def get_even_samples(to_sample: int, n: int) -> tuple[int, ...]:
    return tuple(map(lambda x: int(x), np.linspace(0, to_sample, n)))


def split_image_into_tiles(img_path: str, split_level: int) -> list[list[ndarray]]:

    img = cv2.imread(img_path)

    x_tile_borders = get_even_samples(img.shape[0], 2**split_level + 1)
    y_tile_borders = get_even_samples(img.shape[1], 2**split_level + 1)

    tiles: list[list[ndarray]] = []

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


def get_frames_from_video(vid_path: str) -> List[ndarray]:

    capture = cv2.VideoCapture(vid_path)
    frames = []

    while True:
        success, frame = capture.read()
        if success:
            frames.append(frame)
        else:
            break

    capture.release()

    return frames


def is_data_valid(data: Data) -> bool:
    if data.requested_split_level < 1:
        raise InvalidSplitLevel("split level must be at least 1")

    if not os.path.exists(data.source_video_path):
        raise FileNotFoundError

    if not os.path.exists(data.target_image_path):
        raise FileNotFoundError

    return True
