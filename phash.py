import cv2
import numpy as np


def pHash(image, hashSize=16):    
    # width is increased because the goal is to create
    # a diff image with dimensions hashSize*hashSize 
    # where the diff comes from adjacent columns
    resized = cv2.resize(image, (hashSize + 1, hashSize))
    #resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    hash_list = []
    for i in range(3):
        channel = resized[:, :, i]
        diff = channel[:, 1:] > channel[:, :-1]
        s = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
        hash_list.append(s)

    # convert boolen image to hash
    return hash_list


class Frame:
    def __init__(self, image, phash):
        self.image = image 
        self.phash = phash # perceptual hash


def processVideo(vidcap, tile_dim):
    """read a frame every second from the video 
        and return those frames"""

    frames = []

    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    success, image = vidcap.read()
    # specifies the frame to read
    cursor = 0

    print('processing video...')
    while success and cursor < frame_count:
        # downsize to tile level
        image = cv2.resize(image, tile_dim, interpolation=cv2.INTER_AREA)
        phash = pHash(image)
        
        frame = Frame(image, phash)
        frames.append(frame)

        # read and adjust cursor
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, cursor)
        success, image = vidcap.read()
        cursor += fps

    return frames
    

def calcTileHashes(target_image, split_level):
    """sclice the target image into tiles, then return
        the hashes of the tiles """

    height = int(target_image.shape[0] / split_level)
    width = int(target_image.shape[1] / split_level)

    print('calculating tile hashes...')
    tile_hashes = []
    for i in range(split_level):
        for j in range(split_level):
            
            s = (slice(i * height, (i + 1) * height), slice(j * width, (j + 1) * width))            

            tile = target_image[s]
            hash = pHash(tile)
            tile_hashes.append(hash)
            
    return tile_hashes

def avgDiff(target_hash, frame):
    diff_1 = abs(frame.phash[0] - target_hash[0])
    diff_2 = abs(frame.phash[1] - target_hash[1])
    diff_3 = abs(frame.phash[2] - target_hash[2])

    return (diff_1 + diff_2 + diff_3) / 3


def findBestFit(frames, tile_hashes):
    """for each tile find the best fitting frame based on 
        hash difference"""
    
    best_fit_indeces = []
    print('\nlen(tile_hashes): ' + str(len(tile_hashes)))

    print('finding best fits for each tile...')
    # for each tile find the frame with closest hash
    for target_hash in tile_hashes:
        
        best_idx = 0
        # assume first is best so we can compare in next loop
        best_avg_diff = avgDiff(target_hash, frames[0])
        
        for idx, f in enumerate(frames):
            cur_avg_diff = avgDiff(target_hash, f)
            if cur_avg_diff < best_avg_diff:
                best_idx = idx
                best_avg_diff = cur_avg_diff

        best_fit_indeces.append(best_idx)

    return best_fit_indeces

def suture(frames, indeces, split_level):

    mozaik = None
    row = None
    print('suture the final output...')
    for count, idx in enumerate(indeces):
        #print('count:\t' + str(count) + '\tidx:\t' + str(idx))
        if count % split_level == 0: 
            if count == split_level:
                mozaik = row
            elif count > split_level:
                mozaik = np.concatenate((mozaik, row), axis=0)
            
            # start new row
            row = frames[idx].image
        else:
            row = np.concatenate((row, frames[idx].image), axis=1)

    return mozaik




def createMozaik(video_path, target_image_path, recursion_level):
    
    vidcap = cv2.VideoCapture(video_path)
    if vidcap is None or not vidcap.isOpened():
        print('Unable to open video source: ', video_path)
        exit(1)

    target_image = cv2.imread(target_image_path)
    split_level = 2 ** recursion_level

    # the target image is split into tiles based on the recursion level
    tile_width = int(target_image.shape[1] / split_level)
    tile_height = int(target_image.shape[0] / split_level)

    tile_dim = (tile_width, tile_height)

    frames = processVideo(vidcap, tile_dim)
    tile_hashes = calcTileHashes(target_image, split_level)
    indeces = findBestFit(frames, tile_hashes)
    mozaik = suture(frames, indeces, split_level)

    # save final result
    path = 'my_mozaik.jpg'
    cv2.imwrite(path, mozaik)
    print('mozaik saved as ', path)
    


target_image = 'images/ey_boss.jpg'
video = 'videos/best_of.mp4'
recursion_level = 6

createMozaik(video, target_image, recursion_level)

