from process_video import Mozavid

# setup
video_path = 'videos/riceballs.mp4'
target_frame = 360

dst_path = 'my_mozaic'
recursion_level = 5
histogram_threshold = 0.2

# level of division on a sinlge tile to calculate histogram
histogram_recursion = 2

mozavid = Mozavid(video_path, target_frame, recursion_level, histogram_threshold)
mozavid.ProcessVideo(dst_path, histogram_recursion)
