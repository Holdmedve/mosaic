import numpy as np

from project.similarity import mean_color_similarities, mean_color_similarity
from tests.utils import black_img, green_img, red_img, white_img


def test__mean_color_similairity___black_and_white_images__returns_0() -> None:
    assert mean_color_similarity(black_img(), white_img()) == 0


def test__mean_color_similairity___same_images__returns_1() -> None:
    assert mean_color_similarity(black_img(), black_img()) == 1


def test__mean_color_similairity___order_of_inputs__same_output() -> None:
    output_1 = mean_color_similarity(black_img(), white_img())
    output_2 = mean_color_similarity(white_img(), black_img())

    assert output_1 == output_2


def test__mean_color_similarity__red_and_green_are_more_similar_than_black_and_white() -> None:
    red_green_similarity = mean_color_similarity(red_img(), green_img())
    black_white_similairity = mean_color_similarity(white_img(), black_img())

    assert red_green_similarity > black_white_similairity


def test__mean_color_similarities__returns_expected_similarities() -> None:
    images = np.array([black_img(), white_img()], dtype=np.uint8)
    image_to_compare = black_img()

    similarities = mean_color_similarities(
        images=images, image_to_compare=image_to_compare
    )

    assert similarities == (1.0, 0.0)
