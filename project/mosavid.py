import itertools
import math
import numpy as np
from numpy.typing import NDArray

import cv2
from project.image import split_image_into_tiles, stitch_grid_of_images_together
from project.similarity import mean_color_similarity
from project.types import Config
from project.video import get_frames_at_indeces


def generate_mosaic(config: Config) -> NDArray[np.uint8]:
    original_tiles = split_image_into_tiles(
        image_path=config.original_image_path, tile_count=config.mosaic_tile_count
    )
    best_matches_list = get_best_matches_for_tiles(
        video_path=config.video_path, tiles=flatten_nested_list(original_tiles)
    )
    best_matches_grid = reshape_list_to_square_grid(
        elements=best_matches_list, num_rows=math.isqrt(config.mosaic_tile_count)
    )

    return stitch_grid_of_images_together(images=best_matches_grid)


def get_best_matches_for_tiles(
    video_path: str, tiles: list[NDArray[np.uint8]]
) -> list[NDArray[np.uint8]]:
    num_total_frames = _get_num_total_frames(video_path=video_path)
    frame_indeces = get_random_frame_indeces(num_total_frames)
    return get_best_matching_frames(frame_indeces, tiles, video_path)


def get_best_matching_frames(
    frame_indeces: tuple[int, ...], tiles: list[NDArray[np.uint8]], video_path: str
) -> list[NDArray[np.uint8]]:
    # multiprocess / thread here?
    num_frames = len(frame_indeces)
    batch_size = 100
    best_matching_frames = []

    for i in range(0, min(num_frames, batch_size), num_frames):
        batch_of_frame_indeces = frame_indeces[i : i + batch_size]
        batch_of_frames = get_frames_at_indeces(
            video_path=video_path, indeces=batch_of_frame_indeces
        )
        for tile in tiles:
            best_matching_frames.append(
                get_best_matching_frame_for_tile(batch_of_frames, tile)
            )

    return best_matching_frames


def get_best_matching_frame_for_tile(
    frames: list[NDArray[np.uint8]], tile: NDArray[np.uint8]
) -> NDArray[np.uint8]:
    similarities = [mean_color_similarity(img_a=frame, img_b=tile) for frame in frames]
    best_similarity = max(similarities)
    return frames[similarities.index(best_similarity)]


def reshape_list_to_square_grid(
    elements: list[NDArray[np.uint8]], num_rows: int
) -> list[list[NDArray[np.uint8]]]:
    num_elements = len(elements)
    # should only handle lists with square number of elements
    assert math.isqrt(num_elements) == math.sqrt(num_elements)

    return list(zip(*[iter(elements)] * num_rows))  # type: ignore


def flatten_nested_list(nest_list: list[list]) -> list:
    return list(itertools.chain.from_iterable(nest_list))


def get_random_frame_indeces(num_total_frames: int) -> tuple[int]:
    num_choose = min(1000, num_total_frames)
    return tuple(np.random.choice(num_total_frames, num_choose, replace=False))  # type: ignore


def _get_num_total_frames(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    return int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
