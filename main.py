from process_video import Mozavid

# setup
video_path = 'videos/RICE_BALLS.mp4'
target_frame = 360

dst_path = 'my_mozaic'
recursion_level = 4
histogram_threshold = 0.2

# level of division on a sinlge tile to calculate histogram
histogram_recursion = 4

mozavid = Mozavid(video_path, target_frame, recursion_level, histogram_threshold)
mozavid.ProcessVideo(dst_path, histogram_recursion)
