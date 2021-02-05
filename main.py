from process_vid import Mozavid

# setup
video_path = 'RICE_BALLS.mp4'
target_frame = 360

dst_path = 'my_mozaic'
recursion_level = 4 # resolution = 4^recursion_level

mozavid = Mozavid(video_path, target_frame, recursion_level)
mozavid.CreateMozaic(dst_path)
