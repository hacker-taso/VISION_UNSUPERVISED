import cPickle
from  PIL import Image
import numpy as np
import os

batch=5
folder_name='batch'+str(batch)
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def unpickle(file): 
    import cPickle 
    fo = open(file, 'rb') 
    dict = cPickle.load(fo) 
    fo.close() 
    return dict

def intoImageFile(filename, img_formatted):
	img_rgb = [None]*32
	for i in range(32):
		row=[None]*32
		for j in range(32):
			row[j]=[img_formatted[i*32+j], img_formatted[1024+i*32+j], img_formatted[2048+i*32+j]]
		img_rgb[i]=row
	im = Image.fromarray(np.array(img_rgb))
	im.save(folder_name+"/"+filename)

d=unpickle('data_batch_'+str(batch))

imgs_formatted = d['data']
filenames = d['filenames']
for i in range(len(imgs_formatted)):
	intoImageFile(str(i)+'.'+filenames[i].split('.')[1], imgs_formatted[i])