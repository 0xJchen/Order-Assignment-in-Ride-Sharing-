import pickle
import greedy
import greedy2
import utility
import numpy as np
import matplotlib.pyplot as plt 

rt_graph_list = []
for i in range(120):
	requests,trips,vehicles,scores,data = utility.get_task(i+1)
	df_unique_trip1,eps_matrix1,kai_matrix1,totalCost1 = greedy.greedy_initial(i+1)
	df_unique_trip2,eps_matrix2,kai_matrix2,totalCost2 = greedy2.greedy_initial2(i+1)
	unique_trips1 = df_unique_trip1.shape[0]
	unique_trips2 = df_unique_trip2.shape[0]
	rt_graph1 = np.zeros((requests, unique_trips1))
	rt_graph2 = np.zeros((requests, unique_trips2))
	mapped_trip1 = [str(i) for i in range(unique_trips1)]  # 0->80
	trip_hash1 = dict(zip(df_unique_trip1, mapped_trip1))  # old to new
	reverse_trip_hash1 = {v: k for k, v in trip_hash1.items()}  # new to old
	mapped_trip2 = [str(i) for i in range(unique_trips2)]  # 0->80
	trip_hash2 = dict(zip(df_unique_trip2, mapped_trip2))  # old to new
	reverse_trip_hash2 = {v: k for k, v in trip_hash2.items()}  # new to old
	for r in range(requests):
		for j in range(unique_trips1):
			if utility.if_request_in_trip(r+1, j, reverse_trip_hash1):
				rt_graph1[r, j] = 1
	rt_graph_list.append(rt_graph1)
	for r in range(requests):
		for j in range(unique_trips2):
			if utility.if_request_in_trip(r+1, j, reverse_trip_hash2):
				rt_graph2[r, j] = 1
	rt_graph_list.append(rt_graph2)

outfile = open('rt_graph_list','wb')
pickle.dump(rt_graph_list, outfile)