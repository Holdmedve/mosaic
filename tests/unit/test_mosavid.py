from project.helpers import get_random_non_negative_integers
from project.mosavid import (
    generate_mosaic,
    get_best_matching_frame_for_tile,
)

from project.types import Config
from tests.utils import *


# def test__stitch_tiles__when_called_with_4_pixels_as_tiles__returns_them_as_1_array() -> None:
#     tiles = [
#         [black_img(), white_img()],
#         [white_img(), black_img()],
#     ]
#     expected_image: Image = np.array(
#         [[BLACK_PIXEL, WHITE_PIXEL], [WHITE_PIXEL, BLACK_PIXEL]]
#     )

#     image = stitch_grid_of_images_together(tiles)

#     assert (image == expected_image).all()


# def test__mean_color_euclidian_distance__when_called_with_same_image__returns_1() -> None:
#     img = cv2.imread(TEST_IMAGE_PATH)

#     dst = mean_color_euclidian_distance(img, img)

#     assert dst == 0.0


# def test__mean_color_euclidian_distance__when_called_with_black_and_white_pixels__returns_body_diagonal_of_cube_with_255_long_edges() -> None:
#     # return value of tested function is rounded differently hence the use of str
#     expected_dst = 255 * np.sqrt(3)
#     expected_dst = str(expected_dst)

#     dst = str(mean_color_euclidian_distance(black_img(), white_img()))

#     assert dst[: len(dst) - 1] == expected_dst[: len(expected_dst) - 2]


# def test__mean_color_euclidian_distance__order_of_inputs_does_not_influence_result() -> None:
#     result_1 = mean_color_euclidian_distance(BLACK_IMG, WHITE_IMG)
#     result_2 = mean_color_euclidian_distance(WHITE_IMG, BLACK_IMG)

#     assert result_1 == result_2


# def test__get_n_frames_from_kth_frame_from_video__returns_specified_number_of_frames() -> None:
#     expected_number_of_frames = 10

#     frames = get_n_frames_from_kth_frame(
#         TEST_VIDEO_PATH, n=expected_number_of_frames, k=0
#     )

#     assert len(frames) == expected_number_of_frames


# def test__get_n_frames_from_kth_frame_from_video__n_exceeds_total_frames__returns_total_number_of_frames() -> None:
#     capture = cv2.VideoCapture(TEST_VIDEO_PATH)
#     total_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)

#     frames = get_n_frames_from_kth_frame(TEST_VIDEO_PATH, n=9000, k=0)

#     assert len(frames) == total_frames


# def test__get_n_frames_from_kth_frame_from_video__k_exceeds_total_frames__returns_empty_list() -> None:
#     frames = get_n_frames_from_kth_frame(TEST_VIDEO_PATH, n=9000, k=666)

#     assert frames == []


# @pytest.mark.parametrize(
#     "tile_count, expected_tile_dimensions", [(4, (2, 2)), (9, (3, 3))]
# )
# def test__split_image_into_tiles__when_called_with_certain_tile_count__returns_tiles_in_excpected_dimensions(
#     tile_count: int, expected_tile_dimensions: tuple[int, ...]
# ) -> None:
#     data = MosaicData(
#         target_image_path=TEST_IMAGE_PATH,
#         source_video_path=TEST_VIDEO_PATH,
#         requested_tile_count=tile_count,
#     )
#     tiles = split_image_into_tiles(data)

#     assert len(tiles) == expected_tile_dimensions[0]
#     assert len(tiles[0]) == expected_tile_dimensions[1]
#     assert len({len(row) for row in tiles}) == 1


# @pytest.mark.parametrize(
#     "to_split, split_degree, expected_splits",
#     [
#         (300, 4, (0, 100, 200, 300)),
#         (1452, 8, (0, 207, 414, 622, 829, 1037, 1244, 1452)),
#     ],
# )
# def test__get_even_samples__when_called__returns_expected_splits(
#     to_split: int, split_degree: int, expected_splits: tuple[int, ...]
# ) -> None:
#     splits = get_even_samples(to_split, split_degree)

#     assert splits == expected_splits


# @pytest.mark.parametrize(
#     "invalid_data, expected_exception",
#     [
#         (
#             MosaicData(
#                 target_image_path="invalid_image_path",
#                 source_video_path=TEST_VIDEO_PATH,
#                 requested_tile_count=1,
#             ),
#             FileNotFoundError,
#         ),
#         (
#             MosaicData(
#                 target_image_path=TEST_IMAGE_PATH,
#                 source_video_path="invalid_video_path",
#                 requested_tile_count=1,
#             ),
#             FileNotFoundError,
#         ),
#         (
#             MosaicData(
#                 target_image_path=TEST_IMAGE_PATH,
#                 source_video_path=TEST_VIDEO_PATH,
#                 requested_tile_count=0,
#             ),
#             InvalidSplitLevel,
#         ),
#     ],
# )
# def test__is_data_valid__invalid_property__raises_expected_exception(
#     invalid_data: MosaicData,
#     expected_exception: Union[FileNotFoundError, InvalidSplitLevel],
# ) -> None:
#     with pytest.raises(expected_exception) as e:  # type: ignore
#         is_data_valid(data=invalid_data)


#################


def test__get_random_non_negative_integers__returns_unique_elements() -> None:
    indeces = get_random_non_negative_integers(range_max=10, num_integers=10, duplicates_allowed=False)

    assert len(indeces) == len(set(indeces))


def test__create_mosaic__given_a_config__runs_without_errors() -> None:
    generate_mosaic(
        config=Config(
            video_path=TEST_VIDEO_PATH,
            original_image_path=TEST_IMAGE_PATH,
            mosaic_tile_count=64,
            max_frames_to_match=100,
        )
    )

def test__get_best_matching_frame_for_tile__black_and_white_frame__black_tile__return_black_frame() -> None:
    frames = [black_img(), white_img()]
    tile = black_img()

    result = get_best_matching_frame_for_tile(frames=frames, tile=tile)

    assert (result == black_img()).any()

