import numpy as np

from typing import Callable
from project.distance import mean_color_euclidian_distance
from project.types import Image


from project.helpers import (
    get_frames_from_video,
    is_data_valid,
    split_image_into_tiles,
)
from project.mosaic_data import MosaicData


def stitch_images_together(images: list[list[Image]]) -> Image:
    result: Image

    for x in range(len(images)):
        row: Image
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
    frames: list[Image],
    tile: Image,
    comparison_fn: Callable[[Image, Image], float],
) -> Image:
    best_fit: Image = frames[0]
    best_dst: float = float("inf")

    for f in frames:
        dst = comparison_fn(f, tile)
        if dst < best_dst:
            best_fit = f
            best_dst = dst

    return best_fit


def get_best_fitting_frames(
    target_tiles: list[list[Image]],
    frames: list[Image],
    comparison_fn: Callable[[Image, Image], float],
) -> list[list[Image]]:
    best_fitting_frames: list[list[Image]]

    for x in range(len(target_tiles)):
        row: list[Image]
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


def create_mosaic_from_video(data: MosaicData) -> Image:

    if not is_data_valid(data):
        return np.array([])

    target_tiles: list[list[Image]] = split_image_into_tiles(data)
    frames: list[Image] = get_frames_from_video(data.source_video_path)

    best_fitting_frames: list[list[Image]] = get_best_fitting_frames(
        target_tiles=target_tiles,
        frames=frames,
        comparison_fn=mean_color_euclidian_distance,
    )

    result: Image = stitch_images_together(best_fitting_frames)

    return result
