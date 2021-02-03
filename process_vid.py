import numpy as np
import cv2

def CreateFrames(vid_path):
    vidcap = cv2.VideoCapture(vid_path)

    success, frame = vidcap.read()
    prev_frame = frame
    success, frame = vidcap.read()    

    count = 0
    limit = 500
    step = 12 # number of frames to step over

    while success and count < limit:
        if count % step == 0:
            cv2.imwrite("frames/frame%d.jpg" % count, frame)  # save frame as JPEG file  
            print('still chewing...')    

        prev_frame = frame
        success, frame = vidcap.read()

        count += 1

def FramesAreDifferent(one_frame, other_frame):
    #one_frame.shape == other_frame.shape and not(np.bitwise_xor(one_frame,other_frame).any())
    # here i assume that the two frames have the same shape
    return np.bitwise_xor(one_frame,other_frame).any()