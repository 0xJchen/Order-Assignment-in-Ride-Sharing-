import re

file = input('file_path:')
f = open(file,'r')
# print(type(f))
# line1 = f.readlines()
# print(line1)

lineNumber = 0
keyword = 'Task'
raw_data = []

for line in f:
	m = re.search(keyword,line)
	lineNumber += 1
	if m is None:
		row = line.split()
		raw_data.append(row)

print('lineNumber:',lineNumber)
print(raw_data)

f.close()