import cv2

from project.mosavid import generate_mosaic
from project.types import Config
from tests.utils import TEST_IMAGE_PATH, TEST_VIDEO_PATH


if __name__ == "__main__":
    mosaic = generate_mosaic(
        config=Config(
            original_image_path='C:/Users/Holdmedve/Desktop/mosavid_test_content/gandalf.jpg',
            video_path='C:/Users/Holdmedve/Desktop/mosavid_test_content/lotr.mp4', 
            mosaic_tile_count=4096,
            max_frames_to_match=100
        )
    )

    cv2.imwrite(filename='result.jpg', img=mosaic)
