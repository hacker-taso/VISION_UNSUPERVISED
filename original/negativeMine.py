import faiss, numpy as np
import cv2
import cPickle
import heapq
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

def getLabels(batchNum):
	batchFile = '../data_batch_'+str(batchNum)
	batchInfo = unpickle(batchFile)
	labels = batchInfo['labels']
	return labels

def floydwarshall(I, D):
	vs=xrange(len(I))
	dist = {}
	pred = {}
	for u in vs:
		dist[u] = {}
		pred[u] = {}
		for v in vs:
			dist[u][v] = float('inf')
			pred[u][v] = -1
			dist[u][u] = 0
		for neighborIdx in range(1, len(I[u])):
			dist[u][I[u][neighborIdx]] = D[u][neighborIdx]
			pred[u][I[u][neighborIdx]] = u
		for t in vs:
			# given dist u to v, check if path u - t - v is shorter
			for u in vs:
				for v in vs:
					newdist = dist[u][t] + dist[t][v]
					if newdist < dist[u][v]:
						dist[u][v] = newdist
						pred[u][v] = pred[t][v] # route new path through t
		return dist, pred
def processDist(dist):
	processed = {}
	#f: from, t: to
	for f in dist:
		for t in dist[f]:
			if dist[f][t]!=float('inf'):
				if dist[f][t] in processed:
					processed[dist[f][t]].append((f,t))
				else:
					processed[dist[f][t]] = [(f,t)]
	return processed

batchNum = 1
imgCnt = 10000
import sys
k=int(sys.argv[1])
print 'k:'+str(k)
hogs = getHogs(batchNum, imgCnt)
d=len(hogs[0])
D, I = drawKnn(hogs, d, k)

dist,pred=floydwarshall(I,D)
processedDist=processDist(dist)
total=reduce(lambda l,y: y+len(l),processedDist.values())
print total
