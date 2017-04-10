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

def getDirectMatching(imgCnt, numMatching, D, I):
	heap=[]
	edges=set()
	for id1 in range(imgCnt):
		for j in range(1,k):
			id2=I[id1][j]
			lo=id1 if id1<id2 else id2
			hi=id1 if id2<id1 else id2
			if (lo, hi) not in edges:
				heapq.heappush(heap, (D[id1][j], (lo,hi)))
				edges.add((lo,hi))
	smallMatchingsWithD = heapq.nsmallest(numMatching,heap)
	matchings=[tupleOfTuple[1] for tupleOfTuple in smallMatchingsWithD]
	return matchings

def getDirectMatchingDirectedEdges(imgCnt, numMatching, D, I, k):
	heap=[]
	for id1 in range(imgCnt):
		for j in range(1,k):
			id2=I[id1][j]
			heapq.heappush(heap, (D[id1][j], (id1,id2)))
	smallMatchingsWithD = heapq.nsmallest(numMatching,heap)
	matchings=[tupleOfTuple[1] for tupleOfTuple in smallMatchingsWithD]
	return matchings

def getLabels(batchNum):
	batchFile = '../data_batch_'+str(batchNum)
	batchInfo = unpickle(batchFile)
	labels = batchInfo['labels']
	return labels

def calcTrueMatching(matchings, labels):
	truthList=[0]*len(matchings)
	for i in range(len(matchings)):
		if labels[matchings[i][0]] == labels[matchings[i][1]]:
			truthList[i] = 1
	return truthList

def findCycle(I, cycleSize):
	cycleSize+=1
	def walk(firstNode, thisNode, path, numNode):
		pathWithThis=path+[thisNode]
		numNode+=1
		if thisNode==firstNode:
			return [pathWithThis]
		if numNode==cycleSize:
			return []
		pathL=[]
		NNs=I[thisNode]
		for i in range(1, len(NNs)):
			neighbor = NNs[i]
			pathL+=walk(firstNode, neighbor, pathWithThis, numNode)
		return pathL
	def findFromEach():
		pathL=[]
		for NNs in I:
			fromNode = NNs[0]
			for i in range(1, len(NNs)):
				toNode=NNs[i]
				pathL+=walk(fromNode, toNode, [fromNode], 1)
		return pathL
	return filter(lambda path: len(path)==4, findFromEach())

def getMatchingSFromCycles(cycles):
	matchingsS=set()
	for cycle in cycles:
		for i in range(0,len(cycle)-1,2):
			node1=cycle[i]
			node2=cycle[i+1]
			lo = node1 if node1<node2 else node2
			hi = node2 if node1<node2 else node1
			if (lo,hi) not in matchingsS:
				matchingsS.add((lo,hi))
	return matchingsS

def getAllPositiveCnt(labels):
	classes = []
	for label in labels:
		if label not in classes:
			classes.append(label)
	allPositiveCnt = 0
	for classNumber in classes:
		classSize = labels.count(classNumber)
		allPositiveCnt+=classSize*(classSize-1)/2
	return allPositiveCnt

def makeFakeIFromDMatchings(dMatchings, imgCnt):
	I = [None]*imgCnt
	for i in range(len(I)):
		I[i]=[i]
	for (fromNode, toNode) in dMatchings:
		I[fromNode].append(toNode)
	return np.asarray(I)

batchNum = 1
imgCnt = 10000
import sys
k=int(sys.argv[1])
print 'k:'+str(k)
hogs = getHogs(batchNum, imgCnt)
d=len(hogs[0])
D, I = drawKnn(hogs, d, k)

numDirectMatching = k*10000/2
dMatchings = getDirectMatchingDirectedEdges(imgCnt, numDirectMatching, D, I, k)
fakeI=makeFakeIFromDMatchings(dMatchings, numDirectMatching)
labels=getLabels(batchNum)
cycleSize=4
cycles=findCycle(fakeI,cycleSize)
matchingsS=getMatchingSFromCycles(cycles)
cTruthList=calcTrueMatching(list(matchingsS), labels)
allPositiveCnt = getAllPositiveCnt(labels)
predictPositiveCnt=len(cTruthList)
truePositiveCnt=cTruthList.count(1)
print "="*15+' Direct Matching Cycle '+'='*15
print "allPositiveCnt:"+str(allPositiveCnt)
print "found matchings using cycles:"+str(predictPositiveCnt)
print "correct matchings:"+str(truePositiveCnt)
print "precision:"+str(truePositiveCnt*100.0/predictPositiveCnt)
print "recall:"+str(truePositiveCnt*100.0/allPositiveCnt)
