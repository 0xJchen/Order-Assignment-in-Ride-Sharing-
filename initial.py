import re

#read in task files and return a n*4 array.

# file = input('task_file_path:')
file = './split_data/task1.txt'

f = open(file,'r')
lineNumber = 0
keyword = 'Task'
data = []
for line in f:
	m = re.search(keyword,line)
	lineNumber += 1
	if m is None:
		row = line.split()
		data.append(row)
edgeNum = lineNumber-1
print('number of TV edges:',edgeNum)
# print(data)
f.close()

#format conversion
for i in range(edgeNum):
	data[i][3] = float(data[i][3])
	data[i][1] = data[i][1].split(',')

#greedy assignment
R_ok = []
V_ok = []
S_k = data
totalCost = 0
assign = []
for k in range(edgeNum,0,-1):
	S_k.sort(key=lambda x:x[3],reverse=True) #sort by cost in decreasing order since pop() is from tail(we want to pop the lowest cost first)
	while len(S_k) > 0:
		e_Tv = S_k.pop()
		if set(e_Tv[1]).isdisjoint(set(R_ok)) and e_Tv[2] not in V_ok:
			R_ok.extend(e_Tv[1])
			V_ok.append(e_Tv[2])
			totalCost += e_Tv[3]
			assign.append(e_Tv)

print('length of R_ok:',len(R_ok))
print('R_ok:',R_ok)
print('length of V_ok:',len(V_ok))
print('V_ok:',V_ok)
print('totalCost:',totalCost)
print('assign:',assign)