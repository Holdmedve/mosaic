from process_video import Mozavid

# setup
video_path = 'stfu.mp4'
target_frame = 3960

dst_path = 'my_mozaic'
recursion_level = 6 # resolution = 4^recursion_level
histogram_threshold = 0.15

mozavid = Mozavid(video_path, target_frame, recursion_level, histogram_threshold)
mozavid.ProcessVideo(dst_path)
