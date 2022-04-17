import pytest
import cv2
import numpy as np

from project.mosavid import (
    get_frames_from_video,
    split_image_into_tiles,
    get_even_samples,
    mean_color_euclidian_distance,
    stitch_tiles,
    InvalidSplitLevel,
)

TEST_MP4_PATH = "data/test_video.mp4"
TEST_JPG_PATH = "data/pic1.jpg"

BLACK_PIXEL = [0, 0, 0]
WHITE_PIXEL = [256, 256, 256]


class TestStitchTiles:
    def test__when_called_with_4_pixels_as_tiles__returns_them_as_1_array(self):
        tiles = [
            [np.array([[[BLACK_PIXEL]]]), np.array([[[WHITE_PIXEL]]])],
            [np.array([[[WHITE_PIXEL]]]), np.array([[[BLACK_PIXEL]]])],
        ]
        expected_black_image = np.array(
            [[[BLACK_PIXEL], [WHITE_PIXEL]], [[WHITE_PIXEL], [BLACK_PIXEL]]]
        )

        image = stitch_tiles(tiles)

        assert (image == expected_black_image).all()


class TestMeanColorEuclidianDistance:
    def test__when_called_with_same_image__returns_1(self):
        img = cv2.imread(TEST_JPG_PATH)

        dst = mean_color_euclidian_distance(img, img)

        assert dst == 0.0

    def test__when_called_with_black_and_white_pixels__returns_body_diagonal_of_cube_with_256_long_edges(
        self,
    ):
        black = np.array([[BLACK_PIXEL]])
        white = np.array([[WHITE_PIXEL]])

        dst = mean_color_euclidian_distance(black, white)

        assert dst == 256 * np.sqrt(3)


class TestGetFramesFromVideo:
    def test__when_called__returns_right_number_of_frames(self):
        frames = get_frames_from_video(TEST_MP4_PATH)
        assert len(frames) == 145

    def test__when_called_with_path_not_pointing_to_file__raises_exception(self):
        with pytest.raises(FileNotFoundError):
            get_frames_from_video("definitely_wrong_file_path.truly_wrong")


class TestSplitImageIntoTiles:
    def test__when_called_with_incorrect_split_level__raises_exception(self):
        with pytest.raises(InvalidSplitLevel, match="split level must be at least 1"):
            split_image_into_tiles(TEST_JPG_PATH, 0)

    def test__when_called_with_path_not_pointing_to_file__raises_exception(self):
        with pytest.raises(FileNotFoundError):
            split_image_into_tiles("definitely_wrong_file_path.truly_wrong", 1)

    @pytest.mark.parametrize(
        "split_level, expected_tile_dimensions", [(1, (2, 2)), (3, (8, 8))]
    )
    def test__when_called_with_certain_split_level__returns_tiles_in_excpected_dimensions(
        self, split_level, expected_tile_dimensions
    ):
        tiles = split_image_into_tiles(TEST_JPG_PATH, split_level)

        assert len(tiles) == expected_tile_dimensions[0]
        assert len(tiles[0]) == expected_tile_dimensions[1]
        assert len({len(row) for row in tiles}) == 1


class TestSplitInteger:
    @pytest.mark.parametrize(
        "to_split, split_degree, expected_splits",
        [
            (300, 4, (0, 100, 200, 300)),
            (1452, 8, (0, 207, 414, 622, 829, 1037, 1244, 1452)),
        ],
    )
    def test__when_called__returns_expected_splits(
        self, to_split, split_degree, expected_splits
    ):
        splits = get_even_samples(to_split, split_degree)

        assert splits == expected_splits
