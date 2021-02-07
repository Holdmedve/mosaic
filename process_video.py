import numpy as np
import cv2

# https://docs.opencv.org/4.5.1/d8/dc8/tutorial_histogram_comparison.html

class Frame:

    def __init__(self, image):
        self.image = image
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.hist = self.CalculateHistogram()

    def CalculateHistogram(self):
        # bins help reduce computation time
        # they split the range into the specified number of bins
        h_bins = 16
        s_bins = 32
        histSize = [h_bins, s_bins]

        # hue varies from 0 to 179 (opencv specific), saturation from 0 to 255
        h_ranges = [0, 180]
        s_ranges = [0, 256]
        ranges = h_ranges + s_ranges  # concat lists
        
        channels = [0, 1]

        hist = cv2.calcHist([self.hsv], channels, None, histSize, ranges, accumulate=False)
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        return hist
        
    
# A mozaic made from a video
class Mozavid:
    def __init__(self, vid_path, target_frame_idx, recursion_level):
        
        # checks
        if not isinstance(recursion_level, int) or recursion_level <= 0:
            print('recursion level has to be an integer above 0')
            exit(1)

        # target frame nem létezik

        # útvonalon nem létezik mp4

        self.vidcap = cv2.VideoCapture(vid_path)

        # the frame to be recreated
        self.target_frame_idx = target_frame_idx
        # the target frame is split recursively this many times into quarters
        self.recursion_level = recursion_level

        

    def CreateTiles(self, target_frame):
        """Quarter the target frame as many times as specified be the recursion level
            A tile is a piece of the target frame to be covered
            by one of the (downsized)frames. Which frame u ask?
            One whoose histogram is similar enough to the tile """

        
        shape = target_frame.image.shape

        # this is how many times the edges of the target frame
        # are split into equal length sections
        split_level = 2 ** self.recursion_level

        height = shape[0] // (split_level)
        width = shape[1] // (split_level)
        tile_resolution = (height, width)

        #DEBUG
        print(height)
        print(width)
        print(tile_resolution)

        tiles = []
        count = 0
        for i in range(split_level):
            for j in range(split_level):
                
                tile = target_frame.image[i * height:(i + 1) * height, j * width:(j + 1) * width]
                tiles.append(Frame(tile))
                
                #cv2.imwrite("frames/frame%d.jpg" % count, tile)

                count += 1 

        return tiles
            

        

    def ProcessVideo(self, dst_path):
        self.dst_path = dst_path # path of the final result

        # in case you need it
        #framespersecond= int(cap.get(cv2.CAP_PROP_FPS))

        # lehet eleve olyan felbontásban érdemes olvasni, amekkora egy tile
        # lehet gyorsítana a dolgokon, bár kevesebb pixel alapján
        # számolnál histogram-ot
        success, image = self.vidcap.read()
        count = 0
        frames = []
        limit = 420 # to make things faster

        while success and count < limit:
            if count % 100 == 0:
                # cv2.imwrite("frames/frame%d.jpg" % count, frame)  
                #print('still chewing...')                
                pass

            frame = Frame(image)
            frames.append(frame)

            success, image = self.vidcap.read()
            count += 1

        target_frame = frames[self.target_frame_idx]
        tiles = self.CreateTiles(target_frame)
        
        self.CompareHistograms(frames, tiles)
    
    def CompareHistograms(self, frames, tiles):
        """for each tile find the most fitting frame"""

        threshold = 0.5 # might not even need it
        indeces = [] # holds the best fitting frame indeces

        for tile in tiles:            
            best_fit_idx = 0
            best_similarity = 0

            for idx, frame in enumerate(frames):
                similarity = cv2.compareHist(frame.hist, tile.hist, 0)
                
                # similarity > threshold
                if similarity > best_similarity and idx not in indeces:
                    best_similarity = similarity
                    best_fit_idx = idx

            indeces.append(best_fit_idx)







    
    def FramesAreDifferent(self, one_frame, other_frame):
        #one_frame.shape == other_frame.shape and not(np.bitwise_xor(one_frame,other_frame).any())
        # here i assume that the two frames have the same shape
        return np.bitwise_xor(one_frame,other_frame).any()