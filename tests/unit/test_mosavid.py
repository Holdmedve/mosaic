import pytest

from project.mosavid import (
    get_frames_from_video,
    split_image_into_tiles,
    InvalidSplitLevel,
)

TEST_MP4_PATH = "data/test_video.mp4"
TEST_JPG_PATH = "data/pic1.jpg"


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

        assert tiles.shape == expected_tile_dimensions

    def test__when_called__returned_tiles_make_up_original_image(self):
        assert 1 == 0


# @pytest.mark.parametrize("function", [get_frames_from_video, split_image_into_tiles])
# def test__when_function_called_with_path_not_pointing_to_file__raises_exception(
#     function,
# ):
#     with pytest.raises(FileNotFoundError):
#         function()
