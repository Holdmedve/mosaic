import numpy as np
import cv2

class Frame:

    def __init__(self, image):
        self.hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        
    

class Mozavid:
    def __init__(self, vid_path, target_frame, recursion_level):
        self.vidcap = cv2.VideoCapture(vid_path)
        self.target_frame = target_frame
        self.recursion_level = recursion_level

    def CreateMozaic(self, dst_path):
        self.dst_path = dst_path # path of the final result

        # in case you need it
        #framespersecond= int(cap.get(cv2.CAP_PROP_FPS))

        success, image = self.vidcap.read()
        count = 0
        frames = []

        while success:
            if count % 100 == 0:
                # cv2.imwrite("frames/frame%d.jpg" % count, frame)  # save frame as JPEG file
                print('still chewing...')                

            frame = Frame(image)
            frames.append(frame)

            success, image = self.vidcap.read()
            print(type(image))
            count += 1
    
    def ExecuteHistogramComparison():
        pass

    
    def FramesAreDifferent(self, one_frame, other_frame):
        #one_frame.shape == other_frame.shape and not(np.bitwise_xor(one_frame,other_frame).any())
        # here i assume that the two frames have the same shape
        return np.bitwise_xor(one_frame,other_frame).any()