from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

Image = NDArray[np.uint8]


@dataclass
class Config:
    original_image_path: str
    video_path: str
    max_frames_to_match: int
    mosaic_tile_count: int
