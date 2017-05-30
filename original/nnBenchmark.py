import faiss, numpy as np
import cv2
import cPickle
import time
from sklearn.neighbors import NearestNeighbors
def unpickle(file):
    fo = open(file, 'rb') 
    dict = cPickle.load(fo) 
    fo.close() 
    return dict

def getHogs(batchNum, imgCnt):
	batchDir = '../batch'+str(batchNum)
	imgPrefix = '.png'
	#if cell size is  too small, then accuracy is all small
	winSize=(32,32)
	blockSize=(32,32)
	blockStride=(4,4)
	cellSize=(4,4)
	nbins=7
	hogs=[None]*imgCnt
	for i in range(imgCnt):
		im=cv2.imread(batchDir+'/'+str(i)+imgPrefix)
		hog=cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)
		hogs[i]=[featureL[0] for featureL in  hog.compute(im)]
	print 'hog dimension:' + str(len(hogs[0]))
	hogs=np.asarray(hogs)
	return hogs

def drawKnn(hogs, d, k):
	index = faiss.IndexFlatL2(d)   # build the index
	index.add(hogs)                  # add vectors to the index
	k=k+1
	D, I = index.search(hogs, k)
	return (D, I)

batchNum = 1
imgCnt = 10000
import sys
k=int(sys.argv[1])
print 'k:'+str(k)
print 'imgCnt:' + str(imgCnt)
hogs = getHogs(batchNum, imgCnt)
d=len(hogs[0])
beforeT = time.time()
D, I = drawKnn(hogs, d, k)
afterT = time.time()
print 'faiss time elapsed:' + str(afterT-beforeT)

beforeT = time.time()
nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(hogs)
distances, indices = nbrs.kneighbors(hogs)
afterT = time.time()
print 'sklearn:' + str(afterT-beforeT)

