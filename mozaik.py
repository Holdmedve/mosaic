import numpy as np
import cv2
import argparse
import os

class Frame:
    def __init__(self, image, color_mean):
        self.image = image
        self.color_mean = color_mean


def calcColorMean(image):
    mean_color_per_row = np.average(image, axis=0)
    mean_color = np.average(mean_color_per_row, axis=0)

    return mean_color


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
        color_mean = calcColorMean(image)
        
        frame = Frame(image, color_mean)
        frames.append(frame)

        # read and adjust cursor
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, cursor)
        success, image = vidcap.read()
        cursor += fps

    return frames


def processTarget(target_image, split_level):
    height = int(target_image.shape[0] / split_level)
    width = int(target_image.shape[1] / split_level)

    print('processing target image...')
    target_means = []

    for i in range(split_level):
        for j in range(split_level):
            
            s = (slice(i * height, (i + 1) * height), slice(j * width, (j + 1) * width))
            tile = target_image[s]
            color_mean = calcColorMean(tile)
            target_means.append(color_mean)

    return target_means


def distance(frame_mean, tile_mean):
    
    sq_x = (frame_mean[0] - tile_mean[0]) * (frame_mean[0] - tile_mean[0])
    sq_y = (frame_mean[1] - tile_mean[1]) * (frame_mean[1] - tile_mean[1])
    sq_z = (frame_mean[2] - tile_mean[2]) * (frame_mean[2] - tile_mean[2])

    sqrt = np.sqrt(sq_x + sq_y + sq_z)
    return sqrt


def findBestFit(frames, tile_color_means):
    
    best_fits = []

    print('looking for best fit for each tile...')
    for t_mean in tile_color_means:
        best_idx = 0
        closest = distance(t_mean, frames[0].color_mean)

        for idx, f in enumerate(frames):
            dist = distance(t_mean, f.color_mean)
            
            if dist < closest:
                closest = dist
                best_idx = idx

        best_fits.append(best_idx)

    return best_fits


def suture(frames, indeces, split_level):

    mozaik = None
    row = None
    print('suture the final output...')
    for count, idx in enumerate(indeces):
        
        if count % split_level == 0: # end of row
            if count == split_level: # first row done
                mozaik = row
            elif count > split_level:
                mozaik = np.concatenate((mozaik, row), axis=0)
            
            # start new row
            row = frames[idx].image
        else:
            row = np.concatenate((row, frames[idx].image), axis=1)

    return mozaik


def validateArgs(video_path, target_image_path):
    
    if not os.path.exists(video_path):
        print('video path is invalid')
        exit(1)

    if not os.path.exists(target_image_path):
        print('target image path is invalid')
        exit(1)

def createMozaik(video_path, target_image_path, recursion_level):
    
    validateArgs(video_path, target_image_path)

    vidcap = cv2.VideoCapture(video_path)
    if vidcap is None or not vidcap.isOpened():
        print('Unable to open video source: ', video_path)
        exit(1)

    target_image = cv2.imread(target_image_path)
    split_level = 2 ** recursion_level

    # the target image is split into tiles based on the recursion level
    tile_width = int(target_image.shape[1] / split_level *tile_scale)
    tile_height = int(target_image.shape[0] / split_level *tile_scale)

    tile_dim = (tile_width, tile_height)

    frames = processVideo(vidcap, tile_dim)

    # list containing the color mean for each tile
    tile_color_means = processTarget(target_image, split_level)

    indeces = findBestFit(frames, tile_color_means)
    mozaik = suture(frames, indeces, split_level)

    # save final result
    path = 'my_mozaik.jpg'
    cv2.imwrite(path, mozaik)
    print('mozaik saved as ', path)


parser = argparse.ArgumentParser()
parser.add_argument('target_image', type=str, help='the mozaic will be made from this image')
parser.add_argument('video', type=str, help='video where the frames will be used to create the mozaic tiles')

parser.add_argument('-r', '--recursion', type=int, default=6, 
    help='specifies how many times the target image is split into quarters (default:6)')
parser.add_argument('-s', '--scale', type=int, default=4,
    help='each tile is scaled by this number (default:4)')

args = parser.parse_args()


target_image = args.target_image
video = args.video
recursion_level = args.recursion
tile_scale = args.scale


createMozaik(video, target_image, recursion_level)