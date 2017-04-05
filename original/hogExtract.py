import cv2
im=cv2.imread('./batch1/0.png')
winSize=(32,32)
blockSize=(8,8)
blockStride=(4,4)
cellSize=(4,4)
hog=cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,3)
len(hog.compute(im))