import numpy as np

from numpy.typing import NDArray
from typing import Callable
from project.distance import mean_color_euclidian_distance

from project.helpers import (
    get_frames_from_video,
    is_data_valid,
    split_image_into_tiles,
)
from project.mosaic_data import MosaicData


def stitch_images_together(images: list[list[NDArray[np.int32]]]) -> NDArray[np.int32]:
    result: NDArray[np.int32]

    for x in range(len(images)):
        row: NDArray[np.int32]
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
    frames: list[NDArray[np.int32]],
    tile: NDArray[np.int32],
    comparison_fn: Callable[[NDArray[np.int32], NDArray[np.int32]], float],
) -> NDArray[np.int32]:
    best_fit: NDArray[np.int32] = frames[0]
    best_dst: float = float("inf")

    for f in frames:
        dst = comparison_fn(f, tile)
        if dst < best_dst:
            best_fit = f
            best_dst = dst

    return best_fit


def get_best_fitting_frames(
    target_tiles: list[list[NDArray[np.int32]]],
    frames: list[NDArray[np.int32]],
    comparison_fn: Callable[[NDArray[np.int32], NDArray[np.int32]], float],
) -> list[list[NDArray[np.int32]]]:
    best_fitting_frames: list[list[NDArray[np.int32]]]

    for x in range(len(target_tiles)):
        row: list[NDArray[np.int32]]
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


def create_mosaic_from_video(
    target_img_path: str, source_video_path: str
) -> NDArray[np.int32]:
    data = MosaicData(
        target_image_path=target_img_path,
        source_video_path=source_video_path,
        requested_tile_count=4,
    )
    if not is_data_valid(data):
        return np.array([])

    target_tiles: list[list[NDArray[np.int32]]] = split_image_into_tiles(data)
    frames: list[NDArray[np.int32]] = get_frames_from_video(data.source_video_path)

    best_fitting_frames: list[list[NDArray[np.int32]]] = get_best_fitting_frames(
        target_tiles, frames, mean_color_euclidian_distance
    )

    result: NDArray[np.int32] = stitch_images_together(best_fitting_frames)

    return result
