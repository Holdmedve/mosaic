import pytest

import numpy as np

from project.image import split_image_into_tiles, stitch_grid_of_images_together
from tests.utils import (
    BLACK_PIXEL,
    TEST_IMAGE_PATH,
    WHITE_PIXEL,
    black_img,
    white_img,
)


def test__stitch_tiles__when_called_with_4_pixels_as_tiles__returns_them_as_1_array() -> None:
    tiles = [
        [black_img(), white_img()],
        [white_img(), black_img()],
    ]
    expected_image = np.array([[BLACK_PIXEL, WHITE_PIXEL], [WHITE_PIXEL, BLACK_PIXEL]])

    image = stitch_grid_of_images_together(tiles)

    assert (image == expected_image).all()


@pytest.mark.parametrize(
    "tile_count, expected_tile_dimensions", [(4, (2, 2)), (9, (3, 3))]
)
def test__split_image_into_tiles__when_called_with_certain_tile_count__returns_tiles_in_excpected_dimensions(
    tile_count: int, expected_tile_dimensions: tuple[int, ...]
) -> None:
    tiles = split_image_into_tiles(image_path=TEST_IMAGE_PATH, tile_count=tile_count)

    assert len(tiles) == expected_tile_dimensions[0]
    assert len(tiles[0]) == expected_tile_dimensions[1]
    assert len({len(row) for row in tiles}) == 1
