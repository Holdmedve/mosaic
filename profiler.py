from project.mosavid import create_mosaic_from_video
from tests.utils import TEST_JPG_PATH, TEST_MP4_PATH
from project.mosaic_data import MosaicData


if __name__ == "__main__":
    create_mosaic_from_video(
        data=MosaicData(
            requested_tile_count=32, 
            source_video_path='C:/Users/Holdmedve/Desktop/mosavid_test_content/lotr.mp4', 
            target_image_path='C:/Users/Holdmedve/Desktop/mosavid_test_content/gandalf.jpg'
        )
    )
