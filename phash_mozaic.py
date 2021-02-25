import cv2

def diffHash(image, hashSize=8):    
    # width is increased because the goal is to create
    # a diff image with dimensions hashSize*hashSize 
    # where the diff comes from adjacent columns
    resized = cv2.resize(image, (hashSize + 1, hashSize))
    hash_sum = 0

    for i in range(3):
        channel = resized[:, :, i]
        diff = channel[:, 1:] > channel[:, :-1]
        s = sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
        hash_sum += s

    # convert boolen image to hash
    return hash_sum



img1 = cv2.imread('images/ey_boss.jpg')
hash1 = diffHash(img1)

img2 = cv2.imread('images/pink_guy.jpg')
hash2 = diffHash(img2)

hash_diff = abs(hash1 - hash2)
print(hash_diff)
