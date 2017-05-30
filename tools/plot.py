import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
resultJson=\
'['\
+'{"k":3, "dCorrect": 5230},'\
+'{"k":4, "dCorrect": 5650},'\
+'{"k":5, "dCorrect": 5807},'\
+'{"k":6, "dCorrect": 5893},'\
+'{"k":7, "dCorrect": 5917},'\
+'{"k":8, "dCorrect": 5940},'\
+'{"k":9, "dCorrect": 5943},'\
+'{"k":10, "dCorrect": 5931},'\
+'{"k":11, "dCorrect": 5900},'\
+'{"k":12, "dCorrect": 5893},'\
+'{"k":13, "dCorrect": 5868},'\
+'{"k":14, "dCorrect": 5844},'\
+'{"k":15, "dCorrect": 5828},'\
+'{"k":20, "dCorrect":5734},'\
+'{"k":30, "dCorrect":5595}'\
+']'
originalJson='''[{"recall": 0.0156433820992, "k": 3, "precision": 75.1200768492}, {"recall": 0.0407688142176, "k": 4, "precision": 70.0103057369}, {"recall": 0.0750162185064, "k": 5, "precision": 67.5553954242}, {"recall": 0.114664790528, "k": 6, "precision": 63.7810170246}, {"recall": 0.156333799367, "k": 7, "precision": 59.9815795533}, {"recall": 0.199283085003, "k": 8, "precision": 57.2101303624}, {"recall": 0.247473503772, "k": 9, "precision": 54.9944432096}, {"recall": 0.298304493431, "k": 10, "precision": 53.1281174291}, {"recall": 0.347935223595, "k": 11, "precision": 51.3598110143}, {"recall": 0.398626182981, "k": 12, "precision": 49.8786012866}, {"recall": 0.45123755756, "k": 13, "precision": 48.5901385089}, {"recall": 0.504128992688, "k": 14, "precision": 47.3533888273}, {"recall": 0.557540540265, "k": 15, "precision": 46.145567734}, {"recall": 0.814055998907, "k": 20, "precision": 41.630264652}, {"recall": 1.06655058824, "k": 25, "precision": 38.5638028556}, {"recall": 1.30972316215, "k": 30, "precision": 36.3448631905}]'''
directCycleJson='''[{"recall": 0.00186040221896, "k": 3, "precision": 68.8888888889}, {"recall": 0.0143230966535, "k": 4, "precision": 76.577540107}, {"recall": 0.0360878021828, "k": 5, "precision": 71.7296222664}, {"recall": 0.0639938354672, "k": 6, "precision": 68.7218045113}, {"recall": 0.0948004958672, "k": 7, "precision": 65.4648432104}, {"recall": 0.12626729899, "k": 8, "precision": 62.1504529342}, {"recall": 0.159494482707, "k": 9, "precision": 59.6067583732}, {"recall": 0.194342016744, "k": 10, "precision": 57.5090274078}, {"recall": 0.230989940025, "k": 11, "precision": 55.9041394336}, {"recall": 0.265757456762, "k": 12, "precision": 54.3576104746}, {"recall": 0.300865047023, "k": 13, "precision": 52.9242029699}, {"recall": 0.333632131267, "k": 14, "precision": 51.5102847613}, {"recall": 0.368859747477, "k": 15, "precision": 50.4859951264}, {"recall": 0.527253992313, "k": 20, "precision": 46.0964007136}, {"recall": 0.671665214019, "k": 25, "precision": 43.2084625581}, {"recall": 0.806174294883, "k": 30, "precision": 41.3146887558}]'''
#, {"recall": 1.25985238008, "k": 50, "precision": 36.986204831}]'''

directCycleResults = json.loads(directCycleJson)
directCycleX = [result['precision'] for result in directCycleResults]
directCycleY = [result['recall'] for result in directCycleResults]
k=[result['k'] for result in directCycleResults]

originalResults = json.loads(originalJson)
originalX = [result['precision'] for result in originalResults]
originalY = [result['recall'] for result in originalResults]

results = json.loads(resultJson)
allPositiveCnt = 4998919
dix = [result['dCorrect']/100.0 for result in results]
diy = [result['dCorrect']*100.0/allPositiveCnt for result in results]



plt.plot(directCycleX, directCycleY, 'r-', originalX, originalY, 'b-', dix, diy, 'g-')
directCyclePatch = mpatches.Patch(color='red', label='direct cycle')
originalPatch = mpatches.Patch(color='blue', label='cycle')
directMatchingPatch = mpatches.Patch(color='green', label='direct matching')
plt.legend(handles=[directCyclePatch, originalPatch, directMatchingPatch])
(xmin, xmax, ymin, ymax) = 0, 100, 0, 1.1
plt.axis((xmin, xmax, ymin, ymax))
for i in range(len(directCycleResults)):
	plt.annotate(str(k[i]), (directCycleX[i]+0.003*directCycleX[i],directCycleY[i]+0.01*directCycleY[i]),color="red")
for i in range(len(originalResults)):
	plt.annotate(str(k[i]), (originalX[i]-0.088*originalX[i],originalY[i]-0.01*originalY[i]),color="blue")
#plt.annotate(str(k[0]), (dix[0]+0.003*dix[0],diy[0]+0.03*diy[0]))
plt.xlabel('precision(%)')
plt.ylabel('recall(%)')
plt.show()
