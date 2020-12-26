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
	for j in range(vehicles):
		if sum(eps_matrix1[i][j] for i in range(requests)) > 1 or sum(eps_matrix2[i][j] for i in range(requests)) > 1:
			violate_count1 += 1 
			print('Constraint violated')
	for k in range(requests):
		if kai_matrix1[k] != 0 or kai_matrix2[k] != 0:
			violate_count2 += 1 
			print('Constraint violated')
	x[i] = totalCost1 - totalCost2
 
plt.plot(x)
plt.show()
print('violate_count1:',violate_count1,' violate_count2:',violate_count2)
# print(x[119])