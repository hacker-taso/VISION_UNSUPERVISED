import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
resultJson=\
'['\
+'{"k":3,"precision":78.5046728972,"recall":0.00840181647272, "dCorrect": 5230},'\
+'{"k":4,"precision":74.7318235995,"recall":0.0250854234686, "dCorrect": 5650},'\
+'{"k":5,"precision":70.0355660937,"recall":0.0472702198215, "dCorrect": 5807},'\
+'{"k":6,"precision":66.5936473165,"recall":0.0729757773631, "dCorrect": 5893},'\
+'{"k":7,"precision":64.0498991935,"recall":0.101681983645, "dCorrect": 5917},'\
+'{"k":8,"precision":61.8242927831,"recall":0.13246863972, "dCorrect": 5940},'\
+'{"k":9,"precision":59.5034122259,"recall":0.163955447168, "dCorrect": 5943},'\
+'{"k":10,"precision":57.9219254476,"recall":0.197382674134, "dCorrect": 5931},'\
+'{"k":11,"precision":56.4367535949,"recall":0.231610074098, "dCorrect": 5900},'\
+'{"k":12,"precision":55.168124715,"recall":0.266177547586, "dCorrect": 5893},'\
+'{"k":13,"precision":54.0585923544,"recall":0.302685440592, "dCorrect": 5868},'\
+'{"k":14,"precision":52.8145282077,"recall":0.338593203851, "dCorrect": 5844},'\
+'{"k":15,"precision":51.8287637226,"recall":0.37588126553, "dCorrect": 5828},'\
+'{"k":20, "precision":47.4970994266, "recall":0.56506216644, "dCorrect":5734},'\
+'{"k":30, "precision":42.24395022, "recall":0.966268907338,"dCorrect":5595}'\
+']'

results = json.loads(resultJson)
precisions = [result['precision'] for result in results]
recalls = [result['recall'] for result in results]
k=[result['k'] for result in results]
x=precisions
y=recalls
dix = [result['dCorrect']/100.0 for result in results]
allPositiveCnt = 4998919
diy = [result['dCorrect']*100.0/4998919 for result in results]
plt.plot(x, y, 'r.', dix, diy, 'b.')
cyclePatch = mpatches.Patch(color='red', label='cycle')
directPatch = mpatches.Patch(color='blue', label='direct')
plt.legend(handles=[cyclePatch, directPatch])
(xmin, xmax, ymin, ymax) = 0, 100, 0, 1.1
plt.axis((xmin, xmax, ymin, ymax))
for i in range(len(results)):
	plt.annotate(str(k[i]), (x[i]+0.003*x[i],y[i]+0.01*y[i]))
plt.annotate(str(k[0]), (dix[0]+0.003*dix[0],diy[0]+0.03*diy[0]))
plt.xlabel('precision(%)')
plt.ylabel('recall(%)')
plt.show()
