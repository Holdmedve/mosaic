import cv2
import os

from dataclasses import dataclass
from numpy import ndarray
from typing import Callable, List


class InvalidSplitLevel(Exception):
    pass


def comparison_method(imgA, imgB) -> float:
    pass


@dataclass
class Config:
    split_level: int
    comparison_method: Callable[[ndarray, ndarray], float]


@dataclass
class Data:
    target_image: str
    source_video: str


def get_frames_from_video(vid_path: str) -> List[ndarray]:
    if not os.path.exists(vid_path):
        raise FileNotFoundError

    capture = cv2.VideoCapture(vid_path)
    frames = []

    while True:
        success, frame = capture.read()
        if success:
            frames.append(frame)
        else:
            break

    capture.release()

    return frames


# splits = np.linspace(0, 1452, 8)
# list(map(lambda x: int(x), splits))


def split_image_into_tiles(img_path: str, split_level: int) -> List[List[ndarray]]:
    if split_level < 1:
        raise InvalidSplitLevel("split level must be at least 1")

    if not os.path.exists(img_path):
        raise FileNotFoundError

    img = cv2.imread(img_path)

    tile_height = int(img.shape[0] / 2**split_level)
    tile_width = int(img.shape[2] / 2**split_level)
    horizontal_splits = split_integer()

    tiles: List[List[ndarray]]


# def create_mosaic(data: Data, config: Config) -> ndarray:
#    pass
