from gurobipy import *
import pandas as pd
import numpy as np
import re
from model import *
from utility import *
import matplotlib.pyplot as plt

plot_trips=[]
# task_count = 2

def run_task(task_count):
    requests, trips, vehicles, scores, data = get_task(task_count)
    plot_trips.append(trips)
    # extract columns from dataframe
    # print(data)
    trip_col = 'Orders='+str(requests)
    df_trip = data[trip_col]  # contain pair
    # p_df(df_trip)
    df_unique_trip = df_trip.unique()
    # p_df(df_unique_trip)
    vehicle_col = 'Vehicles='+str(vehicles)
    df_vehicle = data[vehicle_col]
    cost_col = 'Scores='+str(scores)
    df_cost = data[cost_col]

    unique_trips = df_unique_trip.shape[0]

    # assign a new order for each unique trip from 0->#trips-1
    mapped_trip = [str(i) for i in range(unique_trips)]  # 0->80
    trip_hash = dict(zip(df_unique_trip, mapped_trip))  # old to new
    reverse_trip_hash = {v: k for k, v in trip_hash.items()}  # new to old
    # print("trip hash",trip_hash)

    # initialize graphs
    # tv_graph=pd.DataFrame(0,index=mapped_trip,columns=[str(i) for i in range(vehicles)])
    tv_graph = np.zeros((unique_trips, vehicles))
    # print("tv graph size: {}".format(tv_graph.shape))
    rt_graph = np.zeros((requests, unique_trips))
    # print("rt graph size: {}".format(rt_graph.shape))
    tv_cost = np.full((unique_trips, vehicles), 1000000)
    # print("tv_cost graph size: {}".format(tv_cost.shape))

    # iterate through all trips in the dataframe to construct tv graph
    for i in range(trips):
        # an stri indicating the newly assigned number
        r = trip_hash[df_trip[i]]
        c = int(df_vehicle[i])-1  # Note: in df_vehicles: (1,333), so should -1
        tv_graph[int(r), int(c)] = 1
    # print("tv_graph: ",tv_graph)
    # find the trip_pair in the reverse_dict and determine if request is in it
    for i in range(requests):
        for j in range(unique_trips):
            if if_request_in_trip(i+1, j, reverse_trip_hash):
                rt_graph[i, j] = 1
    # print("rt_graph: ",rt_graph)
    # iterate thrugh all trips in the dataframe to construct the tv_cost graph
    for i in range(unique_trips):
        col = int(df_vehicle[i])-1
        tv_cost[i, col] = float(df_cost[i])

    # print("tv_cost: ",tv_cost)
    param = {}
    param['requests'] = requests
    param['trips'] = trips
    param['unique_trips'] = unique_trips
    param['vehicles'] = vehicles

    task_time=rtv(tv_graph, rt_graph, tv_cost, param)
    return task_time
def task_info(task_count):
    print('*'*20+'TASK: '+str(task_count)+'*'*20)
if __name__=='__main__':
    plot_time=[]
    # task_list=[i for i in range(1,10)]
    task_list=[i for i in range(118,120)]
    plt.show()
    for i in task_list:
        task_info(i)
        task_time=run_task(i)
        plot_time.append(task_time)
        # print(plot_time)
    plt.plot(plot_time)
    plt.show()   


        
#     df = pd.DataFrame({'month': [1, 4, 7, 10],
#                     'year': [2012, 2014, 2013, 2014],
#                      'sale': [55, 40, 84, 31]})
#     s = pd.Series(['a','b','c','d'])
#     df=df.set_index(s)
#     p(df)
#     print('*'*80)
#     print(df.at['a','month'])
