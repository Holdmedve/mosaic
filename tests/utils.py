import cv2
import numpy as np

TEST_MP4_PATH = "tests/data/test_video.mp4"
TEST_JPG_PATH = "tests/data/pic1.jpg"

BLACK_PIXEL = [0, 0, 0]
WHITE_PIXEL = [255, 255, 255]

BLACK_IMG = np.array([[BLACK_PIXEL]])
WHITE_IMG = np.array([[WHITE_PIXEL]])


def black_img() -> np.ndarray:
    return cv2.imread("tests/data/black_pixel.png")


def white_img() -> np.ndarray:
    return cv2.imread("tests/data/white_pixel.png")


def green_img() -> np.ndarray:
    return cv2.imread("tests/data/green_pixel.png")


def blue_img() -> np.ndarray:
    return cv2.imread("tests/data/blue_pixel.png")


def red_img() -> np.ndarray:
    return cv2.imread("tests/data/red_pixel.png")
