import pandas as pd
import numpy as np
import re
def sepa():
    print('*'*80)
def sepan(t):
    for i in range(t):
        print('*'*80)
def p_df(data):
    sepa()
    print(data)
    # print(type(data))
    # print(data.index)
    # print(data.columns)
def p_shape(data):
    print(data.shape)
def p_l(data):
    print("length: ",len(data))
    print(data)
def get_task(task_count):
    filename='./split_data/task'+str(task_count)+'.txt'
    with open(filename,'r') as f:
        info=f.readline()
    requests=int(info.split('Orders=')[1].split(' ')[0])
    vehicles=int(info.split('Vehicles=')[1].split(' ')[0])
    scores=int(info.split('Scores=')[1].split(r'\n')[0])
    data = pd.read_table(filename,delim_whitespace=True)
    # data = data.drop(task_name, 1)
    trips=data.shape[0]
    # costs=int(info.split('Scores=')[1].split(r'\n')[0])
    print("No:{},requests: {}, trips: {},vehicles: {}".format(task_count,requests,trips,vehicles))
    print(data.shape)
    return requests,trips,vehicles,scores,data
def if_request_in_trip(request,new_trip_number,reverse_trip_hash):
    """
    
    """
    #find corresponding trip pair from the {newly assigned number}
    trip_pair=reverse_trip_hash[str(new_trip_number)]
    # print(trip_pair)
    trip_member=trip_pair.split(',')
    flag=0
    if str(request) in trip_member:
        flag=1
    return flag