import os

o = int(input('number of orders:'))
v = int(input('number of vehicles:'))

f = open('test.txt','r')

data = []
lineCounts = 0

for line in f.readlines():
	lineCounts += 1
	temp = []
	line = line.strip()
	numbers = line.split()
	for number in numbers:
		temp.append(int(number))
	data.append(temp)

print('number of lines:', lineCounts,'\n')
print("task_data:")
for task in data:
	print(task)

orders_count = []
orders = []
for d in data:
	orders.append(d[1])
for i in range(o):
	orders_count.append(orders.count(i+1))
print("orders_count:",orders_count)

totalCost = 0
vehicle_used = []
task_pairs = []

offset = 0
for i in range(o):
	cost = float('inf')
	vehicle_assign = 0
	for l in range(offset, offset + orders_count[i]):
 		if data[l][3] < cost and data[l][2] not in vehicle_used:
 			cost = data[l][3]
 			vehicle_assign = data[l][2]
	offset += orders_count[i]
	task_pairs.append([i+1,vehicle_assign])
	vehicle_used.append(vehicle_assign)
	totalCost += cost

print('vehicles assigned with orders:\n',vehicle_used)
print('\n')
print('allocation pairs of orders and vehicles:(order,vehicle)')
for pair in task_pairs:
	print(pair)
print('\n')
print('totalCost:',totalCost)
print('AvgOrderCost:',totalCost/o)

f.close()