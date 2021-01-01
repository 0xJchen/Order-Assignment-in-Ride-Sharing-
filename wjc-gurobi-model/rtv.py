from gurobipy import *
import pandas as pd
import numpy as np
import re
from model import *
from utility import *
import matplotlib.pyplot as plt
import greedy as gd
import pickle
# from tqdm import trange
# plot_trips=[]
# task_count = 2
import time


def generate_metadata(task_count):
    requests, trips, vehicles, scores, data = get_task(task_count)
    # plot_trips.append(trips)
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

    task_metadata = {}
    task_metadata['requests'] = requests
    task_metadata['trips'] = trips
    task_metadata['unique_trips'] = unique_trips
    task_metadata['vehicles'] = vehicles

    task_metadata['tv_graph'] = tv_graph
    task_metadata['rt_graph'] = rt_graph
    task_metadata['tv_cost'] = tv_cost
    task_metadata['task_count']=task_count

    meta_file = "./"+"metadata/"+str(task_count)
    pickle.dump(task_metadata, open(meta_file, "wb"))
    return task_metadata


def run_one_task(task_count, from_metadata=True, greedy=0):

    if from_metadata:
        meta_file = "./"+"metadata/"+str(task_count)
        task_metadata = pickle.load(open(meta_file, 'rb'))
    else:
        task_metadata = generate_metadata(task_count)

    # requests = task_metadata['requests']
    # trips = task_metadata['trips']
    # unique_trips = task_metadata['unique_trips']
    # vehicles = task_metadata['vehicles']
    # tv_graph = task_metadata['tv_graph']
    # rt_graph = task_metadata['rt_graph']
    # tv_cost = task_metadata['tv_cost']
    print("finish loading metadata")

    eps_matrix = None
    kai_matrix = None
    gd_cost = None
    gd_time = None
    if greedy == 0:  # pure mip
        mip_time, mip_cost = rtv(task_metadata, False, eps_matrix, kai_matrix)
    elif greedy == 1:
        _, eps_matrix, kai_matrix, gd_cost, gd_time = gd.greedy_initial1(
            task_count)
        mip_time, mip_cost=rtv(task_metadata, True, eps_matrix, kai_matrix)
    else:
        assert(greedy == 2)
        _, eps_matrix, kai_matrix, gd_cost, gd_time = gd.greedy_initial2(
            task_count)
        mip_time, mip_cost = rtv(task_metadata, True, eps_matrix, kai_matrix)
    return mip_time, mip_cost, gd_cost, gd_time


def run_task(task_count, initialization, eps_matrix, kai_matrix,):
    requests, trips, vehicles, scores, data = get_task(task_count)

    param = {}
    param['requests'] = requests
    param['trips'] = trips
    param['unique_trips'] = unique_trips
    param['vehicles'] = vehicles

    task_metadata = {}
    task_metadata['requests'] = requests
    task_metadata['trips'] = trips
    task_metadata['unique_trips'] = unique_trips
    task_metadata['vehicles'] = vehicles
    task_metadata['tv_graph'] = tv_graph
    task_metadata['rt_graph'] = rt_graph
    task_metadata['tv_cost'] = tv_cost

    meta_file = "task1"+str(task_count)
    pickle.dump(task_metadata, open("meta_file", "wb"))

    if initialization:
        task_time, objvalue = rtv(
            tv_graph, rt_graph, tv_cost, param, True, eps_matrix, kai_matrix,)
    else:
        task_time, objvalue = rtv(
            tv_graph, rt_graph, tv_cost, param, False, eps_matrix, kai_matrix,)
    return task_time, objvalue


def task_info(task_count):
    print('*'*20+'TASK: '+str(task_count)+'*'*20)


if __name__ == '__main__':
    st = time.time()
    pure_mip_time = []
    pure_mip_value = []
    greedy_mip_time = []
    greedy_mip_value = []
    task_list = [i for i in range(112, 121)]
    msg("start without initialization")
    # without initialization
    for i in task_list:
        task_info(i)
        task_time, objvalue = run_task(i, False, None, None)
        pure_mip_time.append(task_time)
        pure_mip_value.append(objvalue)
    # with initalization
    msg("start with initialization")
    for i in task_list:
        task_info(i)
        df_unique_trip, eps_matrix, kai_matrix = gd.greedy_initial(i)
        task_time, objvalue = run_task(i, True, eps_matrix, kai_matrix)
        greedy_mip_time.append(task_time)
        greedy_mip_value.append(objvalue)
    save_list(pure_mip_time, pure_mip_value, greedy_mip_time, greedy_mip_value)
    compare_time(pure_mip_time, greedy_mip_time)
    compare_value(pure_mip_value, greedy_mip_value)
    print(pure_mip_value, greedy_mip_value)
    print([a_i - b_i for a_i, b_i in zip(pure_mip_value, greedy_mip_value)])
    print("finish in {}".format(time.time()-st))
    # print([a_i - b_i for a_i, b_i in zip(pure_mip_value, greedy_mip_value)])
