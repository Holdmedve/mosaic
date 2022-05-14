import cv2
from project.helpers import MosaicData

from tests.utils import *

from project.mosavid import (
    stitch_images_together,
    split_image_into_tiles,
    find_best_fitting_frame,
    mean_color_euclidian_distance,
    create_mosaic_from_video,
    get_best_fitting_frames,
)


def test__split_into_tiles_and_stitcing_back_together__results_in_original_image():
    data = MosaicData(
        target_image_path=TEST_JPG_PATH,
        source_video_path=TEST_MP4_PATH,
        requested_tile_count=2,
    )
    original_image = cv2.imread(TEST_JPG_PATH)

    tiles = split_image_into_tiles(data=data)
    stitched_image = stitch_images_together(tiles)

    assert (original_image == stitched_image).all()


def test_create_mosaic__when_called__executes_without_errors():
    create_mosaic_from_video(TEST_JPG_PATH, TEST_MP4_PATH)


def test_get_best_fitting_frames__executes_without_errors():
    tiles = [[BLACK_IMG, BLACK_IMG], [WHITE_IMG, WHITE_IMG]]
    frames = [BLACK_IMG, WHITE_IMG, BLACK_IMG, WHITE_IMG]
    get_best_fitting_frames(tiles, frames, mean_color_euclidian_distance)


def test__find_best_fitting_frame__returns_frame_most_similar_to_tile():
    tile = black_img()
    frames = [white_img(), black_img(), white_img()]

    best_fit = find_best_fitting_frame(
        tile=tile, frames=frames, comparison_fn=mean_color_euclidian_distance
    )

    assert (best_fit == black_img()).all()


def test__find_best_fitting_frame__when_called_with_equally_similar_frames__returns_first_one():
    tile = black_img()
    frames = [green_img(), blue_img(), red_img()]

    best_fit = find_best_fitting_frame(
        tile=tile, frames=frames, comparison_fn=mean_color_euclidian_distance
    )

    assert (best_fit == frames[0]).all()
