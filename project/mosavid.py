import cv2
import math
import numpy as np
from numpy.typing import NDArray

from project.helpers import (
    flatten_nested_list,
    get_num_total_frames,
    get_random_non_negative_integers,
    reshape_flat_list_to_nested,
)
from project.image import (
    split_image_into_tiles,
    stitch_grid_of_images_together,
)
from project.similarity import mean_color_similarities
from project.types import Config, TILE_COUNT_TO_HEIGHT_DICT
from project.video import get_resized_frames_at_indeces


def generate_mosaic(config: Config) -> NDArray[np.uint8]:
    original_tiles = split_image_into_tiles(
        image_path=config.original_image_path, tile_count=config.mosaic_tile_count
    )
    best_matches_list = get_best_matches_for_tiles(
        video_path=config.video_path,
        tiles=flatten_nested_list(original_tiles),
        max_frames_to_match=config.max_frames_to_match,
    )
    best_matches_grid = reshape_flat_list_to_nested(
        elements=best_matches_list, num_rows=math.isqrt(config.mosaic_tile_count)
    )

    return stitch_grid_of_images_together(images=best_matches_grid)


def get_best_matches_for_tiles(
    video_path: str, tiles: list[NDArray[np.uint8]], max_frames_to_match: int
) -> list[NDArray[np.uint8]]:
    num_total_frames = get_num_total_frames(video_path=video_path)

    num_frames_to_match = min(num_total_frames, max_frames_to_match)
    frame_indeces = get_random_non_negative_integers(
        range_max=num_total_frames,
        num_integers=num_frames_to_match,
        duplicates_allowed=False,
    )

    return get_best_matching_frames(frame_indeces, tiles, video_path)


def get_best_matching_frames(
    frame_indeces: tuple[int, ...], tiles: list[NDArray[np.uint8]], video_path: str
) -> list[NDArray[np.uint8]]:
    best_matching_frames = []
    height = TILE_COUNT_TO_HEIGHT_DICT[len(tiles)]
    frames = get_resized_frames_at_indeces(
        video_path=video_path,
        indeces=frame_indeces,
        resized_height=height,
        resized_width=int(height / tiles[0].shape[0] * tiles[0].shape[1]),
    )
    tile_sized_frames = [
        cv2.resize(src=frame, dsize=(tiles[0].shape[0], tiles[0].shape[1]))
        for frame in frames
    ]

    for tile in tiles:
        best_matching_frame = frames[
            get_best_matching_frame_idx_for_tile(frames=tile_sized_frames, tile=tile)
        ]
        best_matching_frames.append(best_matching_frame)

    return best_matching_frames


def get_best_matching_frame_idx_for_tile(
    frames: list[NDArray[np.uint8]], tile: NDArray[np.uint8]
) -> int:
    frames_nparray = np.array(frames)
    similarities = mean_color_similarities(images=frames_nparray, image_to_compare=tile)
    best_similarity = max(similarities)
    return similarities.index(best_similarity)
