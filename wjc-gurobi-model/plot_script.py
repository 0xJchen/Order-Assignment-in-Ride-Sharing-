import pickle
import greedy
import greedy2
import utility
import numpy as np
import matplotlib.pyplot as plt 

x = np.zeros(120)
violate1 = np.zeros(120)
violate2 = np.zeros(120)

infile = open('rt_graph_list','rb')
rt_graph_list = pickle.load(infile)

for i in range(120):
	requests,trips,vehicles,scores,data = utility.get_task(i+1)
	df_unique_trip1,eps_matrix1,kai_matrix1,totalCost1 = greedy.greedy_initial(i+1)
	df_unique_trip2,eps_matrix2,kai_matrix2,totalCost2 = greedy2.greedy_initial2(i+1)
	unique_trips1 = df_unique_trip1.shape[0]
	unique_trips2 = df_unique_trip2.shape[0]
	rt_graph1 = rt_graph_list[2*i]
	rt_graph2 = rt_graph_list[2*i+1]
	for j in range(vehicles):
		if sum(eps_matrix1[i][j] for i in range(requests)) > 1 :
			violate1[i] = 1
			print('Constraint violated')
		if sum(eps_matrix2[i][j] for i in range(requests)) > 1 :
			violate2[i] = 1
			print('Constraint violated')
	for k in range(requests):
		if sum(rt_graph1[k][h]*eps_matrix1[h][c]  for c in range(vehicles) for h in range(unique_trips1)) != 1:
			violate1[i] = 1
			print('Constraint violated')
		if sum(rt_graph2[k][h]*eps_matrix2[h][c]  for c in range(vehicles) for h in range(unique_trips2)) != 1:
			violate2[i] = 1
			print('Constraint violated')
	x[i] = totalCost1 - totalCost2

plt.plot(x)
plt.savefig('diff.jpg')

outfile1 = open('violate1','wb')
outfile2 = open('violate2','wb')
pickle.dump(violate1, outfile1)
pickle.dump(violate1, outfile2)