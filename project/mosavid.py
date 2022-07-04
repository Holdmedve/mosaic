import math
import numpy as np
import cv2

from typing import Callable
from project.distance import mean_color_euclidian_distance
from project.types import Image


from project.helpers import (
    get_n_frames_from_kth_frame,
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
) -> tuple[Image, float]:
    best_fit: Image = frames[0]
    best_dst: float = float("inf")

    for f in frames:
        dst = comparison_fn(f, tile)
        if dst < best_dst:
            best_fit = f
            best_dst = dst

    return best_fit, best_dst


def get_best_fitting_frames(
    target_tiles: list[list[Image]],
    frames: list[Image],
    comparison_fn: Callable[[Image, Image], float],
) -> tuple[list[list[Image]], list[float]]:
    best_fitting_frames: list[list[Image]]
    best_distances: list[float]

    for x in range(len(target_tiles)):
        row_of_frames: list[Image]
        distances: list[float]
        for y in range(len(target_tiles[0])):
            frame, distance = find_best_fitting_frame(
                frames, target_tiles[x][y], comparison_fn
            )
            if y == 0:
                row_of_frames = [frame]
                distances = [distance]
            else:
                row_of_frames.append(frame)
                distances.append(distance)
        if x == 0:
            best_fitting_frames = [row_of_frames]
            best_distances = distances
        else:
            best_fitting_frames.append(row_of_frames)
            best_distances.extend(distances)

    return best_fitting_frames, best_distances


def create_mosaic_from_video(data: MosaicData) -> Image:
    if not is_data_valid(data):
        return np.array([])

    target_tiles: list[list[Image]] = split_image_into_tiles(data)

    mosaic_pieces: list[list[Image]] = list(list([]))
    total_num_frames: int = _get_total_num_frames(data.source_video_path)
    num_frames_processed: int = 0
    num_frames_to_process_per_iteration = 500
    best_tile_distances = [float("inf")] * data.requested_tile_count

    while num_frames_processed < total_num_frames:
        frames: list[Image] = get_n_frames_from_kth_frame(
            data.source_video_path,
            n=num_frames_to_process_per_iteration,
            k=num_frames_processed,
        )

        best_fitting_frames, frame_tile_distances = get_best_fitting_frames(
            target_tiles=target_tiles,
            frames=frames,
            comparison_fn=mean_color_euclidian_distance,
        )

        if num_frames_processed == 0:
            mosaic_pieces = best_fitting_frames
            num_frames_processed += num_frames_to_process_per_iteration
            continue

        num_frames_processed += num_frames_to_process_per_iteration

        for idx, best_dist in enumerate(best_tile_distances):
            if frame_tile_distances[idx] < best_dist:
                best_tile_distances[idx] = frame_tile_distances[idx]
                a = int(math.sqrt(data.requested_tile_count))
                row = idx // a if idx != 0 else 0
                col = idx % a if idx != 0 else 0
                mosaic_pieces[row][col] = best_fitting_frames[row][col]

    result: Image = stitch_images_together(mosaic_pieces)

    return result


def _get_total_num_frames(video_path: str) -> int:
    capture = cv2.VideoCapture(video_path)
    return capture.get(cv2.CAP_PROP_FRAME_COUNT)  # type: ignore
