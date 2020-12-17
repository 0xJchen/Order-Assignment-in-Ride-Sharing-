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
print('number of TV edges:',edgeNum,'\n')
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
assigned_pairs = []
for k in range(edgeNum,0,-1):
	S_k.sort(key=lambda x:x[3],reverse=True) #sort by cost in decreasing order since pop() is from tail(we want to pop the lowest cost first)
	while len(S_k) > 0:
		e_Tv = S_k.pop()
		if set(e_Tv[1]).isdisjoint(set(R_ok)) and e_Tv[2] not in V_ok:
			R_ok.extend(e_Tv[1])
			V_ok.append(e_Tv[2])
			totalCost += e_Tv[3]
			pair = [e_Tv[1],e_Tv[2]]
			assigned_pairs.append(tuple(pair))

print('length of R_ok:',len(R_ok),'\n')
print('R_ok:',R_ok,'\n')
print('length of V_ok:',len(V_ok),'\n')
print('V_ok:',V_ok,'\n')
print('totalCost:',totalCost,'\n')
print('assigned_pairs of (T,v):',assigned_pairs)