import cv2

from tests.utils import *

from project.mosavid import (
    stitch,
    split_image_into_tiles,
    find_best_fitting_frame,
    mean_color_euclidian_distance,
    create_mosaic_from_video,
    get_best_fitting_frames,
)


def test__split_into_tiles_and_stitcing_back_together__results_in_original_image():
    original_image = cv2.imread(TEST_JPG_PATH)

    tiles = split_image_into_tiles(TEST_JPG_PATH, 2)
    stitched_image = stitch(tiles)

    assert (original_image == stitched_image).all()


def test_create_mosaic__when_called__executes_without_errors():
    create_mosaic_from_video(TEST_JPG_PATH, TEST_MP4_PATH)


def test_get_best_fitting_frames__executes_without_errors():
    tiles = [[BLACK_IMG, BLACK_IMG], [WHITE_IMG, WHITE_IMG]]
    frames = [BLACK_IMG, WHITE_IMG, BLACK_IMG, WHITE_IMG]
    get_best_fitting_frames(tiles, frames, mean_color_euclidian_distance)


class TestFindBestFittingFrame:
    def test__when_called__returns_frame_most_similar_to_tile(self):
        tile = black_img()
        frames = [white_img(), black_img(), white_img()]

        best_fit = find_best_fitting_frame(
            tile=tile, frames=frames, comparison_fn=mean_color_euclidian_distance
        )

        assert (best_fit == black_img()).all()

    def test__when_called_with_equally_similar_frames__returns_first_one(self):
        tile = black_img()
        frames = [green_img(), blue_img(), red_img()]

        best_fit = find_best_fitting_frame(
            tile=tile, frames=frames, comparison_fn=mean_color_euclidian_distance
        )

        assert (best_fit == frames[0]).all()
