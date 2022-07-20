import pytest

from project.helpers import get_even_samples


@pytest.mark.parametrize(
    "to_split, split_degree, expected_splits",
    [
        (300, 4, (0, 100, 200, 300)),
        (1452, 8, (0, 207, 414, 622, 829, 1037, 1244, 1452)),
    ],
)
def test__get_even_samples__returns_expected_splits(
    to_split: int, split_degree: int, expected_splits: tuple[int, ...]
) -> None:
    splits = get_even_samples(to_split, split_degree)

    assert splits == expected_splits
