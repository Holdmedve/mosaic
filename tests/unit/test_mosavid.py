from project.helpers import get_random_non_negative_integers
from project.mosavid import (
    generate_mosaic,
    get_best_matching_frame_for_tile,
)

from project.types import Config
from tests.utils import *


def test__get_random_non_negative_integers__returns_unique_elements() -> None:
    indeces = get_random_non_negative_integers(
        range_max=10, num_integers=10, duplicates_allowed=False
    )

    assert len(indeces) == len(set(indeces))


def test__create_mosaic__given_a_config__returns_mosaic_with_roughly_same_ratio_as_original_image() -> None:
    original_image = cv2.imread(TEST_IMAGE_PATH)

    mosaic = generate_mosaic(
        config=Config(
            video_path=TEST_VIDEO_PATH,
            original_image_path=TEST_IMAGE_PATH,
            mosaic_tile_count=64,
            max_frames_to_match=100,
        )
    )

    expected_ratio = original_image.shape[0] // original_image.shape[1]
    actual_ratio = mosaic.shape[0] // mosaic.shape[1]

    assert expected_ratio == actual_ratio


def test__get_best_matching_frame_for_tile__black_and_white_frame__black_tile__return_black_frame() -> None:
    frames = [black_img(), white_img()]
    tile = black_img()

    result = get_best_matching_frame_for_tile(frames=frames, tile=tile)

    assert (result == black_img()).any()
