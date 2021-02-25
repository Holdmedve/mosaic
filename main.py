from process_video import Mozavid

# setup
video_path = 'videos/compilation.mp4'
target_image = 'images/vsauce.jpg'

dst_path = 'my_mozaic'
recursion_level = 6
histogram_threshold = 9000

# level of division on a sinlge tile to calculate histogram
histogram_recursion = 0

mozavid = Mozavid(video_path, recursion_level, histogram_threshold)
mozavid.ProcessVideo(dst_path, histogram_recursion, target_image)
