from project.video import get_resized_frames_at_indeces
from tests.utils import TEST_VIDEO_PATH


def test__get_frames_at_indeces__given_2_indeces__returns_2_frames() -> None:
    frames = get_resized_frames_at_indeces(
        TEST_VIDEO_PATH, tuple([5, 2]), resized_height=100, resized_width=150
    )

    assert len(frames) == 2
