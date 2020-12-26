import greedy
import greedy2
import utility
import numpy as np
import matplotlib.pyplot as plt 

x = np.zeros(120)
violate_count1 = 0
violate_count2 = 0
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
	for i in range(requests):
		for j in range(unique_trips1):
			if utility.if_request_in_trip(i+1, j, reverse_trip_hash1):
				rt_graph1[i, j] = 1
	for i in range(requests):
		for j in range(unique_trips2):
			if utility.if_request_in_trip(i+1, j, reverse_trip_hash2):
				rt_graph2[i, j] = 1
	for j in range(vehicles):
		if sum(eps_matrix1[i][j] for i in range(requests)) > 1 or sum(eps_matrix2[i][j] for i in range(requests)) > 1:
			violate_count1 += 1 
			print('Constraint violated')
	for k in range(requests):
		if sum(rt_graph1[k][h]*eps_matrix1[h][c]  for c in range(vehicles) for h in range(unique_trips1)) != 1 \
		or sum(rt_graph2[k][h]*eps_matrix2[h][c]  for c in range(vehicles) for h in range(unique_trips2)) != 1:
			violate_count2 += 1 
			print('Constraint violated')
	x[i] = totalCost1 - totalCost2
 
plt.plot(x)
plt.show()
print('violate_count1:',violate_count1,' violate_count2:',violate_count2)
# print(x[119])