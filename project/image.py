import math
import cv2
import numpy as np
from numpy.typing import NDArray

from project.helpers import get_even_samples


def split_image_into_tiles(
    image_path: str, tile_count: int
) -> list[list[NDArray[np.uint8]]]:
    img = cv2.imread(image_path)
    tile_count_along_1_dimension_plus_1 = int(math.sqrt(tile_count)) + 1
    x_tile_borders = get_even_samples(img.shape[0], tile_count_along_1_dimension_plus_1)
    y_tile_borders = get_even_samples(img.shape[1], tile_count_along_1_dimension_plus_1)

    tiles: list[list[NDArray[np.uint8]]] = []

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


def stitch_grid_of_images_together(
    images: list[list[NDArray[np.uint8]]],
) -> NDArray[np.uint8]:

    rows = [np.hstack(row_of_images) for row_of_images in images]
    return np.vstack(rows)
