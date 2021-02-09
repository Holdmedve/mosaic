import numpy as np
import cv2

# https://docs.opencv.org/4.5.1/d8/dc8/tutorial_histogram_comparison.html
# calculate the histogram not for a tile, but the 4 quarters of the tile or more
# my hope is that this way the program is somewhat "aware" about the
# position of the colors, as a single histogram gives only a distribution

# to seleect a frame for a tile, sum the 4(or more) histogram comparison outputs (or try the average)
# if that sum is above a threshold, it's good enough 

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

        
    
# mozaic made from a video
class Mozavid:
    def __init__(self, vid_path, target_frame_idx, recursion_level, histogram_threshold):
        
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
        # threshold when filling the mozaik with tiles
        self.threshold = histogram_threshold

        

    def CreateTiles(self, target_frame):
        """Quarter the target frame as many times as specified be the recursion level
            A tile is a piece of the target frame to be covered
            by one of the (downsized)frames. Which frame u ask?
            One whoose histogram is similar enough to the tile """

        #height = self.tile_height
        #width = self.tile_width
        height = int(target_frame.image.shape[0] / self.split_level)
        width = int(target_frame.image.shape[1] / self.split_level)

        tiles = []
        count = 0
        for i in range(self.split_level):
            for j in range(self.split_level):
                
                tile = target_frame.image[i * height:(i + 1) * height, j * width:(j + 1) * width]
                tiles.append(Frame(tile))
                count += 1
                
        for i, t in enumerate(tiles):
            cv2.imwrite("tiles/" + str(i) + ".jpg", t.image)

        return tiles
            

        

    def ProcessVideo(self, dst_path):
        self.dst_path = dst_path # path of the final result

        # lehet eleve olyan felbontásban érdemes olvasni, amekkora egy tile
        # lehet gyorsítana a dolgokon, bár kevesebb pixel alapján
        # számolnál histogram-ot
        success, image = self.vidcap.read()
        frames = []
        
        #fps = int(self.vidcap.get(cv2.CAP_PROP_FPS))
        frame_count = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        print("\n\nstep 1 out of 3")
        print("processing video...")

        # this is how many times the edges of the target frame
        # are split into equal length sections
        self.split_level = 2 ** self.recursion_level

        # tile dimensions; every frame that's not the target frame
        # is downsized to tile dimensions 
        self.tile_width = int(image.shape[1] / self.split_level)
        self.tile_height = int(image.shape[0] / self.split_level)
        dim = (self.tile_width, self.tile_height)

        num = 0
        count = 0

        while success:
            # show progress
            percent = int(count / frame_count * 100)
            if percent // 10 > num // 10:
                print(str(percent) + "%")
                num = percent

            if count != self.target_frame_idx:
                image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            frame = Frame(image)
            frames.append(frame)

            success, image = self.vidcap.read()
            count += 1

        print("100%")

        target_frame = frames[self.target_frame_idx]
        tiles = self.CreateTiles(target_frame)
        
        self.CompareHistograms(frames, tiles)


    
    def CompareHistograms(self, frames, tiles):
        """for each tile find a frame that's similar enough"""

        threshold = 0.3
        indeces = []
        
        print("\n\nstep 2 out of 3")
        print("comparing histograms...")


        num = 0
        listIdx = 0
        for i, tile in enumerate(tiles):
            # show progress
            percent = int(i / len(tiles) * 100)
            if percent // 10 > num // 10:
                print(str(percent) + "%")
                num = percent

            best_fit_idx = 0
            best_similarity = 0

            tries = 0
            while tries < len(frames):
                # reset to beginning
                if listIdx == len(frames): listIdx = 0

                # avoid placing target frame as a tile (dimensions won't fit)
                if listIdx == self.target_frame_idx:
                    listIdx += 1
                    tries += 1
                    continue
                
                frame_hist = frames[listIdx].hist
                similarity = cv2.compareHist(frame_hist, tile.hist, 0)
                
                if similarity > threshold:
                    best_fit_idx = listIdx
                    break

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_fit_idx = listIdx

                listIdx += 1
                tries += 1

            indeces.append(best_fit_idx)

        print("100%")

        self.CreateMozaik(indeces, frames)



    def CreateMozaik(self, indeces, frames):
        """create the final output
            indeces mark which frames to use """

        mozaik = None
        row = None
        new_row = True
        mozaik_empty = True

        print("\n\nstep 3 out of 3")
        print("\ncreating mozaik...")

        dim = (self.tile_width, self.tile_height)
        num = 0
        # create the mozaik row-by-row
        for count, idx in enumerate(indeces):
            # show progress
            percent = int(count / len(indeces) * 100)
            if percent // 10 > num // 10:
                print(str(percent) + "%")
                num = percent

            #image = frames[idx].image
            #tile = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
            tile = frames[idx].image

            if new_row == True:
                row = tile
                new_row = False
            else:
                row = np.concatenate((row, tile), axis=1)

            if count > 0 and (count + 1) % self.split_level == 0:
                if mozaik_empty == True:
                    mozaik = row
                    mozaik_empty = False
                else:
                    mozaik = np.concatenate((mozaik, row), axis=0)
                new_row = True

        print("100%")

        
        # save final product
        cv2.imwrite(self.dst_path + ".jpg", mozaik)
        print("saved as " + self.dst_path + ".jpg")
        

    
    def FramesAreDifferent(self, one_frame, other_frame):
        #one_frame.shape == other_frame.shape and not(np.bitwise_xor(one_frame,other_frame).any())
        # here i assume that the two frames have the same shape
        return np.bitwise_xor(one_frame,other_frame).any()