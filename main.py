from process_video import Mozavid

# setup
video_path = 'RICE_BALLS.mp4'
target_frame = 840

dst_path = 'my_mozaic'
recursion_level = 5 # resolution = 4^recursion_level

mozavid = Mozavid(video_path, target_frame, recursion_level)
mozavid.ProcessVideo(dst_path)
