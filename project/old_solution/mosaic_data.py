from dataclasses import dataclass


@dataclass
class MosaicData:
    requested_tile_count: int
    target_image_path: str
    source_video_path: str
