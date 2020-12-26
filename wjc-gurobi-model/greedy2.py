import re
import copy
import numpy as np

def greedy_initial2(task_count):
	filename='./split_data/task'+str(task_count)+'.txt'
	f = open(filename,'r')
	info=f.readline()
	requests = int(info.split('Orders=')[1].split(' ')[0])
	vehicles = int(info.split('Vehicles=')[1].split(' ')[0])
	scores = int(info.split('Scores=')[1].split(r'\n')[0])
	# print(requests,vehicles,scores)
	lineNumber = 0
	keyword = 'Task'
	data = []
	for line in f:
		m = re.search(keyword,line)
		lineNumber += 1
		if m is None:
			row = line.split()
			data.append(row)
	edgeNum = lineNumber
	# print('number of TV edges:',edgeNum,'\n')
	# print(data)
	f.close()

	#format conversion
	for i in range(edgeNum):
		data[i][3] = float(data[i][3])
		data[i][1] = data[i][1].split(',')

	#greedy assignment
	R_ok = []
	V_ok = []
	S_k = copy.deepcopy(data)
	S_k1 = []
	S_k2 = []
	for i in S_k:
		if len(i[1])==1:
			S_k1.append(i)
		else:
			S_k2.append(i)
	# print(S_k)
	totalCost = 0
	assigned_pairs = []
	S_k2.sort(key=lambda x:x[3],reverse=True) #sort by cost in decreasing order since pop() is from tail(we want to pop the lowest cost first)
	while len(S_k2) > 0:
		e_Tv = S_k2.pop()
		if set(e_Tv[1]).isdisjoint(set(R_ok)) and e_Tv[2] not in V_ok:
				R_ok.extend(e_Tv[1])
				V_ok.append(e_Tv[2])
				totalCost += e_Tv[3]
				pair = [e_Tv[1],e_Tv[2]]
				assigned_pairs.append(tuple(pair))

	S_k1.sort(key=lambda x:x[3],reverse=True) #sort by cost in decreasing order since pop() is from tail(we want to pop the lowest cost first)
	while len(S_k1) > 0:
		e_Tv = S_k1.pop()
		if set(e_Tv[1]).isdisjoint(set(R_ok)) and e_Tv[2] not in V_ok:
				R_ok.extend(e_Tv[1])
				V_ok.append(e_Tv[2])
				totalCost += e_Tv[3]
				pair = [e_Tv[1],e_Tv[2]]
				assigned_pairs.append(tuple(pair))



	unique_trips = []
	for i in range(edgeNum):
		if(data[i][1] not in unique_trips):
			unique_trips.append(data[i][1])

	num_unique_trips = len(unique_trips)
	# trip_dict = {}
	# for i in range(num_unique_trips):
	# 	trip_dict[i] = unique_trips[i]

	eps_matrix = []
	for i in range(num_unique_trips):
		eps_matrix.append([])
		for j in range(vehicles):
			eps_matrix[i].append(0)
			tv_pair = [unique_trips[i],str(j)]
			if tuple(tv_pair) in assigned_pairs:
				eps_matrix[i][j] = 1

	kai_matrix = []
	for i in range(requests):
		kai_matrix.append(1)
		if str(i+1) in R_ok:
			kai_matrix[i] = 0
	df_unique_trip = []
	for i in unique_trips:
		trip = ','.join(i)
		df_unique_trip.append(trip)


	# return trip_dict,eps_matrix,kai_matrix
	return np.array(df_unique_trip),np.array(eps_matrix),np.array(kai_matrix),totalCost


if __name__ == '__main__':
	df_unique_trip,eps_matrix,kai_matrix,totalCost = greedy_initial2(1)
	print("number of unique_trips:",len(df_unique_trip),'\n')
	print("unique_trips:",df_unique_trip,'\n')
	print("kai_matrix:",kai_matrix,'\n')
	print("eps_matrix_size:",eps_matrix.shape)
	print(totalCost)