import cv2
import pytest


from project.mosavid import stitch_tiles, split_image_into_tiles

TEST_JPG_PATH = "data/pic1.jpg"


def test__split_into_tiles_and_stitcing_back_together__results_in_original_image():
    original_image = cv2.imread(TEST_JPG_PATH)

    tiles = split_image_into_tiles(TEST_JPG_PATH, 2)
    stitched_image = stitch_tiles(tiles)

    cv2.imwrite("the_stitched_image.jpg", stitched_image)

    assert (original_image == stitched_image).all()
