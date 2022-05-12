from project.mosavid import create_mosaic_from_video
from tests.utils import TEST_JPG_PATH, TEST_MP4_PATH


if __name__ == "__main__":
    create_mosaic_from_video(
        source_video_path=TEST_MP4_PATH, target_img_path=TEST_JPG_PATH
    )
