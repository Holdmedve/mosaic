import cv2  # type: ignore
import os

import numpy as np

from dataclasses import dataclass
from numpy import ndarray
from typing import Callable, List, Tuple


class InvalidSplitLevel(Exception):
    pass


@dataclass
class Config:
    split_level: int
    comparison_method: Callable[[ndarray, ndarray], float]


@dataclass
class Data:
    target_image: str
    source_video: str


def mean_color_euclidian_distance(img_a: ndarray, img_b: ndarray) -> float:
    mean_a = np.mean(img_a, axis=(0, 1))
    mean_b = np.mean(img_b, axis=(0, 1))

    dst = np.sqrt(((mean_a - mean_b) ** 2).sum(axis=0))

    return dst


def get_frames_from_video(vid_path: str) -> List[ndarray]:
    if not os.path.exists(vid_path):
        raise FileNotFoundError

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


def get_even_samples(to_sample: int, n: int) -> tuple[int, ...]:
    return tuple(map(lambda x: int(x), np.linspace(0, to_sample, n)))


def split_image_into_tiles(img_path: str, split_level: int) -> list[list[ndarray]]:
    if split_level < 1:
        raise InvalidSplitLevel("split level must be at least 1")

    if not os.path.exists(img_path):
        raise FileNotFoundError

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


def stitch(images: list[list[ndarray]]) -> ndarray:
    result: ndarray

    for x in range(len(images)):
        row: ndarray
        for y in range(len(images[0])):
            if y == 0:
                row = images[x][y]
            else:
                row = np.concatenate((row, images[x][y]), axis=1)
        if x == 0:
            result = row
        else:
            result = np.concatenate((result, row), axis=0)

    return result


def find_best_fitting_frame(
    frames: list[ndarray],
    tile: ndarray,
    comparison_fn: Callable[[ndarray, ndarray], float],
) -> ndarray:
    best_fit: ndarray = frames[0]
    best_dst: float = float("inf")

    for f in frames:
        dst = comparison_fn(f, tile)
        if dst < best_dst:
            best_fit = f
            best_dst = dst

    return best_fit


def get_best_fitting_frames(
    target_tiles: list[list[ndarray]],
    frames,
    comparison_fn: Callable[[ndarray, ndarray], float],
) -> list[list[ndarray]]:
    best_fitting_frames: list[list[ndarray]]

    for x in range(len(target_tiles)):
        row: list[ndarray]
        for y in range(len(target_tiles[0])):
            f = find_best_fitting_frame(frames, target_tiles[x][y], comparison_fn)
            if y == 0:
                row = [f]
            else:
                row.append(f)
        if x == 0:
            best_fitting_frames = [row]
        else:
            best_fitting_frames.append(row)

    return best_fitting_frames


def create_mosaic_from_video(target_img_path: str, source_video_path: str) -> ndarray:
    target_tiles: list[list[ndarray]] = split_image_into_tiles(target_img_path, 2)
    frames: list[ndarray] = get_frames_from_video(source_video_path)

    best_fitting_frames: list[list[ndarray]] = get_best_fitting_frames(
        target_tiles, frames, mean_color_euclidian_distance
    )

    result: ndarray = stitch(best_fitting_frames)

    return result
