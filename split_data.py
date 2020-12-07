import re
import linecache

f = open('vrp_task.txt','r')
number = []
lineNumber = 0
keyword = 'Task'
outFileName = 'task'

for line in f:
	m = re.search(keyword,line)
	if m is not None:
		number.append(lineNumber)
	lineNumber += 1

size = int(len(number))

for i in range(0,size-1):
	start = number[i];
	end = number[i+1];
	destLines = linecache.getlines('vrp_task.txt')[start:end]
	outfile = open('./split_data/'+outFileName+str(i+1)+'.txt','w')
	for line in destLines:
		outfile.write(line)
	outfile.close()

