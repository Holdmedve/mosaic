import numpy as np
import cv2

class Frame:

    def __init__(self, image):
        self.image = image
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        
    

class Mozavid:
    def __init__(self, vid_path, target_frame, recursion_level):
        self.vidcap = cv2.VideoCapture(vid_path)
        self.target_frame = target_frame
        self.recursion_level = recursion_level

        

    def CreateTiles(self, frames):
        """Quarter the target frame as many times as specified be the recursion level
            A tile is a piece of the target frame to be covered
            by one of the (downsized)frames. Which frame u ask?
            One whoose histogram is similar enough to the tile """

        print(frames[self.target_frame].image.shape)
        

    def CreateMozaic(self, dst_path):
        self.dst_path = dst_path # path of the final result

        # in case you need it
        #framespersecond= int(cap.get(cv2.CAP_PROP_FPS))

        # lehet eleve olyan felbontásban érdemes olvasni, amekkora egy tile
        # lehet gyorsítana a dolgokon, bár kevesebb pixel alapján
        # számolnál histogram-ot
        success, image = self.vidcap.read()
        count = 0
        frames = []
        limit = 420 # to make things faster in development

        while success and count < limit:
            if count % 100 == 0:
                # save frame as JPEG file
                # cv2.imwrite("frames/frame%d.jpg" % count, frame)  
                #print('still chewing...')                
                pass

            frame = Frame(image)
            frames.append(frame)

            success, image = self.vidcap.read()
            count += 1

        self.CreateTiles(frames)
        self.ExecuteHistogramComparison(frames)
    
    def ExecuteHistogramComparison(self, frames):
        """Compare the histograms of the target"""

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





    
    def FramesAreDifferent(self, one_frame, other_frame):
        #one_frame.shape == other_frame.shape and not(np.bitwise_xor(one_frame,other_frame).any())
        # here i assume that the two frames have the same shape
        return np.bitwise_xor(one_frame,other_frame).any()