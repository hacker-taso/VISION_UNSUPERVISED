f=open('../results/undirected_cycle_result.txt')
contents=f.read()
parts=contents.split('k:')[1:]
summaries=[]
for part in parts:
	lines=part.split('\n')
	summary={'k':int(lines[0])}
	for line in lines:
		if line.find('precision') != -1:
			summary['precision']=float(line.split(':')[1])
		if line.find('recall') != -1:
			summary['recall']=float(line.split(':')[1])
	summaries.append(summary)

import json
print json.dumps(summaries)
