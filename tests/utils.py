import cv2
import numpy as np
from project.types import Image

TEST_MP4_PATH = "tests/data/test_video.mp4"
TEST_JPG_PATH = "tests/data/pic1.jpg"

BLACK_PIXEL = [0, 0, 0]
WHITE_PIXEL = [255, 255, 255]

BLACK_IMG: Image = np.array([[BLACK_PIXEL]], dtype=np.int32)
WHITE_IMG: Image = np.array([[WHITE_PIXEL]], dtype=np.int32)


def black_img() -> cv2.Mat:
    return cv2.imread("tests/data/black_pixel.png")


def white_img() -> cv2.Mat:
    return cv2.imread("tests/data/white_pixel.png")


def green_img() -> cv2.Mat:
    return cv2.imread("tests/data/green_pixel.png")


def blue_img() -> cv2.Mat:
    return cv2.imread("tests/data/blue_pixel.png")


def red_img() -> cv2.Mat:
    return cv2.imread("tests/data/red_pixel.png")
